import adafruit_dotstar # The LED library
import adafruit_fancyled.adafruit_fancyled as fancy
import math
import time
import board
import digitalio
from analogio import AnalogIn

# Setting up the board's blue stat LED, mostly for testing
led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT

# Here we'll define the inputs/values for HSV
SATpot = AnalogIn(board.A3)
HUEpot = AnalogIn(board.A4)
VALval = 0.4 # Set the initial value for Value, since it's button-driven

# Setting up the digital IO pins as input buttons
button8 = digitalio.DigitalInOut(board.D8)
button8.direction = digitalio.Direction.INPUT
button8.pull = digitalio.Pull.UP

button9 = digitalio.DigitalInOut(board.D9)
button9.direction = digitalio.Direction.INPUT
button9.pull = digitalio.Pull.UP

# These two variables should be adjusted to reflect the number of LEDs you have
# and how bright you want them.
num_pixels = 40 #The 3" ring has 60, the 2" ring has 40, the 1" ring has 20
brightness = 0.5 #Set between 0.0 and 1.0, but suggest never running at full brightness
startSequence = 0 # Last minute addition to create startup sequence

# Some standard colors.
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
ORANGE = (255, 40, 0)
GREEN = (0, 255, 0)
TEAL = (0, 255, 120)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
MAGENTA = (255, 0, 20)
WHITE = (255, 255, 255)

# This creates the instance of the DoTStar library.
pixels = adafruit_dotstar.DotStar(board.SCK, board.MOSI,
    num_pixels, brightness= brightness, auto_write=False)

# The travel function takes a color and the time between updating the color. It
# will start at LED one on the strand and fill it with the give color until it
# reaches the maximum number of pixels that are defined as "num_pixels".
def travel(color, wait):
    num_pixels = len(pixels)
    for pos in range(num_pixels):
        pixels[pos] = color
        pixels.show()
        time.sleep(wait)

def slice_rainbow(wait): # Just a little startup color animation

    num_pixels = len(pixels)

    pixels[::6] = [RED] * math.ceil(num_pixels / 6)
    pixels.show()
    time.sleep(wait)
    pixels[1::6] = [ORANGE] * math.ceil((num_pixels - 1) / 6)
    pixels.show()
    time.sleep(wait)
    pixels[2::6] = [YELLOW] * math.ceil((num_pixels -2) / 6)
    pixels.show()
    time.sleep(wait)
    pixels[3::6] = [GREEN] * math.ceil((num_pixels-3) / 6)
    pixels.show()
    time.sleep(wait)
    pixels[4::6] = [BLUE] * math.ceil((num_pixels-4) / 6)
    pixels.show()
    time.sleep(wait)
    pixels[5::6] = [PURPLE] * math.ceil((num_pixels-5) / 6)
    pixels.show()
    time.sleep(wait)

# Here's where the action happens
while True:
    if startSequence == 0: # Startup with a quick color animation
        slice_rainbow(0.2)
        time.sleep(0.1)
        travel(BLACK,0)
        time.sleep(0.5)
    startSequence = 1 # Stops opening sequence from continuing to run

    if not button8.value: # Increases the Value in increments of 0.05
        VALval = round(VALval + 0.05, 2)
        if VALval > 0.8:
            VALval = 0.8 # Limit Value (brightness) to 0.8 to avoid meltdown
        time.sleep(0.05) # Debounce
    elif not button9.value:
        VALval = round(VALval - 0.05, 2)
        if VALval < 0:
            VALval = 0
        time.sleep(0.05) # Debounce

    print ("Value value = ", VALval)
    TRYME = fancy.CHSV(HUEpot.value / 65535, SATpot.value / 65535, VALval)
    packed = TRYME.pack() # Converts HSV into HEX

    pixels.fill(packed) # Sets color to given HEX value
    pixels.show() # Illuminates LEDs

    time.sleep(0.01) # Debounce