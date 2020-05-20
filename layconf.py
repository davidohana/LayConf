"""
LayConf - Layered Configuration Parser for Python3
Written by david.ohana@ibm.com
License: Apache-2.0
"""

import configparser
import os


class LayConf:
    _config_parser_default = configparser.ConfigParser()
    _config_parser_custom = configparser.ConfigParser()
    env_prefix = ""

    ERROR_WHEN_NOT_FOUND = object
    BOOLEAN_STATES = {'1': True, 'yes': True, 'true': True, 'on': True,
                      '0': False, 'no': False, 'false': False, 'off': False}

    @staticmethod
    def init_config(default_config_file_path="cfg/default.ini", custom_config_file_path="", env_prefix=""):
        assert not is_none_or_blank(default_config_file_path)
        if env_prefix is None:
            env_prefix = ""

        LayConf.env_prefix = env_prefix
        LayConf._config_parser_default.read(default_config_file_path)
        if not is_none_or_blank(custom_config_file_path):
            LayConf._config_parser_custom.read(custom_config_file_path)

        print("config env prefix:", env_prefix)
        print("config default:", default_config_file_path)
        print("config custom:", custom_config_file_path)

    @staticmethod
    def get(section: str, option: str, fallback: object = ERROR_WHEN_NOT_FOUND):
        assert not is_none_or_blank(section)
        assert not is_none_or_blank(option)

        env_key = LayConf._get_env_key(section, option)
        env_val = os.environ.get(env_key)
        if env_val is not None:
            return env_val

        custom_val = LayConf._config_parser_custom.get(section, option, fallback=None)
        if custom_val is not None:
            return custom_val

        default_val = LayConf._config_parser_default.get(section, option, fallback=None)
        if default_val is not None:
            return default_val

        if fallback == LayConf.ERROR_WHEN_NOT_FOUND:
            raise KeyError(f"Configuration value for {section}/{option} not found")

        return fallback

    @staticmethod
    def getint(section: str, option: str, fallback: object = ERROR_WHEN_NOT_FOUND):
        str_value = LayConf.get(section, option, fallback)
        return int(str_value)

    @staticmethod
    def getfloat(section: str, option: str, fallback: object = ERROR_WHEN_NOT_FOUND):
        str_value = LayConf.get(section, option, fallback)
        return float(str_value)

    @staticmethod
    def getboolean(section: str, option: str, fallback: object = ERROR_WHEN_NOT_FOUND):
        str_value = LayConf.get(section, option, fallback)
        return LayConf._convert_to_boolean(str_value)

    @staticmethod
    def getsection(section: str):
        assert not is_none_or_blank(section)
        return Section(section)

    @staticmethod
    def _get_env_key(section, option):
        tokens = []
        if LayConf.env_prefix:
            tokens.append(LayConf.env_prefix)
        tokens.append(section)
        tokens.append(option)
        return '_'.join(tokens)

    @staticmethod
    def _convert_to_boolean(value):
        """Return a boolean value translating from other types if necessary.
        """
        if value.lower() not in LayConf.BOOLEAN_STATES:
            raise ValueError('Not a boolean: %s' % value)
        return LayConf.BOOLEAN_STATES[value.lower()]


def is_none_or_blank(s: str):
    return s is None or str(s) == ""


class Section:
    def __init__(self, section: str):
        self.section = section

    def __getitem__(self, option: str):
        return LayConf.get(self.section, option)

    def get(self, option: str, fallback=None):
        return LayConf.get(self.section, option, fallback)

    def getint(self, option: str, fallback: object = LayConf.ERROR_WHEN_NOT_FOUND):
        return LayConf.getint(self.section, option, fallback)

    def getfloat(self, option: str, fallback: object = LayConf.ERROR_WHEN_NOT_FOUND):
        return LayConf.getfloat(self.section, option, fallback)

    def getboolean(self, option: str, fallback: object = LayConf.ERROR_WHEN_NOT_FOUND):
        return LayConf.getboolean(self.section, option, fallback)
