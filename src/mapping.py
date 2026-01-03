def get_mapping():
    """Define mapping: (config_name, controller_button_attribute)"""
    button_mapping = {
        "cross": "btn_cross",
        "circle": "btn_circle",
        "triangle": "btn_triangle",
        "square": "btn_square",
        "l1": "btn_l1",
        "l3": "btn_l3",
        "r3": "btn_r3",
        "r1": "btn_r1",
        "arrow_left": "btn_left",
        "arrow_right": "btn_right",
        "arrow_down": "btn_down",
        "arrow_up": "btn_up",
        "create": "btn_create",  # Select
        "options": "btn_options",  # Start
        "ps": "btn_ps",  # PS
    }
    return button_mapping
