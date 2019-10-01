import re
from multiprocessing import cpu_count
import shutil

from wikiExtractor.WikiExtractor import extract_from_wiki
from createwikicorpus.clean import get_cleaned_titles_and_bodies
from createwikicorpus import config


class Args:
    """
    arguments required by third-party wikiExtractor code
    """

    # arguments that do not affect content (only runtime)
    bytes = "50M"
    compress = False
    json = False
    html = False
    quiet = False
    debug = False
    article = False
    log_file = False
    version = False
    processes = max(1, cpu_count() - 1)

    # arguments that affect do affect content
    links = False
    sections = True
    lists = True
    namespaces = ""
    templates = {}
    no_templates = True
    revision = False
    min_text_length = 0
    filter_disambig_pages = False
    ignored_tags = ""
    discard_elements = ""
    keep_tables = False
    filter_category = None


def save_to_shared_drive(titles, bodies, param2val):
    job_name = config.LocalDirs.runs / param2val['param_name'] / param2val['job_name']
    if not job_name.is_dir():
        job_name.mkdir(parents=True)
    out_titles_p = job_name / 'titles.txt'
    out_bodies_p = job_name / 'bodies.txt'

    f1 = out_titles_p.open('w')
    f2 = out_bodies_p.open('w')

    for body, title in zip(bodies, titles):
        flattened = re.sub('\n+', ' ', body)

        f1.write(title + '\n')
        f2.write(flattened + '\n')

    # wait until content in buffer is written to disk
    f1.close()
    f2.close()

    # copy
    src = config.LocalDirs.runs / param2val['param_name'] / param2val['job_name']
    dst = config.RemoteDirs.runs / param2val['param_name'] / param2val['job_name']
    print('Copying contents of {} to {}'.format(src, dst))
    shutil.copytree(str(src), str(dst))


def main(param2val):  # param2val will be different on each machine

    part = param2val['part']
    num_machines = param2val['num_machines']
    input_file_name = param2val['input_file_name']
    min_body_length = param2val['min_body_length']

    if config.Global.debug:
        input_file_name = 'dummy_input.xml'

    # overwrite Args attributes with values in param2val
    for k, v in param2val.items():
        if k in Args.__dict__:
            setattr(Args, k, v)
            print('Setting {}={}'.format(k, v))

    # step 1
    print('Word_V_World: Starting extraction with part={} and num_machines={}'.format(part, num_machines))
    Args.input = str(config.RemoteDirs.data / input_file_name)  # always put xml file on shared drive
    Args.output = str(config.LocalDirs.extractor_output)  # folder on ludwig worker (not on shared drive)
    extract_from_wiki(Args, part, num_machines)  # this saves extracted pages to worker

    # step 2
    print('Word_V_World: Starting additional cleaning steps')
    titles, bodies = get_cleaned_titles_and_bodies(Args.output, min_body_length)

    # step 3
    print('Word_V_World: Saving to text...')
    save_to_shared_drive(titles, bodies, param2val)

    return []  # ludwigcluster requires a list (empty, or containing pandas data frames)
