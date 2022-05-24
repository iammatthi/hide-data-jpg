import argparse
from os import path

import rsa
from cryptography.fernet import Fernet

jpg_delimiter = bytes.fromhex('FFD9')

private_asymmetric_key_file = "private_asymmetric.key"
public_asymmetric_key_file = "public_asymmetric.key"


def hide(image, image_out, data):
    # Read input image
    with open(image, 'rb') as fin:
        image_data = fin.read()
        offset = image_data.index(jpg_delimiter)

    # Generate image with data
    with open(image_out, 'wb+') as fout:
        fout.write(image_data[:offset + len(jpg_delimiter)])
        fout.write(data)


def extract(image):
    # Read data from image
    with open(image, 'rb') as fin:
        image_data = fin.read()
        offset = image_data.index(jpg_delimiter)
        fin.seek(offset + len(jpg_delimiter))
        return fin.read()


def main():
    parser = argparse.ArgumentParser()
    action_subparser = parser.add_subparsers(dest='action', required=True)

    encrypt = action_subparser.add_parser('enc')
    encrypt.add_argument('-k', '--symmetric-key',
                         type=str, default="symmetric.key")
    encrypt.add_argument('-i', '--image', type=str, required=True)
    encrypt.add_argument('-o', '--image-out', type=str, required=True)
    encryption_data = encrypt.add_mutually_exclusive_group(required=True)
    encryption_data.add_argument('--file', type=str)
    encryption_data.add_argument('--text', type=str)

    decrypt = action_subparser.add_parser('dec')
    decrypt.add_argument('-k', '--symmetric-key',
                         type=str, default="symmetric.key")
    decrypt.add_argument('-i', '--image', type=str, required=True)
    decrypt.add_argument('--file', type=str)

    keys = action_subparser.add_parser('keys')
    keys.add_argument('-k', '--symmetric-key',
                      type=str, default="symmetric.key")
    # FIXME: --image and --image-out should be required when --symmetric-key-image is not specified
    keys.add_argument('-i', '--image', type=str)
    keys.add_argument('-o', '--image-out', type=str)
    key_image = keys.add_mutually_exclusive_group()
    key_image.add_argument('-p', '--public-key-image', type=str)
    key_image.add_argument('-s', '--symmetric-key-image', type=str)

    args = parser.parse_args()
    if args.action == 'keys':
        if args.public_key_image:
            # Public key image received -> Generate symmetric key image

            # Read public key from image
            public_key = rsa.PublicKey.load_pkcs1(
                extract(args.public_key_image))

            if path.exists(args.symmetric_key):
                # Read symmetric key from file
                with open(args.symmetric_key, "rb") as fin:
                    key = fin.read()
            else:
                # Generate symmetric key
                key = Fernet.generate_key()
                # Save symmetric key
                with open(args.symmetric_key, "wb+") as fout:
                    fout.write(key)

            data = rsa.encrypt(key, public_key)
            hide(args.image, args.image_out, data)
            print("Symmetric key image generated:", args.image_out)

        elif args.symmetric_key_image:
            # Symmetric key image received -> Save it to file

            if path.exists(private_asymmetric_key_file) and path.exists(public_asymmetric_key_file):
                # Read public key from file
                with open(private_asymmetric_key_file, "rb") as fin:
                    private_key = rsa.PrivateKey.load_pkcs1(fin.read())
            else:
                print("Asymmetric keys not found")
                exit(1)

            # Read symmetric key from image
            data = extract(args.symmetric_key_image)
            key = rsa.decrypt(data, private_key)
            # Save symmetric key
            with open(args.symmetric_key, "wb+") as fout:
                fout.write(key)

            print("Symmetric key saved:", args.symmetric_key)

        else:
            # Generate public key image

            if path.exists(private_asymmetric_key_file) and path.exists(public_asymmetric_key_file):
                # Read public key from file
                with open(public_asymmetric_key_file, "rb") as fin:
                    public_key = rsa.PublicKey.load_pkcs1(fin.read())
            else:
                # Generate asymmetric keys
                public_key, private_key = rsa.newkeys(2048)
                # Save private key
                with open(public_asymmetric_key_file, "wb+") as fin:
                    fin.write(public_key.save_pkcs1())
                    print(public_asymmetric_key_file + " generated")
                # Save public key
                with open(private_asymmetric_key_file, "wb+") as fin:
                    fin.write(private_key.save_pkcs1())
                    print(private_asymmetric_key_file + " generated")

            data = public_key.save_pkcs1()
            hide(args.image, args.image_out, data)
            print("Public key image generated:", args.image_out)

    elif args.action == 'enc':
        if path.exists(args.symmetric_key):
            # Read symmetric key from file
            with open(args.symmetric_key, "rb") as fin:
                key = fin.read()
        else:
            print("Symmetric key not found")
            exit(1)

        if args.file:
            with open(args.file, 'rb') as f:
                data = f.read()
        elif args.text:
            data = args.text.encode()
        else:
            raise Exception("Encrytion data not found")

        f = Fernet(key)
        encrypted_data = f.encrypt(data)
        hide(args.image, args.image_out, encrypted_data)
        print("Image generated:", args.image_out)

    elif args.action == 'dec':
        if path.exists(args.symmetric_key):
            # Read symmetric key from file
            with open(args.symmetric_key, "rb") as fin:
                key = fin.read()
        else:
            print("Symmetric key not found")
            exit(1)

        encrypted_data = extract(args.image)
        f = Fernet(key)
        data = f.decrypt(encrypted_data)

        if args.file:
            with open(args.file, 'wb') as fout:
                fout.write(data)
                print("File extracted:", args.file)
        else:
            print("Hidden text: " + data.decode('utf-8'))


if __name__ == '__main__':
    main()
