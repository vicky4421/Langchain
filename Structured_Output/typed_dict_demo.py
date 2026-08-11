'''
TypedDict is a feature introduced in Python 3.8 that allows you to define a dictionary with specific key-value types. It is part of the typing module and is used to create type hints for dictionaries with fixed keys and value types.

It is only for representation purpose, there's no validation takes place, if a function or variable is of other type, we don't get any errors.
'''

from typing import TypedDict

class Person(TypedDict):
    name: str
    age: int
    email: str

new_person: Person = {
    "name": "John Doe",
    "age": 30,
    "email": "john.doe@example.com"
}

print(new_person)