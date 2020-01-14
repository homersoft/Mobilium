from os import path

INTERNAL_PROJECT_DIR = '../MobiliumDriver/'
EXTERNAL_PROJECT_DIR = 'mobilium/MobiliumDriver/'
PROJECT_NAME = 'MobiliumDriver.xcodeproj'
SCHEME = 'MobiliumDriver'
CARTHAGE_DIR = 'Carthage'


def get_project_dir():
    if path.exists(INTERNAL_PROJECT_DIR):
        return INTERNAL_PROJECT_DIR
    return EXTERNAL_PROJECT_DIR
