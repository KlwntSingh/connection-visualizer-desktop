import subprocess

def block_ip_address(packet_bean):
    """
    This method fires command to os to block particular ip address
    :param packet_bean:
    :return: None
    """
    rule = "iptables -A OUTPUT -d {ip} -j REJECT".format(ip=packet_bean.communicatingIP)
    subprocess.Popen(rule.split(" "), stdout=subprocess.PIPE).communicate()
    print("ip blocked")