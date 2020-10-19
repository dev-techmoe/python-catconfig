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
print(c['foo'])
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