#!/usr/bin/env python3

# volvopy
# Copyright (C) 2024  Maurice (mausy5043) Hendrix
# AGPL-3.0-or-later  - see LICENSE

import argparse
import json
import logging
import logging.handlers
import os
import random
import sys
import uuid
from typing import Any

import requests

import volvopy.settings.constants as vc

logging.basicConfig(
    level=logging.INFO,
    format="%(module)s.%(funcName)s [%(levelname)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.handlers.SysLogHandler(
            address="/dev/log", facility=logging.handlers.SysLogHandler.LOG_DAEMON
        )
    ],
)
LOGGER: logging.Logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description="Execute the volvopy app.")
parser.add_argument("--debug", action="store_true", help="start in debugging mode")
OPTION = parser.parse_args()

DEBUG = False
HERE = os.path.realpath(__file__).split("/")
MYID = HERE[-1]

# Token for testing: https://developer.volvocars.com/apis/docs/test-access-tokens/#demo-car

__UUID__ = uuid.UUID("{FACADE00-289C-11EE-8000-6AB05A49B93D}")  # Application UUID


class VolvopyException(Exception):
    """Base class for all volvopy exceptions"""

    def __init__(self, message, api) -> None:
        self.message = message
        self.api = api

    def __str__(self):
        msg = f"(volvopy.{self.api}) {self.message}"
        return msg


class VolvoAPI:
    """Base Class to connect and interact with the Volvo APIs.

    ref.: https://developer.volvocars.com/apis/
    """

    def __init__(self, debug=False) -> None:
        self.debug = debug  # flag for debugging
        self.api_key = vc.API_KEY[round(random.random())]  # nosec
        # select one of the keys for use
        # For testing: a DEMO token is needed, which will be valid for 1 hr and can be
        # generated here: https://developer.volvocars.com/apis/docs/test-access-tokens/#demo-car
        self.vin = vc.API_VIN  # The VIN number of the car
        self.uuid = __UUID__  # application UUID
        LOGGER.debug(f"          UUID: {str(self.uuid)}")
        # construct an application-wide instance-specific UUID
        self.vuid = uuid.uuid3(self.uuid, "volvopy")
        LOGGER.debug(f"          VUID: {str(self.vuid)}")

        self.api: str = ""
        self.api_token = None
        self.api_spec = {}
        self.guid = "deadd00d-dead-d00d-dead-badbadbadbad"  # placeholder for a API-specific UUID

    def get_all(self) -> list[Any]:
        """GET all paths"""
        result = []
        vin = self.vin  # noqa  # for use in the eval line
        resource = "none"  # noqa  # for use in the eval line
        id = "none"  # noqa  # for use in the eval line
        base_url = f"{self.api_spec['servers'][0]['url']}"
        for path in self.api_spec["paths"]:
            if any(sub in path for sub in ("resources", "requests")):
                LOGGER.warning("*********GOTCHA******", path)
            try:
                if self.api_spec["paths"][path]["get"]:
                    # get the 'Accept' entry from the specification
                    accept = list(
                        self.api_spec["paths"][path]["get"]["responses"]["200"]["content"]
                    )[
                        0
                    ]  # construct the headers
                    headers = {
                        "Content-type": "application/json",
                        "Accept": f"{accept}",
                        "authorization": f"Bearer {self.api_token}",
                        "vcc-api-key": self.api_key,
                        "vcc-api-operationId": self.guid,
                    }
                    # construct the URL
                    try:
                        url = eval(f"f'{base_url}{path}'")  # nosec

                        LOGGER.debug(f"---\nGETting {url} ")
                        response = requests.get(url, headers=headers, timeout=10)
                        content = json.loads(response.content)

                        LOGGER.debug("Result data: ")
                        for _key in content:
                            if _key in [
                                "data",
                                "resources",
                                "vehicles",
                                "requests",
                            ] and isinstance(content[_key], dict):
                                for _data_key in content[_key]:
                                    LOGGER.debug(
                                        f"d      {_data_key} :: {content[_key][_data_key]}"
                                    )
                            if _key in [
                                "data",
                                "resources",
                                "vehicles",
                                "requests",
                            ] and isinstance(content[_key], list):
                                for _d in content[_key]:
                                    # for _data_key in _d:
                                    LOGGER.debug(f"d      {_key} :: {_d}")
                            else:
                                LOGGER.debug(f"k   {_key} :: {content[_key]}")
                        result.append(content)
                    except json.decoder.JSONDecodeError as her:
                        LOGGER.warning("Invalid response from server.")
                        pass
                    except Exception as her:
                        # Non-anticipated exceptions must be raised to draw attention to them.
                        reraise = VolvopyException(f"{her}", self.api)
                        LOGGER.error("text:", response.text)
                        raise  # reraise from her
            except KeyError:
                LOGGER.info("")
                LOGGER.info(f"** Skipping {path} ...")

            # try:
            #     if self.api_spec["paths"][path]["post"]:
            #         pass
            # except KeyError:
            #     LOGGER.debug(f"Skipping POST {path} ...")

            # TODO: The specification "knows" what responses are to be expected
            #       for each path. Use that here to our advantage.
            # if _response.status_code == 400:
            #     LOGGER.debug(
            #         "Bad Request - Request contains an unaccepted input"
            #     )
            # if _response.status_code == 401:
            #     LOGGER.debug("Unauthorized or TOKEN expired")
            # if _response.status_code == 403:
            #     LOGGER.debug("Resource forbidden")
            # if _response.status_code == 404:
            #     LOGGER.debug("Not found")
            # if _response.status_code == 500:
            #     LOGGER.debug("Internal Server Error")
        return result


class Connected_Vehicle(VolvoAPI):
    """Class to connect and interact with the Volvo Connected Vehicle API.

    ref.: https://developer.volvocars.com/apis/connected-vehicle/v1/specification/
    """

    def __init__(self, debug=False) -> None:
        super().__init__(debug=debug)

        self.api = "connected"
        self.api_token = vc.API_TOKEN[self.api]
        self.api_spec = vc.API_SPECIFICATIONS[self.api]
        self.guid = str(uuid.uuid3(self.vuid, f"volvopy.{self.api}"))
        LOGGER.debug(f"Connected GUID: {self.guid}")


class Energy(VolvoAPI):
    """Class to connect and interact with the Volvo Energy API.

    ref.: https://developer.volvocars.com/apis/energy/v1/specification/
    """

    def __init__(self, debug=False) -> None:
        super().__init__(debug=debug)

        self.api = "energy"  # Name of the API.
        self.api_token = vc.API_TOKEN[self.api]
        self.api_spec = vc.API_SPECIFICATIONS[self.api]
        self.guid = str(uuid.uuid3(self.vuid, f"volvopy.{self.api}"))
        LOGGER.debug(f"   Energy GUID: {self.guid}")


class Extended_Vehicle(VolvoAPI):
    """Class to connect and interact with the Volvo Extended Vehicle API.

    ref.:https://developer.volvocars.com/apis/extended-vehicle/v1/specification/
    """

    def __init__(self, debug=False) -> None:
        super().__init__(debug=debug)

        self.api = "extended"
        self.api_token = vc.API_TOKEN[self.api]
        self.api_spec = vc.API_SPECIFICATIONS[self.api]
        self.guid = str(uuid.uuid3(self.vuid, f"volvopy.{self.api}"))
        LOGGER.debug(f" Extended GUID: {self.guid}")


class Location(VolvoAPI):
    """Class to connect and interact with the Volvo Location API.

    ref.: https://developer.volvocars.com/apis/location/v1/specification/
    """

    def __init__(self, debug=False) -> None:
        super().__init__(debug=debug)

        self.api = "location"
        self.api_token = vc.API_TOKEN[self.api]
        self.api_spec = vc.API_SPECIFICATIONS[self.api]
        self.guid = str(uuid.uuid3(self.vuid, f"volvopy.{self.api}"))
        LOGGER.debug(f" Location GUID: {self.guid}")


def main() -> None:
    a = Location(debug=DEBUG)
    car_loc = a.get_all()

    a = Extended_Vehicle(debug=DEBUG)
    car_xtnd = a.get_all()

    a = Energy(debug=DEBUG)
    car_nrg = a.get_all()

    a = Connected_Vehicle(debug=DEBUG)
    car_cnct = a.get_all()

    LOGGER.debug("\n----location---")
    for path_result in car_loc:
        LOGGER.debug(path_result)
    LOGGER.debug("\n----energy----")
    for path_result in car_nrg:
        LOGGER.debug(path_result)
    LOGGER.debug("\n----connected----")
    for path_result in car_cnct:
        LOGGER.debug(path_result)
    LOGGER.debug("\n----extended----")
    for path_result in car_xtnd:
        LOGGER.debug(path_result)


if __name__ == "__main__":
    if OPTION.debug:
        DEBUG = True
        print(OPTION)
        if len(LOGGER.handlers) == 0:
            LOGGER.addHandler(logging.StreamHandler(sys.stdout))
        LOGGER.level = logging.DEBUG
        LOGGER.debug("Debugging on.")
        LOGGER.debug("Debug-mode started.")
        print("Use <Ctrl>+C to stop.")
    main()
