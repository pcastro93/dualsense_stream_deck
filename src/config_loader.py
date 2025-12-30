import yaml


class ConfigLoader:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.config = {}

    def load_config(self):
        """Loads the YAML configuration file."""
        try:
            with open(self.config_path, "r") as file:
                self.config = yaml.safe_load(file) or {}
            print(f"Loaded config from {self.config_path}")
        except FileNotFoundError:
            print(f"Config file not found: {self.config_path}")
            self.config = {}
        except yaml.YAMLError as e:
            print(f"Error parsing YAML: {e}")
            self.config = {}

        return self.config

    def get_shortcuts(self):
        """Returns the shortcuts configuration."""
        return self.config.get("shortcuts_config", {})
