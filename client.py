from suds.client import Client
import logging
logging.getLogger('suds.client').setLevel(logging.CRITICAL)

class User(object):
    def __init__(self):
        self._client=Client('http://localhost:1234/?wsdl')

    def compile(self,lang,code,private):
        return self._client.service.compile(lang,code,private)
