from netifaces import interfaces, ifaddresses, AF_INET, AF_PACKET

def get_list_of_interfaces():
    return interfaces()

def get_all_interfaces():
    rTurn = dict()
    for i in interfaces():
        rs = get_interface_info(i)
        if rs:
            rTurn[i] = rs
    return rTurn

def get_interface_info(interface):
    if ifaddresses(interface).setdefault(AF_INET):
        return {
            "system_ip_address" : ifaddresses(interface).setdefault(AF_INET)[0]['addr'],
            "system_mac_address" : ifaddresses(interface).setdefault(AF_PACKET)[0]['addr']
        }
    else:
        {}

