"""__main__.py runs if python.exe ./dir is called."""
import os
import sys
import pathlib
import funcs

if len(sys.argv) == 3:
    INPATH = pathlib.Path(sys.argv[2]).resolve()
    os.chdir(INPATH.parent)

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
