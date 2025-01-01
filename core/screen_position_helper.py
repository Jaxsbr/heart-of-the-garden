import random
import pygame


def get_random_start_pos(screen_size, inflate_size=(200, 200)) -> pygame.Vector2:
    # TODO: get inflate size from config
    inflated_rect = pygame.Rect(0, 0, screen_size[0], screen_size[1]).inflate(
        inflate_size[0], inflate_size[1]
    )

    # Regions: top, bottom, left, right
    regions = ["top", "bottom", "left", "right"]
    chosen_region = random.choice(regions)

    if chosen_region == "top":
        x = random.randint(inflated_rect.left, inflated_rect.right - inflate_size[0])
        y = inflated_rect.top - inflate_size[1]
    elif chosen_region == "bottom":
        x = random.randint(inflated_rect.left, inflated_rect.right - inflate_size[0])
        y = inflated_rect.bottom
    elif chosen_region == "left":
        x = inflated_rect.left - inflate_size[1]
        y = random.randint(inflated_rect.top, inflated_rect.bottom - inflate_size[1])
    elif chosen_region == "right":
        x = inflated_rect.right
        y = random.randint(inflated_rect.top, inflated_rect.bottom - inflate_size[1])

    return pygame.Vector2(x, y)
