import pygame

def get_image(sheet, scale, frame, width, height):
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0,0), ((frame * width), 0, width, height))
    image = pygame.transform.scale(image,(width*scale, height*scale))
    image.set_colorkey((0, 0, 0))
    
    return image