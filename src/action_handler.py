import os
import pyautogui
import pywinctl as pwc


class ActionHandler:
    def __init__(self, config):
        self.config = config

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

    def handle_button(self, button_name):
        active_window = self.get_active_window()
        # print(f"Active window: {active_window.title if active_window else 'None'}")

        # 1. Check for Application specific shortcuts
        for key, value in self.config.items():
            if not isinstance(value, dict):
                continue

            if value.get("level") == "application":
                if self._matches_application(active_window, value):
                    shortcuts = value.get("shortcuts", [])
                    for shortcut in shortcuts:
                        if shortcut.get("button") == button_name:
                            self.execute_action(shortcut)
                            return  # Handled by app specific

        # 2. Check for System shortcuts
        system_config = self.config.get("system", {})
        if system_config:
            shortcuts = system_config.get("shortcuts", [])
            for shortcut in shortcuts:
                if shortcut.get("button") == button_name:
                    self.execute_action(shortcut)
                    return
