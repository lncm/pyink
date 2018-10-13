# For python3 semantics
from __future__ import print_function
import draw
import epd2in7b
import time
import buttons

# TODO: Use venv to keep packages contained

epd = epd2in7b.EPD()
epd.init()

# Time it takes to print both logo layers
# print('sleeping for 16 seconds')
# time.sleep(16)


epd.init()
draw.logo()
epd.sleep()

buttons.menu()