"""
RGBShield - generic neopixels strip or shield, using class NeoPixel
RGB8x8Shield - Lolin 8*8 RGB shield, using class APA106
2022-1223 PP new , tested with Lolin 8*8 RGB shield
"""
from machine import Pin
import time


# colors - already reduced in intensity
RED   = (55, 0, 0)
GREEN = (0, 55, 0)
BLUE  = (0, 0, 55)
BLACK = (0, 0, 0)
WHITE = (55, 55, 55)

# Base class
class RGBShield():
    # init: DIN and number of pixels
    def __init__(self, din, n):
        """ __init__() - setup Neopixels at DIN and number of nexopixels
            din : pinnumber of DIN
            n   : number of neopixels
        """
        from neopixel import NeoPixel
        self._leds = NeoPixel(Pin(din, Pin.OUT), n)

    # TODO: get decorator
    # return number of neopixels
    def np(self):
        return self._leds.n

	# clear all neopixels
    def clear(self):
        self._leds.fill(BLACK)
        self._leds.write()


	# common running led helper method
    def _running(self, start, stop, step=1, color=BLACK, dt=0.02):
        for i in range(start, stop, step):
            self._leds[i] = color
            self._leds.write()
            time.sleep(dt)


	# fills RGB shield one-by-one in color
    def running_up(self, color):
        self._running(0, self.np(), 1, color)


	# clears RGB shield one-by-one in color
    def running_down(self, color):
        self._running(self.np()-1, -1, -1, color)


	# demo - several patterns
    def demo(self, cycle_color=WHITE, bounce_color=RED, fade_color=GREEN):
        n = self.np()
        print(f"pixels: {n}")
        np = self._leds

        # cycle
        cycles = 2  # 4
        print(f"cycle... {cycles}x")
        #for i in range(4 * n):
        for i in range(cycles * n):
            for j in range(n):
                np[j] = BLACK
            np[i % n] = cycle_color
            np.write()
            time.sleep_ms(25)

        # bounce
        print(f"bounce... {cycles}x")
        for i in range(cycles*n):
            for j in range(n):
                np[j] = bounce_color
            if (i // n) % 2 == 0:
                np[i % n] = BLACK
            else:
                np[n - 1 - (i % n)] = BLACK
            np.write()
            time.sleep_ms(60)

        # fade in/out
        cycles = 4 
        print(f"fade in/out... {cycles}x")
        brightness = 0.5
        for i in range(0, cycles*256, 8):
            for j in range(n):
                if (i // 256) % 2 == 0:
                    val = i & 0xff
                else:
                    val = 255 - (i & 0xff)
                value = int(val * brightness)
                np[j] = tuple(value*x for x in fade_color)
            np.write()


class RGB8x8Shield(RGBShield):
    """
        RGB8x8Shield is class for Lolin 8*8 RGBshield.
        It is using class APA106, that will display correct colors RED and GREEN
    """
    # init: DIN and number of pixels
    def __init__(self, din, n):
        """ __init__() - setup Neopixels at DIN and number of nexopixels
            din : pinnumber of DIN
            n   : number of neopixels
        """
        # 8*8 RGB shield should use APA106 else RED and GREEN are reversed!
        from apa106 import APA106
        self._leds = APA106(Pin(din, Pin.OUT), n)



if __name__ == "__main__":
    try:
        # TODO: test with 7-pixel D1-mini RGB shield
        #DIN = 6   # <== correct DIN?
        #PIXELS = 7  # 7-pixels
        #shield = RGBShield(din=DIN, n=PIXELS)
        
        # Lolin's 8x8 RGB shield: RED and GREEN are reversed
        DIN = 6
        PIXELS = 64
        shield = RGB8x8Shield(din=DIN, n=PIXELS)
        shield.clear()

		# perform the demo in default colors        
        shield.demo()

    except KeyboardInterrupt:        
        print("user interrupt...")
    finally:
        shield.clear()
        print("Done!")
