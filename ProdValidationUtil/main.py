#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A class that will hold all pertinent information relating to the service
    Each instation of the class service will be made for branch of service.
        - For example uat1, prod, prod-ap, or base service properties on master
"""
import Constants
from Constants import ServiceName
from ProdValidationUtil import validateServiceGroupQueue, createServiceGroup
from Service import Service
from ServiceGroup import ServiceGroup
from PropertyWarning import PropertyWarning
from PropertyError import PropertyError
from pathlib import Path


# Starting point into application.
if __name__ == '__main__':

    # In this case TEST would be replaced by full branch name such as cob-banking-calculation-service
    # And the environment provided is the base point for comparison
    testServiceGroup1 = createServiceGroup(ServiceName.TEST1.value, Constants.EnvironmentType.UAT1Develop)
    testServiceGroup2 = createServiceGroup(ServiceName.TEST2.value, Constants.EnvironmentType.UAT1Develop)

    validationQueue = [testServiceGroup1, testServiceGroup2]

    validateServiceGroupQueue(validationQueue)
