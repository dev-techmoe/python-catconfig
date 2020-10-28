from enum import Enum
from typing import Any
from importlib import import_module

class ValidationError(Exception):
    """
    Error class for validation failed
    """

    def __init__(self, payload: dict):
        """
        :param message: error message
        """
        self.payload = payload

    def generate_err_msg(self, payload: dict, indent: int = 0) -> str:
        """
        Generate human-friendly error message
        example output:
            key1: Error message
            key2:
                inner_key: error message
                inner_key2:
                    key3: error message
        """
        make_indent = ''.join(['    ' for i in range(0, indent)])
        previous_text = ''

        for (key, errors) in payload.items():
            for err in errors:
                if isinstance(err, dict):
                    previous_text += '{}{}:\n'.format(make_indent, key)
                    previous_text += self.generate_err_msg(err, indent+1)
                    pass
                else:
                    previous_text += '{}{}: {}\n'.format(make_indent, key, err)
                    pass

        return previous_text

    @property
    def message(self):
        return self.generate_err_msg(self.payload)


class CatConfig:
    def __init__(self, format: str = 'json', validator_schema: dict = None, data: dict = None):
        """
        :param format: Format of data used for read (json/toml/yaml)
        :param validator_schema: Schema for validator (see https://docs.python-cerberus.org/en/stable/usage.html)
        :param data: Config data
        """

        self._parser = None
        self._data = {}
        if not data == None:
            self._data = data
        self._validator_schema = validator_schema

        if format:
            self._import_parser(format)

        self._config = {}

    def _import_parser(self, parser_name: str):
        if parser_name == 'json':
            self._parser = import_module('json')
        elif parser_name == 'toml':
            try:
                self._parser = import_module('toml')
            except ImportError:
                raise Exception(
                    "CatConfig needs toml parser to work, "
                    "please add `toml` module to your project")
        elif parser_name == 'yaml':
            try:
                self._parser = import_module('yaml')
                # it works! I love Python!
                self._parser.loads = self._parser.load
            except ImportError:
                raise Exception(
                    "CatConfig needs yaml parser to work, "
                    "please add `pyyaml` module to your project\n")
        else:
            raise Exception('Unsupported parser type')

    def load_from_file(self, file_path: str, format: 'str' = None) -> None:
        """
        Update config from file
        :param file_path: config file path
        :param format: format of config file (default: json)
        """
        with open(file_path, 'r') as f:
            self.load_from_string(f.read(), format)

    def load_from_string(self, data: str, format: 'str' = None) -> None:
        """
        Update config from string and validate
        :param data: target data
        :param format: format of config file (default: json)
        """
        if format:
            self._import_parser(format)
        return self.load(self._parser.loads(data))

    def load(self, data: dict) -> None:
        """
        Update config from param `data`
        :param data: data
        """
        if self._validator_schema:
            self.validate(data)
        self._data.update(data)

    def validate(self, data: str) -> None:
        """
        Validate data
        :param data: config data
        """
        try:
            cerberus = import_module('cerberus')
        except ImportError:
            raise Exception('CatConfig need `cerberus` module to make validation work normally, '
                            'please add `cerberus` module to your project.')
        v = cerberus.Validator(self._validator_schema)
        v.validate(data)
        if v != True:
            raise ValidationError(v.errors)

    def update(self, data: dict) -> None:
        """
        Update config item
        :param data: data to be updated
        """
        self._data.update(data)

    def set(self, key: str, value: str) -> None:
        """
        Set config value
        :param key: key of config item
        :param value: value of config item
        """
        return self.update({key: value})

    def get(self, key: str=None) -> Any:
        """
        Get item by key
        It will return self contained object if param `key` == None
        :param key: key
        """
        if key == None:
            return self._data
        if key in self._data:
            data = self._data.get(key)
            if isinstance(data, dict):
                return CatConfig(data=data)
            elif isinstance(data, list):
                return [CatConfig(data=x) for x in data]
            else:
                return data
        return CatConfig()
    
    def __getitem__(self, key: str) -> Any:
        return self.get(key)

    def __bool__(self):
        """
        Return False if `self._data` has no item
        """
        return len(self._data) != 0

    def __getattr__(self, name: str) -> Any:
        return self.__getitem__(name)

    def __eq__(self, b):
        """
        Make sure CatConfig object without any data equal False
        """
        if b == None:
            if len(self._data.keys()) == 0:
                return True
        return self._data == b

    def __str__(self):
        if self._data == {}:
            return 'None'
        return str(self._data)