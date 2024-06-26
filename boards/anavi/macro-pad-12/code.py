import board

from kmk.extensions.display import Display, TextEntry
from kmk.extensions.display.ssd1306 import SSD1306
from kmk.extensions.LED import LED
from kmk.extensions.media_keys import MediaKeys
from kmk.extensions.RGB import RGB, AnimationModes
from kmk.keys import KC
from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners import DiodeOrientation

keyboard = KMKKeyboard()

# I2C pins for the mini OLED display
keyboard.SCL = board.D5
keyboard.SDA = board.D4

display = Display(
    display=SSD1306(sda=board.D4, scl=board.D5),
    entries=[
        TextEntry(text='ANAVI Macro Pad 12'),
    ],
    height=64,
)
keyboard.extensions.append(display)

led = LED(
    led_pin=[
        board.D0,
    ],
    brightness=100,
    brightness_step=5,
    brightness_limit=100,
    breathe_center=1.5,
    animation_mode=AnimationModes.STATIC,
    animation_speed=1,
    user_animation=None,
    val=100,
)
keyboard.extensions.append(led)

# WS2812B LED strips on the back
underglow = RGB(
    pixel_pin=board.D10,
    num_pixels=6,
    val_limit=100,
    val_default=25,
    animation_mode=AnimationModes.RAINBOW,
)
keyboard.extensions.append(underglow)

# Neopixel on XIAO RP2040
frontglow = RGB(
    pixel_pin=board.NEOPIXEL,
    num_pixels=1,
    val_limit=100,
    val_default=25,
    animation_mode=AnimationModes.RAINBOW,
)
keyboard.extensions.append(frontglow)

keyboard.col_pins = (board.D6, board.D8, board.D9)
keyboard.row_pins = (board.D1, board.D2, board.D3, board.D7)
keyboard.diode_orientation = DiodeOrientation.COL2ROW

media_keys = MediaKeys()
keyboard.extensions.append(media_keys)

# Matrix 4x3 keymap, 12 keys in total
keyboard.keymap = [
    [
        KC.N1,
        KC.N2,
        KC.N3,
        KC.N4,
        KC.N5,
        KC.N6,
        KC.N7,
        KC.N8,
        KC.N9,
        KC.N0,
        KC.A,
        KC.B,
    ]
]

if __name__ == '__main__':
    keyboard.go()
