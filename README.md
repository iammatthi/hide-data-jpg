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
# Client 1
# Generate public key image
python3 main.py keys -i fsociety.jpg -o pub.jpg

# Client 2
# Generate symmetric key image from public key image
python3 main.py keys -p pub.jpg -i fsociety.jpg -o sym.jpg

# Client 1
# Save symmetric key to file
python3 main.py keys -s sym.jpg
# Create image with hidden data
python3 main.py enc -i fsociety.jpg -o hidden.jpg --text "Come stai?"

# Client 2
# Read hidden data from image
python3 main.py dec -i hidden.jpg
```
