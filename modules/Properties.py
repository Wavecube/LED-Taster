from os.path import join
from os import listdir


class Properties:

    properties = {}
    __defaults = {}

    def __init__(self, args, defaults=None):
        if defaults is not None:
            self.__defaults = defaults

        for kv in args:
            if "=" in kv:
                (key, value) = kv.split("=")
                self.properties[key] = value
        

    def get(self, key):
        return self.properties.get(key) if key in self.properties else self.__defaults.get(key) if key in self.__defaults else None
    
    def promptL(self, key, seperator=",", strip=False):
        result = input(self.get(key)).split(seperator)
        if strip: result = [rs.strip() for rs in result]
        return result

class Lang(Properties):
    
    def __init__(self, language):
        self._language = language
        file = open(join("lang", self._language))
        super().__init__(file)
    
    def get(self, key, **replace):
        result = super(Lang, self).get(key) 
        for unchanged, replacement in replace.items(): result = result.replace("%%%s%%" % unchanged, replacement)
        return result.replace("%n", "\n")

    def toString(self):
        return self._language

    @staticmethod
    def listLangs():
        return listdir("lang")

    @staticmethod
    def langsToString():
        langs = Lang.listLangs()
        result = ""
        for lang in langs:
            if lang is not langs[0]: result += ", %s" % lang
            else: result = lang
        return result
