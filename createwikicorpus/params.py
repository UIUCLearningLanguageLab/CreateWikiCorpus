
# pass unique integers to each machine to allow unique start_id
# all the values must be in a list
param2requests = {'part': [0, 1, 2, 3, 4, 5],
                  'num_machines': [6],
                  'no_templates': [False, True],
                  'input_file_name': ['enwiki-20190920-pages-articles-multistream.xml.bz2']}

# used to overwrite parameters when --debug flag is on (when calling "ludwig-local")
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
                 'sections': False,
                 'lists': False,
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

# some hard constraints specific to creating Wikipedia corpora on Ludwig
if len(param2requests['part']) != param2requests['num_machines'][0]:
    raise ValueError('"num_machines" must match length of "part".')

if len(param2requests['num_machines']) != 1:
    raise ValueError('It does not make sense to vary "num_machines" across jobs')

if list(range(param2requests['num_machines'][0])) != param2requests['part']:
    raise ValueError('Make sure "part" points to a sequence of consecutive integers,'
                     'ending in "num_machines"-1.')
