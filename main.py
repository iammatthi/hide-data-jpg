import argparse
from os.path import exists

import rsa

jpg_delimiter = bytes.fromhex('FFD9')

parser = argparse.ArgumentParser()
action_subparser = parser.add_subparsers(dest='action', required=True)

encrypt = action_subparser.add_parser('enc')
encrypt.add_argument('--src', type=str, required=True)
encrypt.add_argument('--out', type=str, required=True)
encrypt.add_argument('--publickey', type=str, required=True)
group = encrypt.add_mutually_exclusive_group(required=True)
group.add_argument('--file', type=str)
group.add_argument('--text', type=str)

decrypt = action_subparser.add_parser('dec')
decrypt.add_argument('--src', type=str, required=True)
decrypt.add_argument('--file', type=str)

genkeys = action_subparser.add_parser('genkeys')

file_private_key = "private.key"
file_public_key = "public.key"

args = parser.parse_args()
if args.action == 'enc':
    with open(args.src, 'rb') as fin:
        data = fin.read()
        offset = data.index(jpg_delimiter)

        with open(args.out, 'wb') as fout:
            fout.write(data[:offset + len(jpg_delimiter)])

            with open(args.publickey, "rb") as fout:
                publicKey = rsa.PublicKey.load_pkcs1(fout.read())

            if args.file:
                with open(args.file, 'rb') as f:
                    fout.write(f.read())
            elif args.text:
                data = args.text.encode()
                fout.write(rsa.encrypt(data, publicKey))

            print("JPG generated")

elif args.action == 'dec':
    if exists(file_private_key) and exists(file_public_key):
        with open(file_private_key, "rb") as fout:
            privateKey = rsa.PrivateKey.load_pkcs1(fout.read())
    else:
        print("Personal private key not found")
        exit(1)

    with open(args.src, 'rb') as fin:
        data = fin.read()
        offset = data.index(jpg_delimiter)
        fin.seek(offset + len(jpg_delimiter))

        if args.file:
            with open(args.file, 'wb') as fout:
                fout.write(fin.read())
                print("File extracted")
        else:
            print("Hidden text: " + rsa.decrypt(fin.read(),
                  privateKey).decode('utf-8'))

elif args.action == 'genkeys':
    if exists(file_private_key) and exists(file_public_key):
        print("Keys already exist")
    else:
        publicKey, privateKey = rsa.newkeys(512)
        with open(file_private_key, "w+") as fin:
            fin.write(privateKey.save_pkcs1().decode())

        with open(file_public_key, "w+") as fin:
            fin.write(publicKey.save_pkcs1().decode())

        print("Keys generated")
