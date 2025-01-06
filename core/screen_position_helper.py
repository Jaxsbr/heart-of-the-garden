import random
import pygame

from core.entities.entity import Entity


def get_random_out_bounds_pos(screen_size, inflate_size=(200, 200)) -> pygame.Vector2:
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


def get_random_not_overlapping_in_bounds_pos(
    screen_size, desired_size, entities: list[Entity]
) -> pygame.Vector2 | None:
    # pick a random coord in the rect
    # calculate a proposed bounds
    # loop existing entities
    # check bounds intersection
    # return none if any intersect, return coordinate if none intersect

    rx, ry = random.randint(0, screen_size[0]), random.randint(0, screen_size[1])

    rect = pygame.Rect(rx, ry, desired_size[0], desired_size[1])

    for entity in entities:
        bounds = entity.position_component.get_bounds()
        if bounds.colliderect(rect):
            return None

    return pygame.Vector2(rx, ry)
