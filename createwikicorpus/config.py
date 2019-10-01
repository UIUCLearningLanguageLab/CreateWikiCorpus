from pathlib import Path
import sys

if 'win' in sys.platform:
    raise SystemExit('LudwigCluster does not support Windows')
elif 'linux' == sys.platform:
    mnt_point = '/media'
else:
    # assume MacOS
    mnt_point = '/Volumes'


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