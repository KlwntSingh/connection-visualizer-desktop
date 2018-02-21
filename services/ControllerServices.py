from config.config import CONFIG
from core.ThreadFactory import ThreadFactory as tf
from core.ExpiringDictionary import ExpiringDictionary
from services.SnifferService import Sniffer
from services.IPInfoService import IPInfo
import services.IPTables as iptables

def block_ip_address(packet_bean):
    return iptables.block_ip_address(packet_bean)

def createSnifferAndIPRequesterThread(selected_interface):
    q = {}

    expiring_map = ExpiringDictionary()
    q["expiring_map"] = expiring_map
    q["ignored_ip_set"] = set()

    thread1= tf(Sniffer, Sniffer.start_sniffing.__name__, interface_name=selected_interface, shared_data=q)
    q["threadId"] = thread1

    thread1.start()

    return q

def stopSnifferAndIPRequesterThread(thread1):
    if thread1:
        thread1.stop()