import time

import pyautogui
from dualsense_controller import DualSenseController
from config_loader import ConfigLoader
from action_handler import ActionHandler

controller = None
action_handler = None


# Use a simple class to track finger states
class TouchTracker:
    def __init__(self):
        self.f1_active = False
        self.f2_active = False


tracker = TouchTracker()


def on_f1_change(value):
    # print(f"f1: {value}")
    tracker.f1_active = value.active


def on_f2_change(value):
    # print(f"f2: {value}")
    tracker.f2_active = value.active


def on_btn_touchpad(value):
    global controller
    if tracker.f2_active and value:
        # Click with two fingers
        pyautogui.rightClick()
    # elif tracker.f1_active and value:
    # Click with one finger


def on_error(error):
    print(f"an unforseen error occured {error}")


def on_battery_change(battery) -> None:
    print(f"on battery change: {battery}")


def on_battery_lower_than(battery_level) -> None:
    print(f"on battery low: {battery_level}")


def on_battery_charging(battery_level) -> None:
    print(f"on battery charging: {battery_level}")


def on_battery_discharging(battery_level) -> None:
    print(f"on battery discharging: {battery_level}")


def on_right_stick_change(right_stick):
    current_y = right_stick.y
    delta_y_threshold = 0.15
    if abs(current_y) > delta_y_threshold:
        # print(right_stick)
        pyautogui.scroll(
            int(current_y * 2)
        )  # a non-linear function might be used to allow smoother scrolling


def create_button_handler(button_name):
    def handler():
        if action_handler:
            action_handler.handle_button(button_name)

    return handler


def main():
    device_infos = DualSenseController.enumerate_devices()
    if len(device_infos) < 1:
        raise Exception("No DualSense Controller available.")
    else:
        print(device_infos)

    global controller
    controller = DualSenseController()

    # Load configuration
    config_loader = ConfigLoader("data/config.yml")
    config = config_loader.load_config()
    global action_handler
    action_handler = ActionHandler(config.get("shortcuts_config", {}))

    controller.on_error(on_error)
    controller.touch_finger_1.on_change(on_f1_change)
    controller.touch_finger_2.on_change(on_f2_change)
    controller.btn_touchpad.on_change(on_btn_touchpad)

    controller.battery.on_change(on_battery_change)
    controller.battery.on_lower_than(20, on_battery_lower_than)
    controller.battery.on_charging(on_battery_charging)
    controller.battery.on_discharging(on_battery_discharging)

    # Dynamic Registration
    # Mapping from matched config button names to controller buttons

    # Define mapping: (config_name, controller_button_obj)
    button_mapping = {
        "cross": controller.btn_cross,
        "circle": controller.btn_circle,
        "triangle": controller.btn_triangle,
        "square": controller.btn_square,
        "l1": controller.btn_l1,
        "r1": controller.btn_r1,
        "arrow_left": controller.btn_left,
        "arrow_right": controller.btn_right,
        "arrow_down": controller.btn_down,
        "arrow_up": controller.btn_up,
        "create": controller.btn_create,
        "options": controller.btn_options,
        "ps": controller.btn_ps,
    }

    for name, btn in button_mapping.items():
        btn.on_down(create_button_handler(name))

    # controller.right_stick.on_change(on_right_stick_change)
    # controller.gyroscope.on_change(on_gyroscope_change)
    # controller.accelerometer.on_change(on_accelerometer_change)
    # controller.orientation.on_change(on_orientation_change)

    try:
        controller.activate()
        print("Controller activated. Press Ctrl+C to exit.")
        while True:
            on_right_stick_change(controller.right_stick.value)
            time.sleep(0.01)
    except KeyboardInterrupt:
        pass
    finally:
        controller.deactivate()


if __name__ == "__main__":
    main()
