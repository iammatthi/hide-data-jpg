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
# Generate public key image (pub.jpg)
python3 main.py keys -i image.jpg -o pub.jpg

# Client 2
# Generate symmetric key image (sym.jpg) from public key image (pub.jpg)
python3 main.py keys -p pub.jpg -i image.jpg -o sym.jpg

# Client 1
# Extract symmetric key from image (sym.jpg) and save it to disk
python3 main.py keys -s sym.jpg
# Create image with hidden data (hidden.jpg)
python3 main.py enc -i image.jpg -o hidden.jpg --text "Come stai?"

# Client 2
# Read hidden data from image (hidden.jpg)
python3 main.py dec -i hidden.jpg
```
