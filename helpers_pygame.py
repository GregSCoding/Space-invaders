import pygame

def get_image(sheet, frame, width, height, row=0, scale=1):
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0,0), ((frame * width), (height * row), width, height))
    image = pygame.transform.scale(image,(width*scale, height*scale))
    image.set_colorkey((0, 0, 0))
    return image

def display_text(display, orientation, x, y, font, text, txt_color):
    text = font.render(text, True, txt_color)
    text.set_alpha(256)
    textRect = text.get_rect()
    if orientation.lower() == "bottomleft":
        textRect.bottomleft = (x, y)
    elif orientation.lower() == "center":
        textRect.center =  (x, y)
    elif orientation.lower() == "topleft":
        textRect.topleft =  (x, y)
    elif orientation.lower() == "topright":
        textRect.topright =  (x, y)
    elif orientation.lower() == "bottomright":
        textRect.bottomright =  (x, y)
    display.blit(text, textRect)