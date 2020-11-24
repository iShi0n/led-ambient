from pywinusb import hid
from PIL import Image, ImageGrab
import numpy as np
from time import sleep

def get_dominant_color() -> tuple:
    """https://stackoverflow.com/a/52879133/13030478"""
    img = ImageGrab.grab().convert("RGB")
    w, h = img.size
    pixels = img.getcolors(w * h) # return list((count, (r, g, b)))
    sorted_pixels = reversed(sorted(pixels, key=lambda t: t[0])) # do maior count para o menor
    
    for color in sorted_pixels:
        if any(pixel > 15 for pixel in color[1]):
            r, g, b = color[1] # maior count
            
            r = int(min(255, r*2))
            g = int(min(255, g*2))
            b = int(min(255, b*2))

            dominant_color = r, g, b
            break
    else:
        dominant_color = (0, 0, 0)
    
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
        last_color = (r, g, b)
    
    sleep(0.05)