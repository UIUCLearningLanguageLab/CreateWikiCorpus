import re
from multiprocessing import cpu_count
import shutil
from pathlib import Path

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
    quiet = True
    debug = False
    article = False
    log_file = False
    version = False
    processes = max(1, cpu_count() - 1)

    # arguments that do affect content (overwritten by params.param2requests and params.param2defaults)
    links = False
    sections = False
    lists = False
    namespaces = ""
    templates = {}
    no_templates = True
    revision = False
    min_text_length = 0
    filter_disambig_pages = True
    ignored_tags = ""
    discard_elements = ""
    keep_tables = False
    filter_category = None


def main(param2val):  # param2val is supplied by Ludwig and will be different on each machine

    part = param2val['part']
    num_machines = param2val['num_machines']
    input_file_name = param2val['input_file_name']
    min_body_length = param2val['min_body_length']
    project_path = Path(param2val['project_path'])  # on worker, evaluates to media/research_data/CreateWikiCorpus
    save_path = Path(param2val['save_path'])  # on worker, this path points to a folder inside the job folder

    # check that input file exists
    if not (project_path / 'data' / input_file_name).exists():
        raise FileNotFoundError(f'Did not find input file at {project_path / "data"}')

    # overwrite Args attributes with values in param2val
    for k, v in param2val.items():
        if k in Args.__dict__:
            setattr(Args, k, v)
            print('Setting {}={}'.format(k, v))

    # remove any text files from previous job - otherwise they will all be processed by step 2
    if config.LocalDirs.extractor_output.exists():
        shutil.rmtree(config.LocalDirs.extractor_output)

    # step 1
    print('Starting extraction with part={} and num_machines={}'.format(part, num_machines))
    Args.input = str(project_path / 'data' / input_file_name)  # always put xml file on shared drive
    Args.output = str(config.LocalDirs.extractor_output)  # folder on ludwig worker (not on shared drive)
    extract_from_wiki(Args, part, num_machines)  # this saves extracted pages to worker

    # step 2
    print('Starting additional cleaning steps')
    titles, bodies = get_cleaned_titles_and_bodies(Args.output, min_body_length)

    # step 3
    print('Saving titles and bodies to text to save_path')  # will be copied to server at end of job
    out_titles_p = save_path / 'titles.txt'
    out_bodies_p = save_path / 'bodies.txt'  # TODO test save_path
    f1 = out_titles_p.open('w')
    f2 = out_bodies_p.open('w')
    for body, title in zip(bodies, titles):
        flattened = re.sub('\n+', ' ', body)
        f1.write(title + '\n')
        f2.write(flattened + '\n')
    # wait until content in buffer is written to disk
    f1.close()
    f2.close()

    return []  # Ludwig package requires a list (empty, or containing pandas series objects)
