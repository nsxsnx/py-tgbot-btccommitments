#!/usr/bin/python3
from SETTINGS import *
from PIL import Image, ImageDraw, ImageFont
import urllib.request, re, telebot, pickle

def die(message):
    print(message)
    exit(1)

def create_image(name, text):
    img = Image.new('RGB', (710, 540), color = (73, 109, 137))
    #fnt = ImageFont.truetype('/usr/share/fonts/truetype/msttcorefonts/arial.ttf', 12)
    d = ImageDraw.Draw(img)
    d.text((10,10), text, fill=(255,255,255))
    img.save(name)

def checkdate(data):
    res = re.search(RE_DATE, data)
    if res is None: die('Date parse error\r\n')
    newdate = res.group(1).strip()
    try: 
        olddate = pickle.load(open(STATE_FILE, "rb"))
        if olddate == newdate: return 1
    except: pass #First run
    with open(STATE_FILE, "wb") as fw: pickle.dump(newdate, fw)
    return 0

# Entry point
tb = telebot.TeleBot(TELEGRAM_TOKEN)
c = 1
for url in [CME_LINK, CBOE_LINK]:
    f = urllib.request.urlopen(url)
    result = re.search(RE, f.read().decode('utf-8'), flags=re.DOTALL )
    if result is None: die('Url parse error\r\n')
    if c==1 and checkdate(result.group(1)): exit(0)
    create_image('/tmp/image{}.png'.format(c), result.group(1))
    photo = open('/tmp/image{}.png'.format(c), 'rb')
    try: tb.send_photo(TELEGRAM_CHANNEL, photo)
    except: die('Could not send message to bot')
    c+=1

