"""This package checks or makes blake2b hashes for files."""

import sys
import pathlib
import funcs


if len(sys.argv) == 3:
    INPATH = pathlib.Path(sys.argv[2]).resolve()

    if sys.argv[1] == 'make':
        funcs.write_files_current_hash(INPATH)

    elif sys.argv[1] == 'check':
        funcs.check_hash(INPATH)

    else:
        print('First arg needs to be check or make. Second arg file or dir to work on.')
        sys.exit()
else:
    print('First arg needs to be check or make. Second arg file or dir to work on.')
    sys.exit()
