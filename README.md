<!-- GETTING STARTED -->

## Getting Started

To get a local copy up and running follow these simple example steps.

### Prerequisites

- python 3
- pip3

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/iammatthi/hide-data-jpg
   ```
2. Install python packages
   ```sh
   pip3 install -r requirements.txt
   ```

<!-- USAGE EXAMPLES -->

## Usage

```sh
# image.jpg is an image on the disk

# Client 1
# Generate RSA 2048 bit key pair and generate an image with the public key hidden (pub.jpg)
python3 main.py keys -i image.jpg -o pub.jpg

# Client 2
# Generate Fernet key, encrypt it with the public key received in the image (pub.jpg) and generate 
# image (sym.jpg) with this encrypted key
python3 main.py keys -p pub.jpg -i image.jpg -o sym.jpg

# Client 1
# Extract Fernet key from image (sym.jpg) and save it to disk
python3 main.py keys -s sym.jpg
# Create image with hidden data (hidden.jpg)
python3 main.py enc -i image.jpg -o hidden.jpg --text "Come stai?"

# Client 2
# Read hidden data from image (hidden.jpg)
python3 main.py dec -i hidden.jpg
```

## How it works?
Given that a JPG file ends with the `0xffd9` sequence, hidden data can be inserted after it (in the example is on row `00002280`).
```sh
> xxd hidden.jpg
00000000: ffd8 ffe0 0010 4a46 4946 0001 0100 0001  ......JFIF......
00000010: 0001 0000 ffe2 0228 4943 435f 5052 4f46  .......(ICC_PROF
00000020: 494c 4500 0101 0000 0218 0000 0000 0430  ILE............0
00000030: 0000 6d6e 7472 5247 4220 5859 5a20 0000  ..mntrRGB XYZ ..
00000040: 0000 0000 0000 0000 0000 6163 7370 0000  ..........acsp..
...
00002260: 8808 8880 8888 0888 8088 8808 8880 8888  ................
00002270: 0888 8088 8808 8880 8888 0888 8088 8808  ................
00002280: 8883 ffd9 6741 4141 4141 4269 6a51 4d43  ....gAAAAABijQMC
00002290: 5674 6f4e 766c 6c6a 4e6a 4256 4d64 5275  VtoNvlljNjBVMdRu
000022a0: 6644 7972 6569 4c67 4b6d 366f 3879 6164  fDyreiLgKm6o8yad
000022b0: 5847 3547 2d37 6b46 716a 2d53 4434 355a  XG5G-7kFqj-SD45Z
000022c0: 7573 644b 5742 7a49 724f 4863 6b78 4a62  usdKWBzIrOHckxJb
000022d0: 6f59 414e 6c4a 617a 6173 4135 5778 7547  oYANlJazasA5WxuG
000022e0: 396a 3561 7a51 3d3d                      9j5azQ==
```

To improve security, the hidden data is encrypted by using Fernet symmetric encryption.

The symmetric key used by such algorithm can be shared by using RSA 2048 bit asymmetric encryption as shown in the example in the _Usage_ section.



