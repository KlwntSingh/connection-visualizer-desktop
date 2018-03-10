import platform
import json
import os
from pathlib import Path

CONFIG = json.load(open("config/config.json"))

# CONFIG["AUTHOR"] =  """Kulwant Singh\nkulwantbughipura@gmail.com\nhttps://www.github.com/kulwantDal/sniffer"""
CONFIG["AUTHOR"] = ["Kulwant Singh", "kulwantbughipura@gmail.com", "https://www.github.com/kulwantDal/connection-visualizer-desktop"]

#"IP_API" = "https://ip-geo.geekasservice.com/info/"

CONFIG["os"] = platform.system()