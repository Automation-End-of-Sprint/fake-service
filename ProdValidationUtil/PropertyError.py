"""A class for creating custom warning
"""


class PropertyError:

    def __init__(self, errorName, errorDesc):
        self.errorName = errorName
        self.errorDesc = errorDesc

    # Property that is missing
    def setErrorName(self, errorName):
        self.errorName = errorName

    def getErrorName(self):
        return self.errorName

    # Description of where, what, how is missing
    def setErrorDesc(self, errorDesc):
        self.errorDesc = errorDesc

    def getErrorDesc(self):
        return self.errorDesc

    def __str__(self):
        errorOutput = "ERROR: " + self.errorName + "- " + self.errorDesc
        return errorOutput
