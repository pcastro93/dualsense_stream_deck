from mapping import get_mapping
import os
import pyautogui
import pywinctl as pwc


class ActionHandler:
    def __init__(self, config, controller):
        self.config = config
        self.controller = controller

    def get_active_window(self):
        try:
            return pwc.getActiveWindow()
        except Exception as e:
            print(f"Error getting active window: {e}")
            return None

    def _matches_application(self, window, app_config):
        if not window:
            return False

        window_title = window.title.lower() if window.title else ""
        window_app_name = (
            window.getAppName().lower() if hasattr(window, "getAppName") else ""
        )
        # print(f"Window title: {window_title}\nWindow app name: {window_app_name}")

        matchers = app_config.get("application", [])
        # It should check that all matchers match (and instead of or)
        all_match = True
        for matcher in matchers:
            if "name" in matcher and "contains" in matcher:
                if matcher["contains"].lower() not in window_app_name:
                    all_match = False
                    break
            if "title" in matcher and "contains" in matcher:
                if matcher["contains"].lower() not in window_title:
                    all_match = False
                    break
        return all_match

    def execute_action(self, action_def):
        action_type = action_def.get("type")
        print(f"Executing action: {action_def}")

        if action_type == "command":
            command = action_def.get("command")
            if command:
                os.system(command)

        elif action_type == "hotkey":
            keys = action_def.get("hotkeys", [])
            if keys:
                pyautogui.hotkey(*keys)

        elif action_type == "press":
            keys = action_def.get("keys", [])
            if keys:
                for key in keys:
                    pyautogui.press(key)

    def _check_buttons_pressed(self, buttons):
        """Check if all buttons in the list are pressed on the controller."""
        if not self.controller:
            return False

        buttons_mapping = get_mapping()
        buttons_pressed = []
        for btn_name in buttons:
            attribute_name = buttons_mapping.get(btn_name)
            if attribute_name and hasattr(self.controller, attribute_name):
                btn_obj = getattr(self.controller, attribute_name)
                # Check if pressed
                if btn_obj.value:
                    buttons_pressed.append(btn_name)
            # Check touches/triggers if needed? For now focus on buttons.
            # L2/R2 are triggers but valid as buttons? dualsense-controller treats L2/R2 as triggers usually
            elif btn_name in ["l2", "r2"]:
                if btn_name == "l2":
                    if self.controller.left_trigger.value >= 0.2:  # Threshold
                        buttons_pressed.append(btn_name)
                elif btn_name == "r2":
                    if self.controller.right_trigger.value >= 0.2:
                        buttons_pressed.append(btn_name)
                else:
                    print(f"Warning: Unknown button '{btn_name}'")
            else:
                print(
                    f"Warning: Controller missing button attribute '{attribute_name}'"
                )

        return len(buttons_pressed) == len(buttons)

    def handle_button(self, button_name):
        active_window = self.get_active_window()

        # We need to collect all matching shortcuts (both single and multi-button)
        # And prioritize the ones with MOST buttons (specific > general)
        params = {"matches": []}  # list of tuples (priority, action_def)

        def check_and_add(shortcut_def):
            # 1. Does this shortcut involve the current triggered button?
            # A shortcut matches if:
            # - It's a single button shortcut and matches `button_name`
            # - It's a multi-button shortcut and `button_name` is one of them AND all are pressed.

            buttons = shortcut_def.get("buttons", [])
            single_button = shortcut_def.get("button")

            if single_button:
                buttons = [single_button]

            if button_name not in buttons:
                return  # Not triggered by this event

            # Check if all buttons are pressed
            # Note: The button triggering this event (`button_name`) is presumed pressed/down.
            # We must check the OTHERS.
            other_buttons = [b for b in buttons if b != button_name]
            if not other_buttons or self._check_buttons_pressed(other_buttons):
                params["matches"].append((len(buttons), shortcut_def))

        # 1. Check for Application specific shortcuts
        for key, value in self.config.items():
            if not isinstance(value, dict):
                continue

            if value.get("level") == "application":
                if self._matches_application(active_window, value):
                    shortcuts = value.get("shortcuts", [])
                    for shortcut in shortcuts:
                        check_and_add(shortcut)

        # 2. Check for System shortcuts
        system_config = self.config.get("system", {})
        if system_config:
            shortcuts = system_config.get("shortcuts", [])
            for shortcut in shortcuts:
                check_and_add(shortcut)

        # Execute the best match
        if params["matches"]:
            # Sort by priority (length of buttons) descending
            params["matches"].sort(key=lambda x: x[0], reverse=True)
            # Execute top one
            self.execute_action(params["matches"][0][1])
