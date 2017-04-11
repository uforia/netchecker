# netchecker.py

# Description
Netchecker lets you verify a list of IP addresses against known AS numbers/names. Works with both IPv4 and IPv6!

# Requirements
1) Python 2.7.x / 3.x (should work with both)
2) netaddr module (installable through PyPi etc.): https://pypi.python.org/pypi/netaddr
3) MaxMind's GeoLite ASN databases: http://dev.maxmind.com/geoip/legacy/geolite/

# Usage
./netchecker \<file-with-list-of-IPs-to-check\>

# Caveats
The more AS names/numbers you check, the longer it takes to build the list of netblocks to verify against!
