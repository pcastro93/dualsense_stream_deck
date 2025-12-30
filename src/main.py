import os
import time

import pyautogui
import pywinctl as pwc
from dualsense_controller import DualSenseController

controller = None


def get_active_window():
    active_window = pwc.getActiveWindow()
    return active_window


# Use a simple class to track finger states
class TouchTracker:
    def __init__(self):
        self.f1_active = False
        self.f2_active = False
        self.clicked = False


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
        pyautogui.rightClick()
    elif tracker.f1_active and value:
        controller.player_leds.set_inner()
        controller.left_trigger.effect.no_resistance()


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


def on_gyroscope_change(gyroscope):
    print(f"on_gyroscope_change: {gyroscope}")


def on_accelerometer_change(accelerometer):
    print(f"on_accelerometer_change: {accelerometer}")


def on_orientation_change(orientation):
    print(f"on_orientation_change: {orientation}")


def on_cross_down():
    print(get_active_window().getAppName())


def on_circle_down():
    if "chrome" in get_active_window().getAppName():
        pyautogui.hotkey("ctrl", "r")


def on_left_down():
    if any(app in get_active_window().getAppName() for app in ["chrome"]):
        pyautogui.hotkey("alt", "left")


def on_right_down():
    if "chrome" in get_active_window().getAppName():
        pyautogui.hotkey("alt", "right")


def on_up_down():
    if "chrome" in get_active_window().getAppName():
        pyautogui.press("home")


def on_down_down():
    if "chrome" in get_active_window().getAppName():
        pyautogui.press("end")


def on_l1_down():
    if any(app in get_active_window().getAppName() for app in ["chrome", "zed"]):
        pyautogui.hotkey("ctrl", "pgup")


def on_r1_down():
    if any(app in get_active_window().getAppName() for app in ["chrome", "zed"]):
        pyautogui.hotkey("ctrl", "pgdn")


def on_select_down():
    os.system(
        "qdbus org.kde.kglobalaccel /component/kmix invokeShortcut 'decrease_volume'"
    )


def on_start_down():
    os.system(
        "qdbus org.kde.kglobalaccel /component/kmix invokeShortcut 'increase_volume'"
    )


def on_ps_down():
    os.system("qdbus org.kde.kglobalaccel /component/kmix invokeShortcut 'mute'")


def on_right_stick_change(right_stick):
    current_y = right_stick.y
    delta_y_threshold = 0.15
    if abs(current_y) > delta_y_threshold:
        print(right_stick)
        pyautogui.scroll(
            current_y * 2
        )  # a non-linear function might be used to allow smoother scrolling


def main():
    device_infos = DualSenseController.enumerate_devices()
    if len(device_infos) < 1:
        raise Exception("No DualSense Controller available.")
    else:
        print(device_infos)
    global controller
    controller = DualSenseController()

    controller.on_error(on_error)
    controller.touch_finger_1.on_change(on_f1_change)
    controller.touch_finger_2.on_change(on_f2_change)
    controller.btn_touchpad.on_change(on_btn_touchpad)

    controller.battery.on_change(on_battery_change)
    controller.battery.on_lower_than(20, on_battery_lower_than)
    controller.battery.on_charging(on_battery_charging)
    controller.battery.on_discharging(on_battery_discharging)

    controller.btn_cross.on_down(on_cross_down)
    controller.btn_circle.on_down(on_circle_down)
    controller.btn_l1.on_down(on_l1_down)
    controller.btn_r1.on_down(on_r1_down)
    controller.btn_left.on_down(on_left_down)
    controller.btn_right.on_down(on_right_down)
    controller.btn_down.on_down(on_down_down)
    controller.btn_up.on_down(on_up_down)
    controller.btn_create.on_down(on_select_down)  # select
    controller.btn_options.on_down(on_start_down)  # start
    controller.btn_ps.on_down(on_ps_down)
    # controller.right_stick.on_change(on_right_stick_change)

    # controller.gyroscope.on_change(on_gyroscope_change)
    # controller.accelerometer.on_change(on_accelerometer_change)
    # controller.orientation.on_change(on_orientation_change)

    try:
        controller.activate()
        while True:
            on_right_stick_change(controller.right_stick.value)
            time.sleep(0.001)
    except KeyboardInterrupt:
        pass
    finally:
        controller.deactivate()


if __name__ == "__main__":
    main()
