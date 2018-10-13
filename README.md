# Pyink

### Adds hardware support to Satoshi-Pi box 

> *"No payment is too small to be irrelephant" 🐘*


Planned support:
* e-ink HAT
* Buttons
* Menus
* QR codes
* character display
* status LED support

Installation
---
Pyink is not meant to be run directly by users.
Install [Satoshi-Pi](https://github.com/lncm/Satoshi-Pi) to build your own box.

Development
---

```
# Install dependencies
curl -sS https://raw.githubusercontent.com/lncm/Satoshi-Pi/master/install.sh | bash
git clone git@github.com:lncm/pyink.git
cd pyink
python main.py
```

Requirements
---
* Fresh [Raspbian](https://www.raspberrypi.org/downloads/raspbian/) Stretch Lite [installation](https://www.raspberrypi.org/documentation/installation/installing-images/README.md)
* Raspberry Pi (or compatible)

Optional hardware add-ons:
* [2.7" e-Paper HAT](https://www.waveshare.com/product/2.7inch-e-paper-hat-b.htm) from Waveshare
* HD47780 compatible character display (i2c or parallel with logic converter)
* buttons (GPIO)
* LEDs and appropriate resistors


Contributions
---
All contributions are welcome.

Feel free to get in touch!

---

Made with 🥩 in Chiang Mai