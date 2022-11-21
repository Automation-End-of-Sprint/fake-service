"""A class for creating custom warning
"""


class PropertyWarning:

    def __init__(self, warningName, warningDesc):
        self.warningName = warningName
        self.warningDesc = warningDesc

    # Property that is missing
    def setWarningName(self, warningName):
        self.warningName = warningName

    def getWarningName(self):
        return self.warningName

    # Description of where, what, how is missing
    def setWarningDesc(self, warningDesc):
        self.warningDesc = warningDesc

    def getWarningDesc(self):
        return self.warningDesc

    def __str__(self):
        warningOutput = "WARNING: " + self.warningName + "- " + self.warningDesc
        return warningOutput
