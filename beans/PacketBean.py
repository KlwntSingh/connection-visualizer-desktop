class Packet():

    def __init__(self, systemIP=None, communicatingIP=None, protocol=None, trafficDirection=None, systemMacAddress=None, communicatingMacAddress=None):
        self.systemIP = systemIP
        self.communicatingIP = communicatingIP
        self.protocol = protocol
        self.trafficDirection = trafficDirection
        self.systemMacAddress = systemMacAddress
        self.communicatingMacAddress = communicatingMacAddress
        self.domain_name = ''
        self.request_fired = False
        self.interface = ''
