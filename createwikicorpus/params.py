from createwikicorpus import config

# pass unique integers to each machine to allow unique start_id
# all the values must be in a list
param2requests = {'part': [0, 1, 2, 3, 4, 5, 6],
                  'num_machines': [7],
                  'input_file_name': ['enwiki-20190920-pages-articles-multistream.xml.bz2']}

# used to overwrite parameters when --debug flag is on (when submitting jobs to Ludwig)
param2debug = {'part': 0,
               'num_machines': 1,
               'min_body_length': 1,
               'input_file_name': 'dummy_input.xml'}


param2default = {'part': 0,
                 'num_machines': 1,  # by default, assume, program is run on 1 machine, not on Ludwig
                 'min_body_length': 1,
                 'input_file_name': 'dummy_input.xml',

                 # required for third-party wikiExtractor
                 'links': False,
                 'sections': True,
                 'lists': True,
                 'namespaces': "",
                 'templates': {},
                 'no_templates': True,
                 'revision': False,
                 'min_text_length': 0,
                 'filter_disambig_pages': False,
                 'ignored_tags': "",
                 'discard_elements': "",
                 'keep_tables': False,
                 'filter_category': None
                 }

for input_file_name in param2requests['input_file_name']:
    if not (config.RemoteDirs.data / input_file_name).exists():
        raise FileNotFoundError('Did not find input file at {}'.format(config.RemoteDirs.data))