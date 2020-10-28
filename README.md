# CatConfig
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/catconfig) 
![PyPI - License](https://img.shields.io/pypi/l/catconfig)
![test](https://github.com/dev-techmoe/python-catconfig/workflows/test/badge.svg)

🐱Make more easy for reading/validating/updating config for python app

## Install 

```
pip install catconfig
```

If you want to use validation feature, install `cerberus` module for your project to use it normally.  

Install `toml` or `pyyaml` module for toml/yaml format parsing.

## Quickstart

```python
# Example.py
from catconfig import CatConfig, ValidationError

# Load
# Load config from string
c = CatConfig()
c.load_from_string("""
{
    "foo": "bar"
}
""")
# Load config when initalizing CatConfig object
c = CatConfig(data={
    'foo': 'bar'
})
# load config from file
c = CatConfig()
c.load_from_file('./tests/assests/test.json')
# Specify config type when initalizing CatConfig object
c = CatConfig(format='json')
c.load_from_file('./tests/assests/test.json')
# Specify config type when loading config file
c = CatConfig()
c.load_from_file('./tests/assests/test.json', format='json')

# Get item
print(c.foo)
# Print: bar
print(bool(c.some.value.does.nt.exists))
# Print: False
print(str(c.some.value.does.nt.exists))
# Print: None
print(c['foo'])
# Print: bar
print(c.get('foo'))
# Print: bar

# Validation
# visit https://docs.python-cerberus.org/en/stable/usage.html for more info of schema
schema = {
    'foo': {
        'type': 'integer'
    },
    'some_field': {
        'type': 'string'
    }
}
c = CatConfig(validator_schema=schema)
try:
    c.load_from_file('./tests/assests/test.json')
except ValidationError as err:
    print(err.message)
    # Print:
    # arr: unknown field
    # foo: must be of integer type
```

## License
MIT