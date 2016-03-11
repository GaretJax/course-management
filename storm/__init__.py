"""
STORM

MIT License. See LICENSE for more details.
Copyright (c) 2016, Jonathan Stoppani
"""

from os.path import dirname, join
import subprocess


def get_commit():
    try:
        with open(join(dirname(__file__), 'COMMIT')) as fh:
            return fh.read().strip()
    except:
        pass

    try:
        git_cmd = ['git', 'rev-parse', '--short', 'HEAD']
        return subprocess.check_output(git_cmd).strip()
    except:
        pass

    return 'develop'


__version__ = '0.1.0'
__commit__ = get_commit()
