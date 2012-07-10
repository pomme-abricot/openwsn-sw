import logging
import JSONWrapper
class NullHandler(logging.Handler):
    def emit(self, record):
        pass
log = logging.getLogger('CoapHeader')
log.setLevel(logging.ERROR)
log.addHandler(NullHandler())

class CoapHeader:

    #Version
    def getVersion(self):
        return self._version

    def setVersion(self, version):
        self._version = version

    #Type
    def getType(self):
        return self._type

    def setType(self, type):
        self._type = type

    #Option
    def getOption(self):
        return self._option

    def setOption(self, option):
        self._option = option

    #Code
    def getCode(self):
        return self._code

    def setCode(self, code):
        self._code = code
   
    #Code
    def getMID(self):
        return self._mId

    def setMID(self, mId):
        self._mId = mId
    
    #OptionList
    def getOptionList(self):
        return self._optionList

    def setOptionList(self, optionList):
        self._optionList = optionList      

#TODO check this error
#File " ..... /software/openEndPoint/bin/EpLayerdebugCli/../../epparser/CoapHeader.py", line 62, in __repr__
#return self.toJSON(self)
#TypeError: toJSON() takes exactly 1 argument (2 given)

    def toJSON(self):
        json=JSONWrapper.JSONWrapper()
        return json.json_repr(self)

    def __str__( self ):
       return self.toJSON()

       
    