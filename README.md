# netchecker.py

# Requirements
1) netaddr module (installable through PyPi etc.): https://pypi.python.org/pypi/netaddr

# Description
Netchecker lets you verify a list of IP addresses against known AS numbers/names.

# Usage
./netchecker \<file-with-list-of-IPs-to-check\>

# Caveats
The more AS names/numbers you check, the longer it takes to build the list of netblocks to verify against!
