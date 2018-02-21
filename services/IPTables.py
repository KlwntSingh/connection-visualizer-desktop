import subprocess

def block_ip_address(packet_bean):
    rule = "iptables -A OUTPUT -d {ip} -j REJECT".format(ip=packet_bean.communicatingIP)
    print(subprocess.Popen(rule.split(" "), stdout=subprocess.PIPE).communicate())