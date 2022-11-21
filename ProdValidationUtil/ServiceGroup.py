"""A class that will hold all pertinent information relating to the service
  group being tested
  Each service group will hold the following things
    - The service name being validated
    - A list of service object for each env (Baseline, TRN, Develop.properties, Master.Properties PROD, PROD-AP)
"""
import Constants


class ServiceGroup:

    def __init__(self, serviceName):
        self.serviceName = serviceName
        self.serviceGroupList = []
        self.serviceEnvBaseline = None
        # Key  : Property
        # Value: Value held on right of "="
        # Two list that can be utilized to hold errors and warnings
        self.errorList = []
        self.warningList = []

    def setServiceName(self, serviceName):
        self.serviceName = serviceName
    def getServiceName(self):
        return self.serviceName
    def setServiceEnvBaseline(self, serviceEnvBaseline):
        self.serviceEnvBaseline = serviceEnvBaseline
    def getServiceEnvBaseline(self):
        return self.serviceEnvBaseline


    def putServiceInList(self, serviceObject):
        self.serviceGroupList.append(serviceObject)
    def getServiceList(self):
        return self.serviceGroupList

    def putWarningInList(self, warning):
        self.warningList.append(warning)
    def getWarningList(self):
        return self.warningList

    def putErrorInList(self, error):
        self.errorList.append(error)
    def getErrorList(self):
        return self.errorList


    def __str__(self):
        #serviceNameOutput = "ServiceName: " + self.serviceName.value
        #envTypeOutput = "EnvironmentType: " + self.environmentType.value
        filePathOutput = "filePath: " + self.filePath
        return filePathOutput #serviceNameOutput + envTypeOutput #+
