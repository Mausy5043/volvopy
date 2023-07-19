#!/usr/bin/env python3

import json
import pprint
import configparser
import os
import pytz


# constants
DEBUG = False
HERE = os.path.realpath(__file__).split("/")
APPNAME = HERE[-2]
# to find other files
APPROOT = "/".join(HERE[0:-1])
# host_name :
NODE = os.uname()[1]

_MYHOME = os.environ["HOME"]
_DATABASE = "/tmp/volvopy-db"
_WEBSITE = "/tmp/volvopy-www"

DT_FORMAT = "%Y-%m-%d %H:%M:%S"
TIMEZONE = pytz.timezone("Europe/Amsterdam")

_pp2 = pprint.PrettyPrinter(sort_dicts=False, indent=1, depth=2)

_api_keys_file = f"{_MYHOME}/.config/volvopy/keys.ini"

_supported_api_specifications = {
    "connected.v1": f"{APPROOT}/specification/connected-vehicle-c3-specification.v1.json",
    "energy.v1": f"{APPROOT}/specification/energy-api-specification.v1.json",
    "extended.v1": f"{APPROOT}/specification/extended-vehicle-c3-specification.v1.json",
    "location.v1": f"{APPROOT}/specification/location-specification.v1.json",
}

API_SPECIFICATIONS = {
    "connected": "connected.v1",
    "energy": "energy.v1",
    "extended": "extended.v1",
    "location": "location.v1",
}

# load the specifications and store them in a constant
for _key, _spec in API_SPECIFICATIONS.items():
    _filename = _supported_api_specifications[_spec]
    with open(_filename, encoding="utf-8") as _json_file:
        _data = json.load(_json_file)
    API_SPECIFICATIONS[_key] = _data

# load the configuration file and store the carious keys in constants
_inifile = configparser.ConfigParser()
_inifile.read(_api_keys_file)
API_KEY = [_inifile.get("API", "vcc_primary"), _inifile.get("API", "vcc_secondary")]
API_TOKEN = {}
for _name in API_SPECIFICATIONS:
    try:
        API_TOKEN[_name] = _inifile.get("API", f"{_name}_token")
    except:
        API_TOKEN[_name] = None
API_VIN = _inifile.get("API", "vin")


if __name__ == "__main__":
    _pp2.pprint(API_SPECIFICATIONS)
    print()
    print(API_KEY)
    print(API_VIN)
    print(API_TOKEN)
