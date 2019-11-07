from pathlib import Path


class LocalDirs:
    root = Path(__file__).parent.parent
    src = root / 'createwikicorpus'
    runs = root / '{}_runs'.format(src.name)
    extractor_output = root / 'extractor_output'


class Global:
    debug = False