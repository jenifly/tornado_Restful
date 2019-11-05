class Cache:
    def __init__(self):
        self._cache = {}

    def refresh(self, name, value):
        if name not in self._cache:
            return
        self._cache[name] = value

    def clear(self, name):
        if name not in self._cache:
            return
        del self._cache[name]
    
    def clear_all(self):
        self._cache = {}

    def __getattr__(self, name):
        try:
            return self._cache[name]
        except KeyError:
            raise AttributeError

    def __setattr__(self, name, value):
        if name == '_cache':
            super().__setattr__(name, value)
        else:
            self._cache[name] = value

cache = Cache()