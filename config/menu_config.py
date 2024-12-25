class MenuConfig:
    def __init__(self, button_offset, layout_position) -> None:
        self.button_offset = button_offset
        self.layout_position = layout_position

def get_default_menu_config():
    return MenuConfig(
        button_offset=(0, 10),
        layout_position=(100, 100))
