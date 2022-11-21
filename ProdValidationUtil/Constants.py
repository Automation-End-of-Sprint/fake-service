from enum import Enum

"""A class that enumerates all of the environment that are available for deployment.
    Specification of what environments must be check is completed within main.py
"""


class EnvironmentType(Enum):
    NA = "not-assigned"
    UAT1Develop = "uat1"
    UAT2Develop = "uat2"
    UAT3Develop = "uat3"
    UAT4Develop = "uat4"
    MASTERProps = " master"
    PRODMaster = "prod"
    PRODAPMaster = "prod-ap"


class ValidationEnvConstants(Enum):
    TRAIN = "trn"
    DEVELOPBaseProperties = "develop"
    MASTERBaseProperties = "master"
    PROD = "prod"
    PRODAP = "prod-ap"


class ServiceName(Enum):
    TEST1 = "test-1"
    TEST2 = "test-2"
    COCStag2Ledger = "accums-batch-coc-stagtoldgr"
    COBCalculations = "cob-calculations"
    COBAudit = "cob-audit"
    COBEvaluation = "cob-evaluation"
