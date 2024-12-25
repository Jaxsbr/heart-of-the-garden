import pygame

def load_texture(path, scale_size):
    texture = pygame.image.load(path).convert_alpha()
    texture = pygame.transform.scale(texture, (scale_size[0], scale_size[1]))
    return texture
