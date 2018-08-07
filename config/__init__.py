import os
import sys

import anyconfig

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(os.path.abspath(os.path.join(BASE_DIR)))

config_dir = os.path.join(BASE_DIR, "config")
config = anyconfig.load(
    [os.path.join(config_dir, "config.yml"), os.path.join(config_dir, "secrets.yml")],
    ignore_missing=True
)
