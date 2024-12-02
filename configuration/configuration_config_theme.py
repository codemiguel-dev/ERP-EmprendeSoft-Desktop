import configparser


def load_config(self):
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config.get("Settings", "theme", fallback="0")
