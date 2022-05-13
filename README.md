# text-to-midi
Convert images to music

# Features
Extract the edges of the image to generate MIDI art.

# Requirement
python 3.8.x ~ 3.10.x

# Installation
```bash
git clone https://github.com/gongitsune/text-to-midi.git
cd text-to-midi
python -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
```

# Usage
```bash
python src/scraping_chords.py
python src/midi.py [target image path]
```

Please listen as it will be generated in the dist folder.
