class Packet():
    """
    This is Packet bean.
    Packet bean is used in whole application flowing from one service to another
    """
    def __init__(self, systemIP=None, communicatingIP=None, protocol=None, trafficDirection=None, systemMacAddress=None, communicatingMacAddress=None):
        self.systemIP = systemIP
        self.communicatingIP = communicatingIP
        self.protocol = protocol
        self.trafficDirection = trafficDirection
        self.systemMacAddress = systemMacAddress
        self.communicatingMacAddress = communicatingMacAddress
        self.domain_name = '-'
        self.country = 'fetching.....'
        self.state = 'fetching.....'
        self.region = 'fetching.....'
        self.request_fired = False
        self.interface = ''
