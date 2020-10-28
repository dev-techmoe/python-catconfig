from catconfig import CatConfig, ValidationError
import json
import pytest


def test_get():
    c = CatConfig(data={
        'foo': {
            'bar': 'test'
        },
        'cat': [
            {
                'name': 'tom',
                'age': 114514
            },
            {
                'name': 'Jerry',
                'age': 1919810
            }
        ]
    })

    assert c.foo.bar == 'test'
    assert c.foo == {'bar': 'test'}
    assert c.a.b == None
    assert c.cat[0].name == 'tom'

    assert c['foo']['bar'] == 'test'
    assert c['foo'] == {'bar': 'test'}
    assert c['a']['b'] == None
    assert c['cat'][0]['name'] == 'tom'


@pytest.mark.parametrize(
    'type,path',
    [
        ('json', 'tests/assests/test.json'),
        ('toml', 'tests/assests/test.toml'),
        ('yaml', 'tests/assests/test.yaml')
    ]
)
def test_load_file(type, path):
    c = CatConfig(format=type)
    c.load_from_file(path)
    assert c.foo == 'bar'

    c = CatConfig()
    c.load_from_file(path, format=type)
    assert c.foo == 'bar'

    
    c = CatConfig(data={
        'previous_key': 'val'
    })
    c.load_from_file(path, format=type)
    assert c.previous_key == 'val'
    

def test_update():
    c = CatConfig(data={
        'foo': 'bar',
        'obj': {
            'key': 'val'
        },
        'boolitem': True
    })

    c.update({'test': 'val'})
    c.set('key', 'val')
    c.obj.set('key', 'new_val')

    assert c.test == 'val'
    assert c.key == 'val'
    assert c.obj.key == 'new_val'

    assert c.boolitem == True
    assert bool(c.obj) == True
    assert bool(c.some.item.does.nt.exist) == False

    assert c.get('test') == 'val'
    assert c.get('some_key_does_not_exists') == None


def test_validate():
    data = {
        'foo': {
            'key': 'value'
        },
        'id': 114514
    }
    schema = {
        'foo': {
            'type': 'dict',
            'schema': {
                'key': {
                    'type': 'integer'
                }
            }
        },
        'id': {
            'type': 'string'
        }
    }

    c = CatConfig(validator_schema=schema)

    with pytest.raises(ValidationError):
        c.load(data)


def test_generate_config():
    err = ValidationError({
        'l1': [
            {
                'l2': [{
                    'l3': ['value']
                }]
            }
        ],
        'foo': ['bar']
    })

    assert err.message != None