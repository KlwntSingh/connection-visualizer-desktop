import os

import controller
from services import InterfaceService
from services.LoggerService import Logger
import gui
import services.ControllerServices as ControllerServices

# pending feature
if os.getuid() != 0:
    pass



root = gui.render_frame()

logger = Logger.getLogger()

logger.info("Application started")

controller.addService(ControllerServices.createSnifferAndIPRequesterThread, fn_name='startSnifferThread')
controller.addService(ControllerServices.stopSnifferAndIPRequesterThread, fn_name='stopSnifferThread')
controller.addService(ControllerServices.block_ip_address)
controller.addService(InterfaceService.get_list_of_interfaces, "list_of_interfaces")

gui.render_content(root)