import socket, sys
from struct import *

from beans.PacketBean import Packet

from services.LoggerService import logger
from services.utils import Utilities
from services import InterfaceService


class Sniffer():

    # first argument specifies communication domain i.e network interface
    communication_domain = socket.AF_PACKET

    # second argument communication semantics
    communication_semantic = socket.SOCK_RAW

    # specifies the protocol
    communication_protocol = socket.ntohs(0x0003)

    THIRD_LAYER_PROTOCOL_MAP = {
        6 : 'TCP',
        1 : 'ICMP',
        17 : 'UDP'
    }

    def __init__(self, **kargs):
        interface_name = kargs.get("interface_name")
        shared_data = kargs.get("shared_data")

        self.shared_data = shared_data.get("expiring_map")
        self.ignored_ip_set = shared_data.get("ignored_ip_set")
        self.system_interface_obj = InterfaceService.get_all_interfaces()
        self.ip_exists_map = {}
        self.ip_to_domain_map = {}

    def start_sniffing(self, event):
        """
            This method starts the sniffing process of the interface card
        """
        shared_data = self.shared_data

        bool = event

        try:
            s = socket.socket(self.communication_domain, self.communication_semantic, self.communication_protocol)
        except socket.error as msg:
            logger.error( 'Socket could not be created. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
            sys.exit()

        while True and not bool.isSet():
            packet = s.recvfrom(65565)
            packet_bean = Packet()

            packet_bean.interface = packet[1][0]

            packet_bean.systemMacAddress = self.system_interface_obj[packet_bean.interface]["system_mac_address"]
            packet_bean.systemIP = self.system_interface_obj[packet_bean.interface]["system_ip_address"]

            # packet string from tuple
            packet = packet[0]

            # parse ethernet header
            eth_length = 14

            eth_header = packet[:eth_length]

            eth = unpack('!6s6sH', eth_header)
            eth_protocol = socket.ntohs(eth[2])

            destination_mac_address = Utilities.getEthernetAddressFromPacket(packet[0:6])
            source_mac_address = Utilities.getEthernetAddressFromPacket(packet[6:12])

            if packet_bean.systemMacAddress == source_mac_address:
                packet_bean.communicatingMacAddress = destination_mac_address
            else:
                packet_bean.communicatingMacAddress = source_mac_address

            logger.debug('Destination MAC : ' + destination_mac_address + ' Source MAC : ' +
                    source_mac_address + ' Protocol : ' + str(eth_protocol))

            # Parse IP packets, IP Protocol number = 8
            if eth_protocol == 8:
                    # Parse IP header
                    # take first 20 characters for the ip header
                    ip_header = packet[eth_length:20 + eth_length]

                    # now unpack them :)
                    iph = unpack('!BBHHHBBH4s4s', ip_header)

                    version_ihl = iph[0]
                    version = version_ihl >> 4
                    ihl = version_ihl & 0xF

                    iph_length = ihl * 4

                    ttl = iph[5]
                    protocol = iph[6]
                    s_addr = socket.inet_ntoa(iph[8]);
                    d_addr = socket.inet_ntoa(iph[9]);

                    source_ip_address = str(s_addr)
                    destination_ip_address = str(d_addr)

                    if packet_bean.systemIP ==  source_ip_address:
                        packet_bean.communicatingIP = destination_ip_address
                    else:
                        packet_bean.communicatingIP = source_ip_address

                    packet_bean.protocol = Sniffer.THIRD_LAYER_PROTOCOL_MAP[protocol] if protocol in Sniffer.THIRD_LAYER_PROTOCOL_MAP else '-'

                    logger.debug ('Version : ' + str(version) + ' IP Header Length : ' + str(ihl) + ' TTL : ' + str(
                        ttl) + ' Protocol : ' + str(protocol) + ' Source Address : ' + str(
                        s_addr) + ' Destination Address : ' + str(d_addr))

                    # TCP protocol
                    if protocol == 6:
                        t = iph_length + eth_length
                        tcp_header = packet[t:t + 20]

                        # now unpack them :)
                        tcph = unpack('!HHLLBBHHH', tcp_header)

                        source_port = tcph[0]
                        dest_port = tcph[1]
                        sequence = tcph[2]
                        acknowledgement = tcph[3]
                        doff_reserved = tcph[4]
                        tcph_length = doff_reserved >> 4

                        logger.debug ('Source Port : ' + str(source_port) + ' Dest Port : ' + str(
                            dest_port) + ' Sequence Number : ' + str(
                            sequence) + ' Acknowledgement : ' + str(acknowledgement) + ' TCP header length : ' + str(
                            tcph_length))

                        h_size = eth_length + iph_length + tcph_length * 4
                        data_size = len(packet) - h_size

                        # get data from the packet
                        data = packet[h_size:]


                    # ICMP Packets
                    elif protocol == 1:
                        u = iph_length + eth_length
                        icmph_length = 4
                        icmp_header = packet[u:u + 4]

                        # now unpack them :)
                        icmph = unpack('!BBH', icmp_header)

                        icmp_type = icmph[0]
                        code = icmph[1]
                        checksum = icmph[2]

                        logger.debug ('Type : ' + str(icmp_type) + ' Code : ' + str(code) + ' Checksum : ' + str(checksum))

                        h_size = eth_length + iph_length + icmph_length
                        data_size = len(packet) - h_size

                        # get data from the packet
                        data = packet[h_size:]

                    # UDP packets
                    elif protocol == 17:
                        u = iph_length + eth_length
                        udph_length = 8
                        udp_header = packet[u:u + 8]

                        # now unpack them :)
                        udph = unpack('!HHHH', udp_header)

                        source_port = udph[0]
                        dest_port = udph[1]
                        length = udph[2]
                        checksum = udph[3]

                        logger.debug ('Source Port : ' + str(source_port) + ' Dest Port : ' + str(dest_port) + ' Length : ' + str(
                            length) + ' Checksum : ' + str(checksum))

                        h_size = eth_length + iph_length + udph_length
                        data_size = len(packet) - h_size

                        # get data from the packet
                        data = packet[h_size:]

                        # 1 byte equals length of 1 when stringified string
                        # dns response packet analysis
                        if source_port == 53:
                            question = unpack('!H', data[4:6])[0]
                            answers = unpack('!H', data[6:8])[0]
                            authority_rr, additional_rr = unpack('!HH', data[8:12])

                            if (authority_rr + additional_rr) == 0:
                                # udp layer has length and other 4 fields and than in dns layer 6 fields which are each of 2 bytes and are useless
                                data_length = length - 20
                                # print(len(data[8:]))
                                # print(unpack("!{}s".format(length-20), data[12:]))

                                answers_bytes_length = answers * 16
                                question_bytes_length = data_length - answers_bytes_length

                                # 6 fields are extra fields before dns layer queries which makes starting point at 12
                                # 2 fields in question area which makes it 4 bytes
                                question_ares = data[12: 12 + question_bytes_length]
                                question_data = question_ares[1:-5]

                                domain_name = unpack("!{count}s".format(count=len(question_data)), question_data)

                                question_type = unpack("!H", question_ares[-4:-2])
                                if question_type[0] == 1:

                                    # 6 extra fields in dns layer + questionbytes length
                                    answers_area = data[12 + question_bytes_length: ]

                                    # each of anwer are is of 16 bytes
                                    for i in range(answers):
                                        dns_rep = answers_area[12 + i * 16: (i + 1) * 16]
                                        found_ip_addr = socket.inet_ntoa(unpack("!4s", dns_rep)[0])
                                        if found_ip_addr not in self.ip_to_domain_map:
                                            self.ip_to_domain_map[found_ip_addr] = domain_name

                    # some other IP packet like IGMP
                    else:
                        logger.debug ('Protocol other than TCP/UDP/ICMP')

                    # if packet_bean.communicatingIP in self.ip_to_domain_map:
                    #     packet_bean.domain_name = self.ip_to_domain_map[packet_bean.communicatingIP]
                    # else:
                    #     packet_bean.domain_name = socket.gethostbyaddr(packet_bean.communicatingIP)#input addr, output name

                    self.shared_data.put(packet_bean.communicatingIP, packet_bean)


    def stop_sniffing(self):
        pass