import RPi.GPIO as GPIO
import time
import os.path
import draw
import epd2in7b
import requests
from PIL import Image
from button_handler import ButtonHandler

epd = epd2in7b.EPD()

username = 'raspberry'
password = 'raspberry'
invoicer_url = '127.0.0.1'
invoicer_port = '1666'


above = (20,20)
below = (64,244)
png_path = 'png'

# BCM pin numbering scheme
KEY1 = 5
KEY2 = 6
KEY3 = 13
KEY4 = 19



key_list = [KEY1, KEY2, KEY3, KEY4]


items = [
        [{"name": "steak"}, {"amount": 50000}],
        [{"name": "beer"}, {"amount": 25000}],
        [{"name": "t-shirt"}, {"amount": 100000}],
]

num_items = len(items)
print(num_items)
item = None
selected = False


def key_press(key_num):
    global item, selected

    print('Rising GPIO input detected on BCM pin %s' % key_num)

    if key_num == KEY1:
        print('"Previous" button pressed')
        if not selected:
            print(item)
            item = previous_item(item)
            print(item)
            print('Rendering %s' % items[item][0]["name"])
            render(item, items[item][1]["amount"])

    elif key_num == KEY2:
        print('"Next" button pressed')
        if not selected:
            item = next_item(item)
            print('Rendering %s' % items[item][0]["name"])
            render(item, items[item][1]["amount"])

    elif key_num == KEY3:
        print("Select button pressed")
        selected = not selected
        print("Select mode: %s" % selected)
        if selected:
            epd.init()
            req = get_invoice(items[item][1]["amount"], items[item][0]["name"])
            invoice = req[0].encode('ascii','ignore')
            invoice = "LIGHTNING:" + str.upper(invoice)
            print(invoice)
            img = draw.qr(invoice)
            img = draw.expand(img, (176, 264))
            draw.img(img)
            epd.sleep()
        else:
            print('Rendering %s' % items[item][0]["name"])
            render(item, items[item][1]["amount"])

    elif key_num == KEY4:
        print("QR button pressed")
        connstring = get_connstring()[0]
        ascii = connstring.encode('ascii','ignore')
        upper = str.upper(str(ascii))
        print(str(upper))
        epd.init()
        img = draw.qr(upper)
        img = draw.expand(img, (176, 264))
        img = draw.text(img, 'connstring', (20, 20))
        draw.img(img)
        epd.sleep()

    else:
        print("Unknown button pressed")


def get_connstring():
    response = requests.get('http://' + invoicer_url + ':' + invoicer_port + '/connstrings/',
                            auth=(username, password))
    return response.json()


def get_status(hash):
    response = requests.get('http://' + invoicer_url + ':' + invoicer_port + '/status/' + hash,
                            auth=(username, password))
    return response.json()


def get_invoice(amount, desc, expire=180):
    response = requests.get('http://' + invoicer_url + ':' + invoicer_port + '/invoice?amount=' + str(amount)
                            + '&desc=' + str(desc) + '&expire=' + str(expire),
                            auth=(username, password))
    invoice = response.json()['invoice']
    hash = response.json()['hash']
    return invoice, hash


def next_item(item=item, num_items=num_items):
    if item == None:
        return 0
    elif item != num_items - 1:
        item += 1
        return item
    else:
        return 0


def previous_item(item=item, num_items=num_items):
    if item == None:
        return 0
    if item == 0:
        return num_items -1
    else:
        item -= 1
        return item


def make_path(item_name, color):
    if color != 'black' and color != 'red':
        color = 'black'
    path = png_path + '/' + item_name + '_' + color + '.png'
    return path


def render(item, amount):
    item_name = items[item][0]["name"]
    black_exists = None
    red_exists = None
    black_path = make_path(item_name, 'black')
    red_path = make_path(item_name, 'red')
    black_exists = os.path.isfile(black_path)
    red_exists = os.path.isfile(red_path)

    epd.init()

    img = Image.open(black_path)
    img = draw.text(img, str(amount), above)

    if black_exists and red_exists:
        draw.img(img, Image.open(red_path))
    elif black_exists:
        draw.img(img, None)
    elif red_exists:
        draw.img(None, Image.open(red_path))
    epd.sleep()


def bits_to_msat(bits):
    return bits * 100


def menu():
    # BCM pin numbering scheme
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(key_list, GPIO.IN, GPIO.PUD_UP)

    # Switch debouncing ignores further edges for bouncetime in milliseconds
    cb1 = ButtonHandler(KEY1, key_press, edge='falling', bouncetime=50)
    cb2 = ButtonHandler(KEY2, key_press, edge='falling', bouncetime=50)
    cb3 = ButtonHandler(KEY3, key_press, edge='falling', bouncetime=50)
    cb4 = ButtonHandler(KEY4, key_press, edge='falling', bouncetime=50)

    cb1.start()
    cb2.start()
    cb3.start()
    cb4.start()

    GPIO.add_event_detect(KEY1, GPIO.BOTH, callback=cb1)
    GPIO.add_event_detect(KEY2, GPIO.BOTH, callback=cb2)
    GPIO.add_event_detect(KEY3, GPIO.BOTH, callback=cb3)
    GPIO.add_event_detect(KEY4, GPIO.BOTH, callback=cb4)

    # keep running
    while True:
        time.sleep(1)

