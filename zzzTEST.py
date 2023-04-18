import cfg
import os
import utils
import configparser
import sys
import json

pretty = json.dumps(cfg.CyclesGetNames(), indent=4)

print(pretty)

