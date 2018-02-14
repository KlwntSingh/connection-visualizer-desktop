from netifaces import interfaces, ifaddresses, AF_INET, AF_PACKET

def get_list_of_interfaces():
    return interfaces()

def get_interface_info(interface):
    print(ifaddresses(interface).setdefault(AF_INET))
    return {
        "system_ip_address" : ifaddresses(interface).setdefault(AF_INET)[0]['addr'],
        "system_mac_address" : ifaddresses(interface).setdefault(AF_PACKET)[0]['addr']
    }

