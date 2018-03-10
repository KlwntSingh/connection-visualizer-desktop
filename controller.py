
import sys
import os

from config.config import CONFIG
from core.ThreadFactory import ThreadFactory as tf
from core.ExpiringDictionary import ExpiringDictionary

"""
This module is interface between backend application i.e business logic and Graphical user interface
Reason: Don't want to import any business logic service inside of gui. Hence this bridge is created.
Baically This file is just dictionary of services which is populated by backend application and used by GUI
"""

def close():
    sys.exit()

def appversion():
    return CONFIG["VERSION"]

def authorinfo():
    return CONFIG["AUTHOR"]

# This feature is not complete yet
def restart_with_root():
    # python = sys.executable
    # actFil= sys.argv[0]
    # neargs=python, os.getcwd() + "/" + actFil
    # os.execl("sudo", *neargs)
    pass

# This object is like controller
services = {
    "close": close,
    "appversion" : appversion,
    "authorinfo": authorinfo,
    "restart_with_root" : restart_with_root
}

# Generic
def addService(fn, fn_name=None):
        if fn_name:
            services[fn_name] = fn
        else:
            services[fn.__name__] = fn
