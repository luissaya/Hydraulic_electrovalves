import os
from dataclasses import dataclass

import tomli

PROJECT_PATH = "/".join(os.path.abspath(__file__).split("/")[:-2])
CONFIG_FILE = f"{PROJECT_PATH}/config/tmp102.toml"

with open(CONFIG_FILE, mode="rb") as f_data:
    config = tomli.load(f_data)


@dataclass
class Tmp102:
    channel: int = config["i2c"]["channel"]
    address: int = config["i2c"]["address"]
    reg_tmp: int = config["register"]["temp"]
    reg_config: int = config["register"]["config"]
