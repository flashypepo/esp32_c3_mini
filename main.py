"""
main.py - generic startup

2022-1223 PP test: Lolin's 8x8 RGB shield
"""
import time


# Demo of Lolin 8*8 RGBshield
def rgbdemo():
    from rgbshield import RGB8x8Shield

    # colors - full intensity
    RED   = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE  = (0, 0, 255)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    try:
        # Lolin's 8x8 RGB shield, use class RGB8x8Shield
        DIN = 6       # pin D4
        PIXELS = 8*8  # 8x8 neopixels
        shield = RGB8x8Shield(din=DIN, n=PIXELS)

        shield.clear()
        BRIGTHNESS = 0.1   # percentage of full color intensity
        
        # demo of shield
        # from https://docs.micropython.org/en/latest/esp8266/tutorial/neopixel.html
        shield.demo(
            cycle_color=tuple(int(BRIGTHNESS*x) for x in RED),
            bounce_color=tuple(int(BRIGTHNESS*x) for x in BLUE),
            fade_color=tuple(int(BRIGTHNESS*x) for x in GREEN)
        )
        # default color values: shield.demo()

        shield.clear()
        time.sleep(1)
        
        # demo: up and down runner
        color = tuple(int(BRIGTHNESS*x) for x in WHITE)
        print(f"running up ... color={color}")
        shield.running_up(color=color)
        time.sleep(1)

        color = BLACK
        print(f"running down ... color={color}")
        shield.running_down(color=color)
        time.sleep(1)

    except KeyboardInterrupt:        
        print("user interrupt...")
    finally:
        shield.clear()
        print("Done!")



if __name__ == "__main__":
    print("RGB shield demo...")
    rgbdemo()
