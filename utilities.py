import pygame

_image_library = {}
_sound_library = {}
_cached_fonts = {}
_cached_text = {}

counter = {"Moves": 0, "Lives": 0, "Time": 0}

## TIMER ##
def timer(seconds):
    pygame.time.set_timer(pygame.USEREVENT+0, seconds*1000)

## SCREEN ##

def get_dimensions():
    width = pygame.display.Info().current_w
    height = pygame.display.Info().current_h
    dimensions = [width, height]
    return dimensions

def centralize(image):
    x, y = get_dimensions()[0], get_dimensions()[1]
    return [(x / 2) - (image.get_width()/2), (y / 2) - (image.get_height()/2)]
    #(1920 / 2) - 256, (1080 / 2) - 256)

## IMAGES ##

def get_image(path):
    global _image_library
    image = _image_library.get(path)
    if image is None:
        image = pygame.image.load(path)
        _image_library[path] = image
    if pygame.display.get_init():
        return image.convert_alpha()
    else:
        return image


## MUSIC ##

def play_sound(path):
    global _sound_library
    sound = _sound_library.get(path)
    if sound is None:
        sound = pygame.mixer.Sound(path)
        _sound_library[path] = sound
    sound.play()

## FONTS ##

def make_font(fonts, size):
    available = pygame.font.get_fonts()
    choices = map(lambda x: x.lower().replace(' ', ''), fonts)
    for choice in choices:
        if choice in available:
            return pygame.font.SysFont(choice, size)
    return pygame.font.Font(None, size)


def get_font(font_preferences, size):
    global _cached_fonts
    key = str(font_preferences) + '|' + str(size)
    font = _cached_fonts.get(key, None)
    if font is None:
        font = make_font(font_preferences, size)
        _cached_fonts[key] = font
    return font

def create_text(text, fonts, size, color):
    global _cached_text
    key = '|'.join(map(str, (fonts, size, color, text)))
    image = _cached_text.get(key, None)
    if image is None:
        font = get_font(fonts, size)
        image = font.render(text, True, color)
        _cached_text[key] = image
    return image
