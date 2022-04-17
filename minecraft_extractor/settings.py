import json
import logging
import os

_LOGGER = logging.getLogger("SETTINGS")


class Settings:
    def __init__(self, version):
        self._properties = {}
        self.add_property("meta", "version", version)

    def add_property(self, group: str, key: str, default=None) -> "Settings":
        """
        Add a property to be stored in the settings
        :param group: A section of properties
        :param key: The name of the property
        :param default: The default value of the property
        :return: Its self
        """
        if group in self._properties:
            self._properties[group] |= {key: default}
        else:
            self._properties |= {group: {key: default}}
        return self

    def set_property(self, group: str, key: str, value) -> "Settings":
        """
        Set the value of a property
        :param group: A section of properties
        :param key: The name of the property
        :param value: The value that the property will be set to
        :return: Its self
        """
        self._properties[group][key] = value
        return self

    def get_property(self, group: str, key: str):
        """
        Get the value of a property
        :param group: A section of properties
        :param key: The name of the property
        :return: The value stored in the property
        """
        if group in self._properties:
            if key in self._properties[group]:
                return self._properties[group][key]
            else:
                raise AttributeError(f"No property called '{key}' in '{group}'")
        else:
            raise AttributeError(f"No properties in {group}")

    def is_property_unset(self, group: str, key: str) -> bool:
        """
        Whether the selected property is unset
        :param group: A section of properties
        :param key: The name of the property
        :return: True is unset. False if set
        """
        return self.get_property(group, key) is None

    def get_group(self, group: str):
        """
        Get the value of a property
        :param group: A section of properties
        :return: The value stored in the property
        """
        if group in self._properties:
            return self._properties[group]
        else:
            raise AttributeError(f"No properties in {group}")

    def save(self):
        with open("settings.json", "w", encoding="utf-8") as file:
            json.dump(self._properties, file, ensure_ascii=False, indent=2)
        _LOGGER.info(f"Saved settings to {os.path.abspath('settings.json')}")

    def load(self):
        if os.path.exists("settings.json"):
            with open("settings.json", "r") as file:
                settings_file = json.load(file)
            for group, properties in settings_file.items():
                for key, value in properties.items():
                    self.add_property(group, key, value)


MAIN_SETTINGS = Settings(0)\
    .add_property("locations", "minecraft")

# Load settings file
MAIN_SETTINGS.load()
MAIN_SETTINGS.save()
