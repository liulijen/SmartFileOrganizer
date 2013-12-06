from os import listdir, getcwd
from os.path import isfile, join
import os
import sys
import re
import shutil
mypath = "."
profileName = ".tidyrc"
def getCWFiles(path):
    onlyfiles = [f for f in listdir(path) if isfile(join(path,f))]
    return onlyfiles
def readConfig(path):
    try:
        fd=open(path,"r")
        lines = fd.read().strip().split('\n')
        return lines
    except IOError:
        sys.exit("[Error] Configuration not found. Need \""+profileName+"\"")

def runConfig(configList,fileList):
    print "Now working on: "+getcwd()
    print "Config List:"
    print configList
    # Avoid move the profile
    fileList.remove(profileName)
    print "File List"
    print fileList
    # Create folder
    folders=[]
    for config in configList:
        if config.find('->')<0:
            if os.path.isdir(config) == True:
                print config+" existed"
            else:
                print config+" not existed"
                os.makedirs(config)
                print config+" created."
            folders.append(config)

    # Move file
    for config in configList:
        if config.find('->')>0:
            regexp = config.strip().split('->')[0].strip()
            folder = config.strip().split('->')[1].strip()
            p = re.compile(regexp)
            # Copy list by value
            tmpList = fileList[:]
            for f in fileList:
                if p.match(f):
                    if folder in folders:
                        print "Move "+f+" to "+folder
                        shutil.move(f, folder)
                        # Since the file has been moved, delete it from list
                        tmpList.remove(f)
                    else:
                        print "Move "+f+" ...Target folder "+folder+" is not defined.Skip."
                #else:
                   # print f+ " not match rule "+regexp
            fileList=tmpList

runConfig(readConfig(profileName),getCWFiles(mypath))
