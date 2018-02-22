class Utilities():

    # %x is used to define in hexadecimal
    @staticmethod
    def getEthernetAddressFromPacket(pck):
        addr = "%.2x:%.2x:%.2x:%.2x:%.2x:%.2x" % (pck[0], pck[1], pck[2], pck[3], pck[4], pck[5])
        return addr
