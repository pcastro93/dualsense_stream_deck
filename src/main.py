import os
import argparse
import math
import time

import yaml.cyaml
import pyautogui
from dualsense_controller import DualSenseController
from config_loader import ConfigLoader
from action_handler import ActionHandler

from mapping import get_mapping
from windows import print_all_windows_data

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
    DELTA_Y_THRESHOLD = 0.15
    MAX_SCROLL_SPEED = 4
    MIN_SCROLL_SPEED = 1
    current_y = right_stick.y

    def transform_input(y_value):
        """Map input value using a non-linear function for smoother scrolling"""
        y_sign = math.copysign(1, y_value)
        return y_sign * abs(y_value * y_value * y_value)

    def get_value_to_scroll(y_value):
        y_sign = math.copysign(1, y_value)
        to_scroll = int(transform_input(y_value) * MAX_SCROLL_SPEED)
        return (
            to_scroll
            if abs(to_scroll) > MIN_SCROLL_SPEED
            else MIN_SCROLL_SPEED * y_sign
        )

    if abs(current_y) >= DELTA_Y_THRESHOLD:
        pyautogui.scroll(get_value_to_scroll(current_y))


def create_button_handler(button_name):
    def handler():
        if action_handler:
            action_handler.handle_button(button_name)

    return handler


def main():
    parser = argparse.ArgumentParser(description="DualSense Stream Deck")
    parser.add_argument("--config", help="The config file", required=True)
    parser.add_argument(
        "--view-windows",
        action="store_true",
        help="View available windows",
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Increase output verbosity"
    )

    args = parser.parse_args()

    if args.view_windows:
        print_all_windows_data()
        return

    # Check if config file exists
    if not os.path.exists(args.config):
        print(f"Config file does not exist: {args.config}")
        return -1

    # Check if config file is a valid YAML file
    try:
        with open(args.config, "r") as f:
            yaml.safe_load(f)
    except yaml.YAMLError as exc:
        print(f"Invalid YAML file: {args.config}")
        return -1

    device_infos = DualSenseController.enumerate_devices()
    if len(device_infos) < 1:
        print("No DualSense Controller available.")
        return -1
    else:
        print(device_infos)

    global controller
    controller = DualSenseController()

    # Load configuration
    config_loader = ConfigLoader(args.config)
    config = config_loader.load_config()
    global action_handler
    action_handler = ActionHandler(config.get("shortcuts_config", {}), controller)

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
    button_mapping = get_mapping()
    for name, btn in button_mapping.items():
        getattr(controller, btn).on_down(create_button_handler(name))

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
