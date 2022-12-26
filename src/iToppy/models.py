from enum import Enum
from typing import Iterator, List, Union, Tuple, AbstractSet
from .exceptions import (
    InvalidResponseException
)
from dataclasses import dataclass

class iStatusCode(Enum):
    """iTop Rest API Error Codes"""
    OK = 0
    UNAUTHORIZED = 1
    MISSING_VERSION = 2
    MISSING_JSON = 3
    INVALID_JSON = 4
    MISSING_AUTH_USER = 5
    MISSING_AUTH_PWD = 6
    UNSUPPORTED_VERSION = 10
    UNKNOWN_OPERATION = 11
    UNSAFE = 12
    INTERNAL_ERROR = 100

class iAuth(Enum):
    """Set the authentication method for the connection with this object"""
    FORM = 1
    BASIC = 2

@dataclass
class iResponse:
    """Base iTop response class"""
    code: int
    message: str
    
    @classmethod
    def from_response(cls, response: dict):
        if "code" not in response:
            raise InvalidResponseException("Invalid response returned from iTop: " + str(response))

        if response['code'] == 0:
            if response.get('objects', False) is None:
                return iEmptyResponse(0, "")
        
            return iSuccessfulResponse.MakeModel(**response)

        return iUnsuccessfulResponse(iStatusCode(response['code']), response['message'], str(response))

@dataclass
class iSuccessfulResponse(iResponse):
    num_results: int
    objects: List["iObject"]
    page: int = None
    limit: int = None
    __iterator: Iterator["iObject"] = None
    
    @classmethod
    def MakeModel(cls, **kwargs):
        custom_types = {}
        new_obj = []
        
        for obj in kwargs['objects'].values():
            if custom_types.get(obj['class'], None) is None:
                custom_types[obj['class']] = iObject.MakeCustom(obj['class'], obj)
            
            fields = {**obj['fields'], **{'id': obj['key']}}

            new_obj.append(custom_types[obj['class']](fields))

        kwargs['objects'] = new_obj
        kwargs['num_results'] = len(kwargs['objects'])

        return cls(**kwargs)

    def __post_init__(self):
        self.__iterator = iter(self.objects)
    
    def get_one(self):
        try:
            return next(self.__iterator)
        except StopIteration:
            return None
    
    def get_all(self):
        return self.objects

@dataclass
class iEmptyResponse(iResponse):
    pass

@dataclass
class iUnsuccessfulResponse(iResponse):
    code: iStatusCode
    data: str

class iObject:
    """iTop Object Class"""
    @staticmethod
    def create(cls, itop_class: str, fields: dict, key: str = "id"):
        pass
        
    @staticmethod
    def custom_init(self, kwargs):
        for key, arg in kwargs.items():
            setattr(self, key, arg)

    @staticmethod
    def MakeCustom(name: str, kwargs: dict):
        kwargs['__init__'] = iObject.custom_init
        fields = {**{x: None for x in kwargs['fields'].keys()}, **{'id': None, '__init__': iObject.custom_init}}
        # new_cls = type(name, (iObject,), {x: None if x != '__init__' else kwargs[x] for x in kwargs.keys()})
        new_cls = type(name, (iObject,), fields)
        return new_cls

    def __init__(**kwargs):
        super().__init__(id=kwargs.pop('id', None))

@dataclass
class iOperation:
    verb: str
    extension: str = None
    description: str = None

@dataclass
class iOQLBuilder:
    """iTop OQL Query Class Builder"""
    itop_object: str
    wheres: List[Union[List[str], tuple[str], AbstractSet[str]]]
    
    @staticmethod
    def get_where(attr: str, operator: str, value: Union[str, int]) -> str:
        if isinstance(value, str):
            value = f"'{value}'"
        
        return f"{attr} {operator} {value}"
    
    def __str__(self):
        return f"SELECT {self.itop_object} {' AND '.join([self.get_where(**x) for x in self.wheres])}"
    
    def add_condition(self, attribute: str, value: Union[str, int], operator: str = '='):
        self.wheres.append((attribute, operator, value))
        
