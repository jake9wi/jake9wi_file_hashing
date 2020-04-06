"""functions."""
import os
import sys
import pathlib
import hashlib
import json

HASHALGO = 'blake2b'


def make_hash_blake2b(inpath):
    """
    Take a file and compute its blake2b hash.

    refrence:
    https://stackoverflow.com/questions/22058048/hashing-a-file-in-python
    """
    buf_size = 65536  # lets read stuff in 64kb chunks!

    thehash = hashlib.blake2b()

    with open(inpath, 'rb') as the_file:
        while True:
            data = the_file.read(buf_size)
            if not data:
                break
            thehash.update(data)

    return thehash.hexdigest()


def check_hash(inpath):
    """Check hashes."""
    if (inpath.exists() and inpath.is_file() and
            (inpath.suffixes[-1] == '.json') and
            (inpath.suffixes[-2] == '.hash')):

        infile = json.load(inpath.open(mode='r'))

        if infile['hash-algo'] == HASHALGO:
            thehash = make_hash_blake2b(pathlib.Path(infile['file-name']))

            if thehash == infile['hash']:
                print('good hash for file: {}'.format(infile['file-name']))
            else:
                print('bad hash for file: {}'.format(infile['file-name']))
        else:
            print('this script uses blake2b not {}'
                  .format(infile['hash-algo']))

    elif (inpath.exists() and inpath.is_dir()):

        file_list = inpath.glob('*.hash.json')

        for files in file_list:

            infile = json.load(files.open(mode='r'))

            if infile['hash-algo'] == HASHALGO:
                thehash = make_hash_blake2b(pathlib.Path(infile['file-name']))

                if thehash == infile['hash']:
                    print('good hash for file: {}'.format(infile['file-name']))
                else:
                    print('bad hash for file: {}'.format(infile['file-name']))

            else:
                print('this script uses blake2b not {}'
                      .format(infile['hash-algo']))

    else:
        print('input error')


def write_files_current_hash(inpath):
    """Compute and write files current hash."""
    if (inpath.exists() and inpath.is_file()):
        if len(inpath.suffixes) == 1:

            outpath = pathlib.Path(str(inpath) + '.hash.json')

            out = outpath.open(mode='w')

            thehash = make_hash_blake2b(inpath)

            the_dict = make_dict(inpath, thehash)

            json.dump(the_dict, out, indent=3)

        elif len(inpath.suffixes) > 1:
            if ((inpath.suffixes[-1] == '.json') and
                    (inpath.suffixes[-2] == '.hash')):
                print()

            else:
                outpath = pathlib.Path(str(inpath) + '.hash.json')

                out = outpath.open(mode='w')

                thehash = make_hash_blake2b(inpath)

                the_dict = make_dict(inpath, thehash)

            json.dump(the_dict, out, indent=3)

    elif (inpath.exists() and inpath.is_dir()):

        file_list = inpath.glob('*')

        for files in file_list:
            if len(files.suffixes) == 1:
                outpath = pathlib.Path(str(files) + '.hash.json')

                out = outpath.open(mode='w')

                thehash = make_hash_blake2b(files)

                the_dict = make_dict(inpath, thehash)

                json.dump(the_dict, out, indent=3)

            elif len(files.suffixes) > 1:
                if ((files.suffixes[-1] != '.json') and
                        (files.suffixes[-2] != '.hash')):
                    outpath = pathlib.Path(str(files) + '.hash.json')

                    out = outpath.open(mode='w')

                    thehash = make_hash_blake2b(files)

                    the_dict = make_dict(inpath, thehash)

                    json.dump(the_dict, out, indent=3)

    else:
        print('input error')


def make_dict(inpath, thehash):
    """Make the dict that will be turned into JSON."""
    the_dict = {
        'file-name': str(inpath.name),
        'file-size': {
            'value': format(inpath.stat().st_size, '_d'),
            'unit': 'bytes',
            },
        'hash-algo': HASHALGO,
        'hash': thehash,
    }
    return the_dict

def main(args):
    """The main func."""
    if len(args) == 3:
        inpath = pathlib.Path(args[2]).resolve()
        os.chdir(inpath.parent)

        if args[1] == 'make':
            write_files_current_hash(inpath)

        elif args[1] == 'check':
            check_hash(inpath)

        else:
            print('First arg needs to be check or make. Second arg file or dir to work on.')
            sys.exit()
    else:
        print('First arg needs to be check or make. Second arg file or dir to work on.')
        sys.exit()
