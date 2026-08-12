'''
    Pydantic is data validation and data parsing lib for python. It ensures that the data you work with is correct, structured and typesafe.
'''

from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class Student(BaseModel):
    name: str = 'Vivek'
    age: Optional[int] = None
    email: EmailStr
    cgpa: float = Field(gt=0, lt=10, default=5.0, description= 'Decimal value representing the cgpa value of student')
    mobile: str = Field(pattern=r'^(?:\+91[\-\s]?|91[\-\s]?|0)?[6-9]\d{9}$')

new_student = {'cgpa': 9.5, 'email': 'abc@abc.com', 'mobile': '+919876543210'}

student = Student(**new_student)

print(student)
print(type(new_student))

# convert dict to json
print('\n', student.model_dump_json())

#---------------------------------------------------------------------------------------------------------

'''
    Output:
        name='Vivek'
        <class 'dict'>
'''

# new_student1 = {'name': 34}
# student1 = Student(**new_student1)

# print(student1)

'''
    Output:
        Traceback (most recent call last):
          File "D:\AI\Langchain\Lang\Structured_Output\pydantic_demo.py", line 24, in <module>
            student1 = Student(**new_student1)
          File "D:\AI\Langchain\Lang\venv\Lib\site-packages\pydantic\main.py", line 263, in __init__
            validated_self = self.__pydantic_validator__.validate_python(data, self_instance=self)
        pydantic_core._pydantic_core.ValidationError: 1 validation error for Student
        name
          Input should be a valid string [type=string_type, input_value=34, input_type=int]
            For further information visit https://errors.pydantic.dev/2.13/v/string_type
'''

# DEFAULT VALUES
'''
    You can pass default values.

    class Student(BaseModel):
        name: str = 'Vivek'

    new_student = {}

    Output:
        name='Vivek'
        <class 'dict'>

'''

# OPTIONAL
'''
    You can use Optional class from typing module.
    If we keep a parameter option we must provide a default value or None.

    class Student(BaseModel):
        name: str = 'Vivek'
        age: Optional[int] = None

    Output:
        name='Vivek' age=None
        <class 'dict'>
'''

# COERCE / TYPE INFERING
'''
    If mistakenly we get a different type of value than expected and if its a basic type (int, str etc), pydantic can infer the value itself.

    class Student(BaseModel):
        name: str = 'Vivek'
        age: Optional[int] = None

    new_student = {'age': '36'}

    Output:
        name='Vivek' age=36
        <class 'dict'>
'''

# BUILT IN VALIDATIONS
'''
    Pydantic has many types of built in validations. e.g email
    for email we should install 'pip install "pydantic[email]"'

    from pydantic import BaseModel, EmailStr
    class Student(BaseModel):
        name: str = 'Vivek'
        age: Optional[int] = None
        email: EmailStr

    new_student = {'email': 'abc'}

    value is not a valid email address: An email address must have an @-sign. [type=value_error, input_value='abc', input_type=str]

    Pydantic has following types of built in validators:
        - Web & Network Types:	URLs, URIs, IP/mac addresses, 
        - Identifiers & Hashes:	UUIDs: Validate UUID versions 1, 3, 4, or 5., Cryptographic Hashes
        - Numbers with Constraints (Annotated / Field): Constrained Types: PositiveInt, NegativeInt, NonNegativeInt,    PositiveFloat, Custom Numerical Rules
        - Dates, Times & Durations
        - String Constraints & Regex Matching
        - File System & File Paths
        - Specialized Utility Types: Color validations, credit card no.s etc

'''

# FIELD FUNCTIONS (DEFAULT VALUES, CONSTRAINTS, DESCRIPTION, REGEX)
'''
    from pydantic import BaseModel, EmailStr, Field

    class Student(BaseModel):
        name: str = 'Vivek'
        age: Optional[int] = None
        email: EmailStr
        cgpa: float = Field(gt=0, lt=10, default=5.0, description= 'Decimal value representing the cgpa value of student')
        mobile: str = Field(pattern='^(?:\+91[\-\s]?|91[\-\s]?|0)?[6-9]\d{9}$')

    new_student = {'cgpa': 9.5, 'email': 'abc@abc.com', 'mobile': '12345'}

    Output for cgpa:
        Input should be less than 10 [type=less_than, input_value=12, input_type=int]

    Output for regex:
        String should match pattern '^(?:\+91[\-\s]?|91[\-\s]?|0)?[6-9]\d{9}$' [type=string_pattern_mismatch, input_value='12345', input_type=str]

'''