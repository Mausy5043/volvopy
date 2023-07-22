
[![PyPI version](https://img.shields.io/pypi/v/volvopy.svg?logo=pypi&logoColor=FFE873)](https://pypi.org/project/volvopy)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/volvopy.svg?logo=python&logoColor=FFE873)](https://pypi.org/project/volvopy)
[![PyPI downloads](https://img.shields.io/pypi/dm/volvopy.svg)](https://pypistats.org/packages/volvopy)
[![Code style: Black](https://img.shields.io/badge/code%20style-Black-000000.svg)](https://github.com/psf/black)

# volvopy
Connect to the Volvo API using Python.

The library works with Python 3.9 (v3.8 will likely also work) for the demo cars of the API using your own VCC keys. You also need to generate DEMO tokens for each API module. 

# Installation
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

# Disclaimer & License
This is demonstration software.
See [LICENSE](LICENSE).
