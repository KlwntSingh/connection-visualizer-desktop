import platform
import json
import os
from pathlib import Path

CONFIG = json.load(open("config/config.json"))

CONFIG["AUTHOR"] = """
                        Kulwant Singh
                        kulwantbughipura@gmail.com
                        https://www.github.com/kulwantDal/sniffer
                    """

CONFIG["os"] = platform.system()