import os

import controller
from services import InterfaceService
from services.LoggerService import Logger
#import initialization

import gui

# pending feature
if os.getuid() != 0:
    pass



root = gui.render_frame()

from services.SnifferService import Sniffer
from services.IPInfoService import IPInfo
import services.ControllerServices as ControllerServices
logger = Logger.getLogger()

logger.info("Application started")

controller.addService(ControllerServices.createSnifferAndIPRequesterThread, fn_name='startSnifferThread')
controller.addService(ControllerServices.stopSnifferAndIPRequesterThread, fn_name='stopSnifferThread')

controller.addService(InterfaceService.get_list_of_interfaces, "list_of_interfaces")

gui.render_content(root)


