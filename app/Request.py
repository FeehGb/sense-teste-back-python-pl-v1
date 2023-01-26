
from time import sleep
import requests, string, jsonmerge, abc
from .Utils import Utils


class Body:
    """TYPE BODY"""
    
    
class Params:
    """TYPE PARAMS"""

class Path:
    """Type Path"""
    
    
class Method:
    """Type Method"""
    


class Json(object):
    """ def __init__(self, function):
        self.function = function """
        
    def __call__(self, *param_arg):
        #if len(param_arg) == 1:
        def wrapper( *args, **kwargs):
            response = param_arg[0](*args, **kwargs)
            try:
                if response.ok:
                    return response.json()
                return {}
            except: return {}
        return wrapper


class Response_handler(object):
    def __init__(self, function):
        self.function = function
        
    def __call__(self, *param_arg):
        if len(param_arg) == 1:
            def wrapper( *args, **kwargs):
                response = param_arg[0]( *args, **kwargs)
                return self.function(response)
            return wrapper
            
    @property
    def output(self):
        return self.__output
        
        
    @output.setter
    def output(self, value):
        self.__output = value
        
        
class Pagination(object):
    def __init__(self, function) :
        self.pagination = function
        
    def __call__(self, *param_arg):
        if len(param_arg) == 1:
            def wrapper( *args, **kwargs):
                response = param_arg[0]( *args, **kwargs)
                if not response.ok :
                    #self.createLog(response.status_code,f"Erro ao pegar dados: {rote}")
                    return []
                    
                data = response.json()
                if not data : return []
                """ afterGet_data = self.call("afterGet_" + self.fixed_rote(), data)
                if afterGet_data != None:
                    data = afterGet_data
                    """
                next_page = False
                if callable(self.pagination):
                    next_page = self.pagination(response, data)
                    #next_page = self.call("pagination_rules", response, data)
                    
                
                if next_page:
                    data = data + param_arg[0]( *args, **kwargs)
                    
                
                return data 
                
                
            return wrapper
        
    
class Throttling(object):
    def __init__(self, function):
        self.throttling_rules = function
        
    def __call__(self, *param_arg):
        if len(param_arg) == 1:
            def wrapper( *args, **kwargs):
                throttling_time = 0
                while True:
                    response    =  param_arg[0]( *args, **kwargs)
                    if callable(self.throttling_rules):
                        throttling_time = self.throttling_rules(response)
                        
                    if not throttling_time :
                        break
                        
                    sleep(throttling_time)
                    
                return response 
            return wrapper
    
        
class Request(object):
    default_params = {}
    def __init__(self, route, **deco_kwarg):
        self._route  = route
        self._kwargs = deco_kwarg
        
    
    def update_dafault_params(self, value):
        self.default_params = jsonmerge.merge(self.default_params, value)
        
    
    def __join_json(self, _list):
        out = {}
        for item in _list:
            out = jsonmerge.merge(out, item)
            
        return out
            
        
    
    def __valid_types(self, kwargs, fn):
        
        __annotations__      = fn.__annotations__
        __annotations__items = __annotations__.items()
        for _key, _type in __annotations__items :
            exist_key = kwargs.get(_key)
            if exist_key is None:
                raise Exception(f"Key Error: '{_key}' type: {_type.__name__} is Required")
                
            
        for _key, _type in kwargs.items() :
            exist_key = __annotations__.get(_key)
            if not exist_key:
                raise Exception(f"Key Error: '{_key}' Not Found")
                
            
        return {
                "Params": {_key: kwargs.get(_key)  for _key, _type in __annotations__items if _type == Params }
            ,   "Path"  : {_key: kwargs.get(_key)  for _key, _type in __annotations__items if _type == Path }
            ,   "Body"  : self.__join_json([  kwargs.get(_key)  for _key, _type in __annotations__items if _type == Body])
            ,   "Method": [  kwargs.get(_key)  for _key, _type in __annotations__items if _type == Method]
        }
        
        
        
    def __call__(self, *param_arg):
        if len(param_arg) == 1:
            def wrapper(*args, **kwargs):
                kwargs_checked = self.__valid_types(kwargs, param_arg[0])
                
                _params = jsonmerge.merge(self.default_params, self._kwargs)
                Params  = jsonmerge.merge(kwargs_checked.get('Params', {}), _params.get('params', {}))
                Path    = kwargs_checked.get('Path',{})
                Body    = kwargs_checked.get('Body',{})
                Method  = Utils.get_index(kwargs_checked.get('Method'), -1, _params.get('method', 'GET'))
                
                if 'method' in _params:
                    del _params['method']
                    
                if 'params' in _params:
                    del _params['params']
                    
                
                return self.run_request(route=self._route, url_format=Path, params=Params, data=Body, method=Method, **_params)
            return wrapper
        
    
    def run_request(self, **kwargs):
        self.response = None
        params = self.__handle_arguments(**kwargs)
        
        try:
            self.response = requests.request(**params)
        except Exception as error:
            raise Exception(str(error))
        
        #self.params = {}
        return self.response
        
    
    def __handle_arguments(self, **kwargs):
        request_kwargs = kwargs
        #request_kwargs = self.__merge_params(kwargs, request_kwargs)
        
        base_url = request_kwargs.get('base_url')
        if not base_url and 'route' in request_kwargs and not 'url' in request_kwargs :
            raise Exception ("Need to set a base_url or url")
            
        
        if 'route' in request_kwargs :
            request_kwargs['url'] = base_url + request_kwargs['route']
            
        
        format_string_in_url = [tup[1] for tup in string.Formatter().parse(request_kwargs['url']) if tup[1] is not None]
        if 'url_format' in request_kwargs and request_kwargs['url_format'] and format_string_in_url:
            for format_string in format_string_in_url:
                if format_string not in request_kwargs['url_format']:
                    raise Exception(f"Key Error: '{format_string}' not founded")
            else:
                request_kwargs['url'] = request_kwargs['url'].format(**request_kwargs['url_format'])
                
        elif request_kwargs.get('url_format') and not format_string_in_url:
            raise Exception(f"Key Error: '{', '.join(request_kwargs['url_format'].keys())}' not in URL")
            
        
        return {
                "method"            :   request_kwargs.get('method')
            ,   "url"               :   request_kwargs.get('url')
            ,   "params"            :   request_kwargs.get('params')
            ,   "data"              :   request_kwargs.get('data')
            ,   "headers"           :   request_kwargs.get('headers')
            ,   "cookies"           :   request_kwargs.get('cookies')
            ,   "files"             :   request_kwargs.get('files')
            ,   "auth"              :   request_kwargs.get('auth')
            ,   "timeout"           :   request_kwargs.get('timeout')
            ,   "allow_redirects"   :   request_kwargs.get('timeout', True)
            ,   "proxies"           :   request_kwargs.get('proxies')
            ,   "hooks"             :   request_kwargs.get('hooks')
            ,   "stream"            :   request_kwargs.get('stream')
            ,   "verify"            :   request_kwargs.get('verify')
            ,   "cert"              :   request_kwargs.get('cert')
            ,   "json"              :   request_kwargs.get('json')
            
            
            
        }
        
