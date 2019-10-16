from pathlib import Path
import sys

if sys.platform == 'darwin':
    mnt_point = '/Volumes'
elif 'linux' == sys.platform:
    mnt_point = '/media'
else:
    raise SystemExit('Ludwig does not support this platform')


class RemoteDirs:
    root = Path(mnt_point) / 'research_data' / 'CreateWikiCorpus'
    runs = root / 'runs'
    data = root / 'data'


class LocalDirs:
    root = Path(__file__).parent.parent
    src = root / 'createwikicorpus'
    runs = root / '{}_runs'.format(src.name)
    extractor_output = root / 'extractor_output'


class Global:
    debug = False