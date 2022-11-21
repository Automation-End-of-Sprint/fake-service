"""
The utility that accomplishes creation, population, and validation of services and service groups,
"""
import os

import Constants
from Service import Service
from ServiceGroup import ServiceGroup
from PropertyWarning import PropertyWarning
from PropertyError import PropertyError
from pathlib import Path


# Passed 4 Service Objects that are each holding a populated dictionary
# with all properties and values mapped
def validateServiceGroup(serviceGroup):
    baselineEnvService = None  # service-uatN.prop
    trnEnvService = None  # service-trn.prop
    developBaseService = None  # Develop.prop
    masterBaseService = None  # Master.prop
    prodEnvService = None
    prodAPEnvService = None

    # Loop through and create proper local variables
    for service in serviceGroup.serviceGroupList:
        if service.environmentType == serviceGroup.serviceEnvBaseline:
            baselineEnvService = service
        elif service.environmentType == Constants.ValidationEnvConstants.TRAIN:
            trnEnvService = service
        elif service.environmentType == Constants.ValidationEnvConstants.DEVELOPBaseProperties:
            developBaseService = service
        elif service.environmentType == Constants.ValidationEnvConstants.MASTERBaseProperties:
            masterBaseService = service
        elif service.environmentType == Constants.ValidationEnvConstants.PROD:
            prodEnvService = service
        elif service.environmentType == Constants.ValidationEnvConstants.PRODAP:
            prodAPEnvService = service
        else:
            serviceGroup.putWarningInList(Warning("Validation Config", "Not all services in serviceGroupList aligned with "
                                                               "current setup. Ensure settings are correct and "
                                                               "reattempt run"))

    # Now that local service objects are made check with the following logic
    # Find set of properties in which the following condition is satisfied (Each is their own step)
    # PART 1: Validate baseline with prod, prod-ap, master.properties
    # 1) Exists within BASELINE but not within prod    ==> Output list
    baselineVSProdCompareResults = set(baselineEnvService.propertiesDict) - set(prodEnvService.propertiesDict)
    # 2) Exists within BASELINE but not within prod-ap ==> Output list
    baselineVSProdAPCompareResults = set(baselineEnvService.propertiesDict) - set(prodAPEnvService.propertiesDict)
    # 3) With these two list remove redundant and check both against master.properties ==> Output list
    step1ResultsVSProp = set(baselineVSProdCompareResults) - set(masterBaseService.propertiesDict)
    step2ResultsVSProp = set(baselineVSProdAPCompareResults) - set(masterBaseService.propertiesDict)
    # If empty set then all good
    # If non-empty set report errors/warnings
    # Python way of saying if either of these list are populated then ...
    # TODO most likely want to make this error message stronger/easier to track but for now good\
    if step1ResultsVSProp:
        for errorProd in step1ResultsVSProp:
            serviceGroup.putErrorInList(
                PropertyError(errorProd, service.serviceName + "Missing the following property that exist within UAT1 "
                                         "but not prod "))

    if step2ResultsVSProp:
        for errorProdAP in step2ResultsVSProp:
            serviceGroup.putErrorInList(
                PropertyError(errorProdAP, service.serviceName + "Missing the following property that exist within "
                                                                 "UAT1 but not prod-ap "))

    # PART 2: Validate TRN is updated with UAT1
    # 1) Exists within UAT1 and TRN ==> Output list
    baselineEnvVSTRN = set(baselineEnvService.propertiesDict) - set(trnEnvService.propertiesDict)
    if baselineEnvVSTRN:
        for errorTRN in baselineEnvVSTRN:
            serviceGroup.putErrorInList(PropertyError("Service: " + service.serviceName + ": ", "Missing " + errorTRN +
                                                                                    " from TRN but exist within UAT1"))

    # PART 3: Validate master.properties VS develop.properties
    # 1) Find values missing within Master ==> Output list
    masterPropVSDevProp = set(developBaseService.propertiesDict) - set(masterBaseService.propertiesDict)
    # 2A) Compare OutputList against PROD
    missingInMasterAndProd = masterPropVSDevProp - set(prodEnvService.propertiesDict)
    # 2B) Compare OutputList against PROD-AP
    missingInMasterAndProdAP = masterPropVSDevProp - set(prodAPEnvService.propertiesDict)

    if missingInMasterAndProd:
        for errorMasterProd in missingInMasterAndProd:
            serviceGroup.putErrorInList(
                PropertyError(errorMasterProd, service.serviceName + "Missing the following property that exist "
                                                                     "within Develop"))
    if missingInMasterAndProdAP:
        for errorMasterAP in missingInMasterAndProdAP:
            serviceGroup.putErrorInList(
                PropertyError("Service: " + service.serviceName + ":", "Missing" + errorMasterAP + "the following "
                                                                                                   "property that "
                                                                                 "exist within Master"))


# Dictionary population in the format
# Key   = anything before equal sign
# Value = anything after equal sign
def populatePropDictionary(serviceGroup):
    for service in serviceGroup.serviceGroupList:
        with open(service.filePath, "r") as fp:
            for line in fp:
                if line[0].isalnum():
                    # Start inserting into dictionary after parsing and cleansing data
                    line.rstrip()
                    lineArray = line.split("=")
                    if (lineArray[0]) in service.propertiesDict.keys():
                        # Add error for duplicate property
                        pass
                    else:
                        # Insert into dictionary if key does not exist
                        service.propertiesDict.update({lineArray[0]: lineArray[1]})


def createFilePath(serviceList):
    for service in serviceList:
        #bashScript = "ls develop/"
        #os.system(bashScript)
        if service.environmentType == Constants.EnvironmentType.NA:
            pass  # TODO Might want to reorganize this but for now it works
        elif service.environmentType == Constants.ValidationEnvConstants.TRAIN:
            filePath = Path(
                "./develop/" + service.serviceName + "/" + service.serviceName + "-" + service.environmentType.value + ".properties")
            service.setFilePath(filePath)
        elif service.environmentType == Constants.ValidationEnvConstants.DEVELOPBaseProperties:
            filePath = Path("./develop/" + service.serviceName + "/" + service.serviceName + ".properties")
            service.setFilePath(filePath)
        elif service.environmentType == Constants.ValidationEnvConstants.MASTERBaseProperties:
            filePath = Path("./master/" + service.serviceName + "/" + service.serviceName + ".properties")
            service.setFilePath(filePath)
        elif service.environmentType == Constants.ValidationEnvConstants.PROD or service.environmentType == Constants.ValidationEnvConstants.PRODAP:
            filePath = Path(
                "./master/" + service.serviceName + "/" + service.serviceName + "-" + service.environmentType.value + ".properties")
            service.setFilePath(filePath)
        else:
            filePath = Path(
                "./develop/" + service.serviceName + "/" + service.serviceName + "-" + service.environmentType.value + ".properties")
            service.setFilePath(filePath)


def createServiceGroup(serviceName, baselineEnv):
    tempServiceGroup = ServiceGroup(serviceName)
    tempServiceGroup.setServiceEnvBaseline(baselineEnv)
    baselineService = Service(serviceName)
    baselineService.setEnvironmentType(baselineEnv)
    tempServiceGroup.putServiceInList(baselineService)
    for envConstant in Constants.ValidationEnvConstants:
        tempServiceName = Service(serviceName)
        tempServiceName.setEnvironmentType(envConstant)
        tempServiceGroup.putServiceInList(tempServiceName)
    return tempServiceGroup


def outputServiceGroupResults(validatedServiceGroup):
    # results will be held in two spots within a validated service group
    # - List of Warnings
    # - List of Errors
    if validatedServiceGroup.errorList or validatedServiceGroup.warningList:
        for error in validatedServiceGroup.errorList:
            print(error)
        for warning in validatedServiceGroup.warningList:
            print(warning)
    else:
        print("SUCCESS: " + validatedServiceGroup.serviceName)


def validateServiceGroupQueue(serviceGroupQueue):
    for serviceGroup in serviceGroupQueue:
        # The main logic driver portion
        # 1) Create file path string from given information of service and env.
        createFilePath(serviceGroup.serviceGroupList)
        # 2) Populate the service object dict with above method
        populatePropDictionary(serviceGroup)
        # 3) Once all 4 dictionaries are populated compare them using above method
        validateServiceGroup(serviceGroup)
        # 4) Output results
        outputServiceGroupResults(serviceGroup)

