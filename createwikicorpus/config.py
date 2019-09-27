from pathlib import Path


class RemoteDirs:
    root = Path('/media/research_data') / 'CreateWikiCorpus'
    runs = root / 'runs'
    data = root / 'data'


class LocalDirs:
    root = Path(__file__).parent.parent
    src = root / 'createwikicorpus'
    runs = root / '{}_runs'.format(src.name)
    wiki_output = root / 'output'


class Global:
    debug = False
    min_article_length = 1