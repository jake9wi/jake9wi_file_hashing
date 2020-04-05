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


if (inpath.exists() and inpath.is_file()):
    if len(inpath.suffixes) == 1:

        outpath = pathlib.Path(str(inpath) + '.hash.json')

        out = outpath.open(mode='w')

        thehash = make_hash_blake2b(inpath)

        x = {
            'file-name': str(inpath.name),
            'file-size': {
                        'value': format(inpath.stat().st_size, '_d'),
                        'unit': 'bytes'
                        },
            'hash-algo': hashalgo,
            'hash': thehash
            }

        json.dump(x, out, indent=3)

    elif len(inpath.suffixes) > 1:
        if ((inpath.suffixes[-1] == '.json') and
                (inpath.suffixes[-2] == '.hash')):
            print()

        else:
            outpath = pathlib.Path(str(inpath) + '.hash.json')

            out = outpath.open(mode='w')

            thehash = make_hash_blake2b(inpath)

            x = {
                'file-name': str(inpath.name),
                'file-size': {
                            'value': format(inpath.stat().st_size, '_d'),
                            'unit': 'bytes'
                },
                'hash-algo': hashalgo,
                'hash': thehash
                }

            json.dump(x, out, indent=3)


elif (inpath.exists() and inpath.is_dir()):

    file_list = inpath.glob('*')

    for f in file_list:
        if len(f.suffixes) == 1:
            outpath = pathlib.Path(str(f) + '.hash.json')

            out = outpath.open(mode='w')

            thehash = make_hash_blake2b(f)

            x = {
                'file-name': str(f.name),
                'file-size': {
                        'value': format(inpath.stat().st_size, '_d'),
                        'unit': 'bytes'
                },
                'hash-algo': hashalgo,
                'hash': thehash
            }

            json.dump(x, out, indent=3)

        elif len(f.suffixes) > 1:
            if ((f.suffixes[-1] == '.json') and (f.suffixes[-2] == '.hash')):
                break

            else:
                outpath = pathlib.Path(str(f) + '.hash.json')

                out = outpath.open(mode='w')

                thehash = make_hash_blake2b(f)

                x = {
                    'file-name': str(f.name),
                    'file-size': {
                        'value': format(inpath.stat().st_size, '_d'),
                        'unit': 'bytes'
                    },
                    'hash-algo': hashalgo,
                    'hash': thehash
                }

                json.dump(x, out, indent=3)

else:
    print('input error')
