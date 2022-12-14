import time
from rpi_ws281x import *
import argparse
from PIL import Image
import os

LED_COUNT      = 100      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 50     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

class Pixel:
    def __init__(self):
        self.color = Color(0,0,0)

    def setColor(self, new_color):
        self.color = new_color

    def getColor(self):
        return self.color

class Frame:
    def __init__(self):
        self.matrix = []
        for row in range(10):
            row = []
            for col in range(10):
                row.append(Pixel())
            self.matrix.append(row)

    def setPixel(self, row, col, color):
        #update('Setting pixel color inside frame..')
        self.matrix[row][col].setColor(color)
        #update('New pixel value: ' + str(self.matrix[row][col].getColor()))

    def getPixel(self, row, col):
        return self.matrix[row][col]
    
    def update(self, strip):
        #update('frame is updating the strip')
        for row in range(10):
            for col in range(10):
                strip.setPixelColor((row*10) + col, self.matrix[row][col].getColor())
        return strip

# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def firstTest(frame, i):
    #update('frame value -> ' + str(frame))
    #update('calling firstTest which should update pixels in frame')
    for row in range(10):
        for col in range(10):
            frame.setPixel(row, col, Color(i, 0, 0))

def showImage(frame, strip, image_path):
    #print('showimage called')

    img = Image.open(f'{image_path}')
    img = img.convert('RGB')

    for row in range(10):
        for col in range(10):
            # get the RGB values of the current pixel
            r, g, b = img.getpixel((col, row))
            frame.setPixel(row, col, Color(r, g, b))

    strip = frame.update(strip)
    strip.show()

def showGif(frame, strip, foldername, interval):
    n_files = len([name for name in os.listdir(f'gifs/{foldername}') if os.path.isfile(f'gifs/{foldername}/{name}')])

    for i in range(n_files):
        showImage(frame, strip, f'gifs/{foldername}/{i}.png')
        time.sleep(interval)

def mainLoop(frame, strip, i):
    # clear all pixels
    #update('mainloop: clearning pixels..\nframe value -> ' + str(frame))
    #colorWipe(strip, Color(0,0,0), 10)

    while True:
        showGif(frame, strip, 'fractal2', 0.1)
        #showImage(frame, strip, 'images/heart1.png')
    #firstTest(frame, i)


def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i+j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def rainbowCycle(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, wheel((i+j) % 255))
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

def test(strip):
    for i in range(10):
        strip.setPixelColor(i, Color(0,0,0))
        strip.setPixelColor(1+i, Color(255,255,0))
        strip.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()

    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    try:

        frame = Frame()
        i = 1

        while True:
        
            mainLoop(frame, strip, i)
            
            break
         


    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0,0,0), 10)
