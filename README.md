<!-- PROJECT LOGO -->
<br />
<div align="center">
  <h3 align="center">hide-data-jpg</h3>

  <p align="center">
    Hide data safely in a JPG image.
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#how-it-works">How It Works?</a></li>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About the project

This project aims to use steganography to allow communication between two users to be hidden using JPG images.

### How It Works?

Since a JPG file ends with the sequence `0xffd9`, hidden data can be inserted after it (in the example, the jpg delimiter is on line `00002280`).

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

To improve security, data is encrypted using Fernet symmetric encryption.

The symmetric key used by this algorithm can be shared using 2048-bit RSA asymmetric encryption, as shown in the example in the _Usage_ section.

### Built With

- [Python](https://www.python.org/)

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
python3 app.py keys --image image.jpg --image-out pub.jpg

# Client 2
# Generate Fernet key, encrypt it with the public key received in the image (pub.jpg) and generate
# image (sym.jpg) with this encrypted key
python3 app.py keys --public-key-image pub.jpg --image image.jpg --image-out sym.jpg

# Client 1
# Extract Fernet key from image (sym.jpg) and save it to disk
python3 app.py keys --symmetric-key-image sym.jpg
# Create image with hidden data (hidden.jpg)
python3 app.py hide --image image.jpg --image-out hidden.jpg --text "Hi! How are you?"

# Client 2
# Read hidden data from image (hidden.jpg)
python3 app.py extract --image hidden.jpg
```
