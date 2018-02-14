from services.IPInfoService import IPInfo
dic = { }
dic["expiring_map"]= {}
dic["ignored_ip_set"]=set()
IPInfo(shared_data=dic)
