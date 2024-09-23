
[![License](https://img.shields.io/github/license/mausy5043/volvopy)](LICENSE)
![Static Badge](https://img.shields.io/badge/release-rolling-lightgreen)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/Mausy5043/volvopy/devel.svg)](https://results.pre-commit.ci/latest/github/Mausy5043/volvopy/devel)

# volvopy
Connect to the Volvo API using Python.

The library works with Python 3.9 (v3.8 will likely also work) for the demo cars of the API using your own VCC keys. You also need to generate DEMO tokens for each API module.

## Installation
On Linux:
```bash
python3 -m pip install --upgrade volvopy
```

Create a file in your home directory at `~/.config/volvopy/keys.ini`. This should contain the following information:
```ini
[API]
vcc_primary: <VCC API primary key>
vcc_secondary: <VCC API secondary key>
connected_token: <token to access the Connected Vehicle API>
extended_token: <token to access the Extended Vehicle API>
location_token: <token to access the Location API>
energy_token: <token to access the Energy API>
vin: <VIN number of your car>
```

## Disclaimer & License
This is demonstration software.
As of September 2024 `volvopy` is distributed under [AGPL-3.0-or-later](LICENSE).
