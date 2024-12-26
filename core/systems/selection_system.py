import pygame

from core.components import PositionComponent, SelectionComponent


class SelectionSystem:


    def update(self, entities):
        mouse_clicks = pygame.mouse.get_pressed()
        mouse_left_clicked = mouse_clicks[0]
        mouse_right_clicked = mouse_clicks[2]
        mouse_x, mouse_y = pygame.mouse.get_pos()

        for entity in entities:
            position_component: PositionComponent = entity.position_component
            selection_component: SelectionComponent = entity.selection_component
            if mouse_left_clicked:
                # Select the entity that was clicked
                in_bounds = position_component.contains_point((mouse_x, mouse_y))
                within_range = position_component.within_center_distance(64, (mouse_x, mouse_y))
                if in_bounds or within_range:
                    selection_component.is_selected = True
            elif mouse_right_clicked:
                selection_component.is_selected = False


