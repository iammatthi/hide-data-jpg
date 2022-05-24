import argparse

parser = argparse.ArgumentParser()
action_subparser = parser.add_subparsers(dest='action', required=True)

encrypt = action_subparser.add_parser('enc')
encrypt.add_argument('--src', type=str, required=True)
encrypt.add_argument('--out', type=str, required=True)
group = encrypt.add_mutually_exclusive_group(required=True)
group.add_argument('--file', type=str)
group.add_argument('--text', type=str)

decrypt = action_subparser.add_parser('dec')
decrypt.add_argument('--src', type=str, required=True)
decrypt.add_argument('--file', type=str)

delimiter = bytes.fromhex('FFD9')

args = parser.parse_args()
if args.action == 'enc':
    with open(args.src, 'rb') as fin:
        data = fin.read()
        offset = data.index(delimiter)

        with open(args.out, 'wb') as fout:
            fout.write(data[:offset + len(delimiter)])

            if args.file:
                with open(args.file, 'rb') as f:
                    fout.write(f.read())
            elif args.text:
                fout.write(bytes(args.text, 'utf-8'))

            print("File encrypted")

elif args.action == 'dec':
    with open(args.src, 'rb') as fin:
        data = fin.read()
        offset = data.index(delimiter)
        fin.seek(offset + len(delimiter))

        if args.file:
            with open(args.file, 'wb') as fout:
                fout.write(fin.read())
                print("File decrypted")
        else:
            print("Hidden text: " + fin.read().decode('utf-8'))
