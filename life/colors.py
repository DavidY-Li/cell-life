import colorsys

# Colors
black = [0, 0, 0]
white = [255, 255, 255]
red = [255, 0, 0]
light_red = [200, 10, 10]
grey = [200, 200, 200]
blue = [0, 30, 200]
light_blue = [0, 40, 255]
green = [0, 255, 0]
dark_grey = [128, 128, 128]

# Converts HSV to RGB value
def hsv_to_rgb(h, s, v):
    return tuple(round(value * 255) for value in colorsys.hsv_to_rgb(h, s, v))


# Converts RGB to HSV value
def rgb_to_hsv(r, g, b):
    return tuple(value for value in colorsys.rgb_to_hsv(r / 255, g / 255, b / 255))