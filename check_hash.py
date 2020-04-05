import sys
import pathlib
import hashlib
import json

inpath = pathlib.Path(sys.argv[1]).resolve()

hashalgo = 'blake2b'


def make_hash_blake2b(inpath):
    # refrence
    # https://stackoverflow.com/questions/22058048/hashing-a-file-in-python

    # BUF_SIZE is totally arbitrary, change for your app!
    BUF_SIZE = 65536  # lets read stuff in 64kb chunks!

    thehash = hashlib.blake2b()

    with open(inpath, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            thehash.update(data)

    return thehash.hexdigest()


if (inpath.exists() and inpath.is_file() and
        (inpath.suffixes[-1] == '.json') and
        (inpath.suffixes[-2] == '.hash')):

    infile = json.load(inpath.open(mode='r'))

    if infile['hash-algo'] == hashalgo:
        thehash = make_hash_blake2b(pathlib.Path(infile['file-name']))

        if thehash == infile['hash']:
            print('good hash for file: {}'.format(infile['file-name']))
        else:
            print('bad hash for file: {}'.format(infile['file-name']))
    else:
        print('this script uses blake2b not {}'.format(infile['hash-algo']))

elif (inpath.exists() and inpath.is_dir()):

    file_list = inpath.glob('*.hash.json')

    for f in file_list:

        infile = json.load(f.open(mode='r'))

        if infile['hash-algo'] == hashalgo:
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
