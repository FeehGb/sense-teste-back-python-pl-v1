class Utils:
    @classmethod
    def extractasdict(cls, arroba_key, data):
        return {key.replace(arroba_key+":", ''): value for key, value in data.items() if key.startswith(arroba_key)}
        
    @classmethod
    def extractaslist(cls, arroba_key, data):
        return [{"path": key.replace(arroba_key+":", ''), 'value':value} for key, value in data.items() if key.startswith(arroba_key)]
        
        
    @staticmethod
    def read_file(path ="",flag = "r", encoding='utf8') :
        return Utils.__handle_file(handle="read", path =path,flag = flag, encoding=encoding)
        
    
    @staticmethod
    def write_file(data="", path="", flag = "w+", encoding='utf8') :
        return Utils.__handle_file(handle = "write",data=data, path =path,flag = flag, encoding=encoding)
        
    
    @classmethod
    def __handle_file(cls, **kwargs) :
        try:
            with open(kwargs['path'] , kwargs['flag'], encoding=kwargs['encoding']) as file:
                if kwargs['handle'] == 'read':
                    return True, file.read() 
                elif kwargs['handle'] == 'write':
                    return True, file.write(kwargs['data'])
                else:
                    pass
                    
        except IOError as error:
            return None, error
        
    
    @staticmethod
    def md5(text) :
        import hashlib

        md5 = hashlib.md5(text.encode('utf-8'))
        return md5.hexdigest()
        
    @staticmethod
    def get_index(arr:list, index:int, fallback=None) :
        try:
            return arr[index]
        except :
            return fallback
    
    
