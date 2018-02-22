from netifaces import interfaces, ifaddresses, AF_INET, AF_PACKET

def get_list_of_interfaces():
    """
    Returns list of interfaces
    :return:
    """
    return interfaces()

def get_all_interfaces():
    """
    Returns Interfaces map with interface name as key and it's ip and map address as value
    :return:
    """
    rTurn = dict()
    for i in interfaces():
        rs = get_interface_info(i)
        if rs:
            rTurn[i] = rs
    return rTurn

def get_interface_info(interface):
    """
    Returns ip and mac address of interface passed as argument
    :param interface:
    :return:
    """
    if ifaddresses(interface).setdefault(AF_INET):
        return {
            "system_ip_address" : ifaddresses(interface).setdefault(AF_INET)[0]['addr'],
            "system_mac_address" : ifaddresses(interface).setdefault(AF_PACKET)[0]['addr']
        }
    else:
        {}

