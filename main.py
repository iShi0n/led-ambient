from pywinusb import hid
from PIL import Image, ImageGrab
import numpy as np

def get_dominant_color() -> tuple:
    img = ImageGrab.grab()
    w, h = img.size
    pixels = img.getcolors(w * h)
    sorted_pixels = sorted(pixels, key=lambda t: t[0])
    dominant_color = sorted_pixels[-1][1]
    print(dominant_color)
    
    return dominant_color

def set_color(r, g, b):
    devices = hid.HidDeviceFilter(vendor_id=0x0c45, product_id=0x5004).get_devices()
    device = devices[2]
    device.open()

    buffer = [0x04, 0x0c, 0x01, 0x06, 0x03, 0x05, 0x00, 0x00]
    buffer += r, g, b
    buffer += [0x00] * 53

    out_report = device.find_output_reports()
    for out in out_report:
        out.send(buffer)
    device.close()

last_color = (-1, -1, -1)

while True:
    r, g, b = get_dominant_color()
    if last_color != (r, g, b):
        set_color(r, g, b)

    
