import functools
import inspect
from typing import Union

VERSION = "0.1.0"

class Model:
    def __init__(self) -> None:
        self.model = {}

    def _get(self, query:dict, model = {}):
        compiled_query = {}
        for key, value in query.items():
            if type(value) == dict:
                compiled_query[key] = self._get(value, model[key])
            elif type(value) == list:
                compiled_query[key] = model[key](*value)
            else:
                compiled_query[key] = value

        return compiled_query

    def get(self, query:dict):
        """
        Used to make queries to your `Model`.
        """
        return self._get(query, self.model)

        


#this is the decorator that serializes the Model
class ModelSerializer:
    def __init__(self) -> None:
        """
        Each Model requires a new `ModelSerializer`.
        """
        self._funcs = []

    def add(self, parent:list, key:Union[int, float, bool, None, str] = tuple()):
        """
        A decorator that adds a model endpoint/function inside the directory `parent` of the model with a key of `key`.
        """
        def inner(func):
            func._tagged = True
            func._parent = parent
            func._key = key
            return func
        return inner

    def sync(self, object:Model):
        """
        Must be called in your Model's `__init__` function after defining your `self.model`.
        You must pass in `self` as the object parameter.  The function call should look like this: `model_serializer_instance.sync(self)`
        """
        for method_name in dir(object):
            method = getattr(object, method_name)
            if hasattr(method, '_tagged'):
                pointer = object.model
                for index in method._parent:
                    pointer = pointer[index]
                pointer[method._key] = method
