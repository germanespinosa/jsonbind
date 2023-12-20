# JsonBind

JsonBind is an advanced JSON handling library for Python, designed to enhance the capabilities of the standard json 
module. It offers seamless serialization and deserialization of Python data types not typically supported by the default 
JSON library, including datetime.datetime, tuples, sets, enumerations (enum), bytes, and custom classes.


## Installation
```
pip install jsonbind

```


## Features
- Compatibility: Functions prototypes designed to match the standard json library.
- Extended Data Type Support: Handle complex Python data types effortlessly.
- Custom Class Serialization: Easily serialize and deserialize your custom classes.
- Intuitive API: Designed to be familiar to users of the standard json module.


## The Python JSON standard library

The standard JSON library in Python expertly facilitates the serialization and deserialization of JSON data types into 
native Python data types, as detailed in the following table:

| JSON Data Type | Python Data Type |
|----------------|------------------|
| object         | dict             |
| array          | list             |
| string         | str              |
| number         | int, float       |
| bool           | bool             |
| null           | None             |

This compatibility with JSON significantly enhances its utility for data sharing, communication, and storage purposes. 
However, it is important to recognize that the JSON format's inherent limitations in representing more complex data 
structures can sometimes restrict its applicability. Crafting specific encoders and decoders to address these 
limitations often presents a substantial technical challenge, requiring thoughtful consideration and expertise.

## Type-bindings

JsonBind operates on the principle of utilizing type bindings to facilitate the transformation between JSON types and 
Python types. It comes equipped with an extensive array of pre-defined bindings for commonly used types, including 
tuples, sets, datetime objects, bytes, classes, and more. Additionally, JsonBind is designed to simplify the process 
of creating new bindings. This flexibility allows users to seamlessly integrate JSON types with novel Python data types, 
enhancing the library's adaptability and ease of use in various programming scenarios.

To extend the JSON's functionality, multiple bindings can be created for the same json data type. 
This allows, for example, strings to be decoded as datetime objects and bytes, object to class dictionaries and instances, etc.

### Out-of-the-box bindings

| JSON Data Type | Python Data Type                            |
|----------------|---------------------------------------------|
| object         | dict, <span style="color:blue">class</span> |
| array          | list, <span style="color:blue">tuple</span>, <span style="color:blue">set</span>|
| string         | str, <span style="color:blue">datetime</span>, <span style="color:blue">bytes</span>, <span style="color:blue">enum</span>                  |
| number         | int, float, <span style="color:blue">enum</span>                            |
| bool           | bool                                        |
| null           | None                                        |

## Side by side

<table>
<tr>
<th> Standard Library </th>
<th> JsonBind </th>
</tr>
<tr>
<td>
Serializing a datetime to JSON is not possible by default:

``` python
import json 
import datetime
mydate = datetime.datetime.now().date()
mydate = json.dumps(mydate)

```
output
```
TypeError: Object of type date is not JSON serializable
```

To do it,  it is necessary to create an  Encoder: 

```python
import json 
import datetime

class DateTimeEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
            return obj.isoformat()
        elif isinstance(obj, datetime.timedelta):
            return (datetime.datetime.min + obj).time().isoformat()

        return super(DateTimeEncoder, self).default(obj)

mydate = datetime.datetime.now().date()
encoder = DateTimeEncoder()
encoder.encode(mydate)
```
Output:
```
"2023-12-19"
```

However, this only works converting from python to json.
To read values from json to python it is necessary to write an additional Decoder class.
</td>
<td>
By default datetime values are fully supported by JsonBind:

```
import jsonbind as jb 
import datetime
mydate = datetime.datetime.now().date()
mydate = jb.dumps(mydate)
print(mydate)
mynewdate = jb.loads('"2023-12-20"', cls=datetime)
print(mynewdate)
```
Output:
```
"2023-12-19"
"2023-12-20"
```
</td>
</tr>
</table>


### Creating new bindings for python types
JsonBind allows the creation of new Bindings with very little code. 

In this example a new binding for the type datetime is created to encode to the object Json datatype (dict):

```python
import jsonbind as jb
import datetime

class MyDateBinding(jb.TypeBinding):
    def __init__(self):
        super().__init__(json_type=dict, python_type=datetime.datetime)

    def to_json_value(self, python_value: datetime.datetime) -> dict:
        return {"year": python_value.year,
                "month": python_value.month,
                "day": python_value.day}

    def to_python_value(self, json_value: dict, python_type: type) -> datetime.datetime:
        return datetime.datetime(year=json_value["year"],
                                 month=json_value["month"],
                                 day=json_value["day"])

jb.Bindings.set_binding(MyDateBinding())
print(jb.dumps(datetime.datetime.now()))

``` 
Output:
```python
{"year":2023,"month":12,"day":20}
```
To convert a JSON value to date time using the new binding, we need the following code: 
```python
new_date = jb.loads('{"year":2025,"month":10,"day":22}', cls=datetime.datetime)
print(new_date, type(new_date))
```
Output:
```python
2025-10-22 00:00:00 <class 'datetime.datetime'>
```
JsonBind automatically matches the expected type to the custom binding as there can only exist one binding per python 
type. This means that in this code the default binding for datetime was replaced during the set_binding operation.


### Creating bound classes
```python

import jsonbind as jb
import datetime

class MyClass(jb.BoundClass):
    def __init__(self):
        self.text = "Hello World"
        self.date = datetime.datetime.now()
        self.data = [3,1,4,1,5,9,2]

my_object=MyClass()
print("Serialization test:")
print(jb.dumps(my_object))
new_object = jb.loads('{"text":"Deseralization test","date":"2023-12-23","data":[6,2,8,3,1,8,4]}', cls=MyClass)
print()
print("Deserialization test:")
print ("Text: ",new_object.text, new_object.text.__class__)
print ("Date: ",new_object.date, new_object.date.__class__)
print ("Data: ",new_object.data, new_object.data.__class__)

```

Output:
```python
Serialization test:
{"text":"Hello World","date":"2023-12-20","data":[3,1,4,1,5,9,2]}

Deserialization test:
Text:  Deseralization test <class 'str'>
Date:  2023-12-23 00:00:00 <class 'datetime.datetime'>
Data:  [6, 2, 8, 3, 1, 8, 4] <class 'list'>
```

## Standard Json load and dump functions

### Loading a json string to its default python type

```python
import jsonbind as jb
mydict = jb.loads('{"name":"German Espinosa","age":41,"weight":190.0}')
print(mydict, type(mydict))
mylist = jb.loads('[1, 2, 3, 4]')
print(mylist, type(mylist))
myint = jb.loads('1')
print(myint, type(myint))
myfloat = jb.loads('10.5')
print(myfloat, type(myfloat))
mystring = jb.loads('"Hello World"')
print(mystring, type(mystring))
mybool = jb.loads('true')
print(mybool, type(mybool))
```
output
```
{'name': 'German Espinosa', 'age': 41, 'weight': 190.0} <class 'dict'>
[1, 2, 3, 4] <class 'list'>
1 <class 'int'>
10.5 <class 'float'>
Hello World <class 'str'>
True <class 'bool'>
```

### Serializing a json string from its default python type

```python
import jsonbind as jb
mydict = {"name":"German Espinosa","age":41,"weight":190.0}
print(jb.dumps(mydict), type(mydict))
mylist = [1, 2, 3, 4]
print(jb.dumps(mylist), type(mylist))
myint = 1
print(jb.dumps(myint), type(myint))
myfloat = 10.5
print(jb.dumps(myfloat), type(myfloat))
mystring = "Hello World"
print(jb.dumps(mystring), type(mystring))
mybool = True
print(jb.dumps(mybool), type(mybool))
```
output
```
{'name': 'German Espinosa', 'age': 41, 'weight': 190.0} <class 'dict'>
[1, 2, 3, 4] <class 'list'>
1 <class 'int'>
10.5 <class 'float'>
Hello World <class 'str'>
True <class 'bool'>
```

### Loading a json string to a non-default python type

```python
import jsonbind as jb
mytuple = jb.loads('[1, 2, 3, 4]', cls=tuple)
print(mytuple, type(mytuple))
myset = jb.loads('[1, 2, 3, 4]', cls=set)
print(myset, type(myset))
mybytes=jb.loads('"SGVsbG8gV29ybGQ="', cls=bytes)
print (mybytes, type(mybytes))
import datetime
mydate = jb.loads('"2023-12-19"', cls=datetime.datetime)
print(mydate, type(mydate))
```
output
```
(1, 2, 3, 4) <class 'tuple'>
{1, 2, 3, 4} <class 'set'>
b'Hello World' <class 'bytes'>
2023-12-19 00:00:00 <class 'datetime.datetime'>
```


### Serializing a json string from a non-default python type

```python
import jsonbind as jb
mydict = {"name":"German Espinosa","age":41,"weight":190.0}
print(jb.dumps(mydict), type(mydict))
mylist = [1, 2, 3, 4]
print(jb.dumps(mylist), type(mylist))
myint = 1
print(jb.dumps(myint), type(myint))
myfloat = 10.5
print(jb.dumps(myfloat), type(myfloat))
mystring = "Hello World"
print(jb.dumps(mystring), type(mystring))
mybool = True
print(jb.dumps(mybool), type(mybool))
```
output
```
{'name': 'German Espinosa', 'age': 41, 'weight': 190.0} <class 'dict'>
[1, 2, 3, 4] <class 'list'>
1 <class 'int'>
10.5 <class 'float'>
Hello World <class 'str'>
True <class 'bool'>
```

# JsonBind Object & List
JsonBind provides special implementations of Object and List datatypes that provide a lot of functionality to 
interact with data in JSON format.



## Create your first json object:
After installing the package, try the following python script:
```python 
import jsonbind as jb
myobject = jb.Object(name="German Espinosa", age=41, weight=190.0)
print("name:", myobject.name, type(myobject.name).__name__)
print("age:", myobject.age, type(myobject.age).__name__)
print("weight:", myobject.weight, type(myobject.weight).__name__)
print(myobject)
```
output
```
name: German Espinosa str
age: 41 int
weight: 190.0 float
{"name":"German Espinosa","age":41,"weight":190.0}
```
### Loading json_data:
To quickly load json data into objects, use the load command:
```python
import jsonbind as jb
myobject = jb.Object.load("{\"name\":\"German Espinosa\",\"age\":41,\"weight\":190.0}")

print("name:", myobject.name, type(myobject.name).__name__)
print("age:", myobject.age, type(myobject.age).__name__)
print("weight:", myobject.weight, type(myobject.weight).__name__)

```
output
```
name: German Espinosa str
age: 41 int
weight: 190.0 float
```
### Formatting outputs:
You can easily format data, even in complex json hierarchical structures:
```python
import jsonbind as jb
myobject = jb.Object.parse("{\"name\":\"German Espinosa\",\"age\":41,\"weight\":190.0,\"place_of_birth\":{\"country\":\"Argentina\",\"city\":\"Buenos Aires\"}}")

print(myobject.format("{name} was born in {place_of_birth.city}, {place_of_birth.country}"))

```
output
```
German Espinosa was born in Buenos Aires, Argentina
```
### Working with pre-structured data:
A powerful way to read and write json is to pre-define the structure of the data. This creates standarized data samples that are easire to be consumed by other tools.
To pre-define structure of a json object, you need to create your own custom class extending the JsonObject:
```python
import jsonbind as jb

class MyJsonClass(jb.Object):
    def __init__(self, name="", age=0, weight=0.0):
        self.name = name
        self.age = age
        self.weight = weight


myobject = MyJsonClass('German Espinosa', 41, 190.0)

json_string = str(myobject)

print(json_string)

```
output
```
{"name":"German Espinosa","age":41,"weight":190.0}
```

### Loading values into an existing object:
You can also load values from a json string directly into an existing custom JsonObject:
```python
import jsonbind as jb

class MyJsonClass(jb.Object):
    def __init__(self, name="", age=0, weight=0.0):
        self.name = name
        self.age = age
        self.weight = weight

myobject = MyJsonClass('German Espinosa', 41, 190.0)

myobject.parse("{\"name\":\"Benjamin Franklin\",\"age\":84,\"weight\":195.5}")

json_string = str(myobject)

print(json_string)

```
output
```
{"name":"Benjamin Franklin","age":84,"weight":195.5}
```


### Object to json conversion:

All objects with type MyJsonClass will produce perfectly formed json when converted to string.
If you need to retrieve the json string representing the object:
```python
import jsonbind as jb

class MyJsonClass(jb.Object):
    def __init__(self, name="", age=0, weight=0.0):
        self.name = name
        self.age = age
        self.weight = weight


myobject = MyJsonClass('German Espinosa', 41, 190.0)

json_string = str(myobject)

print (json_string)

```
output
```
{"name":"German Espinosa","age":41,"weight":190.0}
```
### Json to object conversion:
You can create instances of your json objects from strings containing a correct json representation:
```python
import jsonbind as jb

class MyJsonClass(jb.Object):
    def __init__(self, name="", age=0, weight=0.0):
        self.name = name     # string
        self.age = age       # int
        self.weight = weight # float


json_string = "{\"name\":\"German Espinosa\",\"age\":41,\"weight\":190.0}"

myobject = MyJsonClass.parse(json_string)

print("name:", myobject.name, type(myobject.name).__name__)
print("age:", myobject.age, type(myobject.age).__name__)
print("weight:", myobject.weight, type(myobject.weight).__name__)

```
output
```
name: German Espinosa str
age: 41 int
weight: 190.0 float
```
note: all members are populated with the right values using the same data type declared in the default constructor of the class

### Nested json structures:
You can create complex structures with nested objects:
```python
import jsonbind as jb

class Person(jb.Object):
    def __init__(self, name="", age=0):
        self.name = name
        self.age = age

class Transaction(jb.Object):
    def __init__(self, buyer=None, seller=None, product="", amount=0.0):
        self.buyer = buyer if buyer else Person()
        self.seller = seller if seller else Person()
        self.product = product
        self.amount = amount


mytransaction = Transaction(Person("German Espinosa", 41), Person("Benjamin Franklin", 84), "kite", 150.5)

print (mytransaction)

```
output
```
{"buyer":{"name":"German Espinosa","age":41},"seller":{"name":"Benjamin Franklin","age":84},"product":"kite","amount":150.5}
```

### Json lists:
You can load full lists with values from a json string to a JsonList:
```python
import jsonbind as jb

fibonacci = jb.List(list_type=int)

json_string = "[1,1,2,3,5,8,13,21]"

fibonacci.parse(json_string)

```
You can also load a list of json objects:
```python
import jsonbind as jb

class Person(jb.Object):
    def __init__(self, name="", surname=""):
        self.name = name
        self.surname = surname

person_list = jb.List(list_type=Person)

json_string = "[{\"name\":\"german\",\"surname\":\"espinosa\"},{\"name\":\"benjamin\",\"surname\":\"franklin\"}]"

person_list.parse(json_string)

```
Lists can also be used as members of other objects:
```python
import jsonbind as jb

class Person(jb.Object):
    def __init__(self):
        self.name = ""
        self.surname = ""
        self.languages = List(list_type=str)

person = Person.parse("{\"name\":\"German\",\"surname\":\"Espinosa\", \"languages\":[\"english\",\"spanish\",\"portuguese\"]}")

print(person)

```
output
```
{"name":"German","surname":"Espinosa","languages":["english","spanish","portuguese"]}
```