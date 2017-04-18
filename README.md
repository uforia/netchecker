# Description  

(c) Arnim Eijkhoudt \<arnime _squiggly_ kpn-cert.nl\>, 2017, KPN-CERT, GPLv2 license
  
Netchecker lets you offline-check a list of IP addresses against known AS numbers/names. Works with both IPv4 and IPv6! This tool is useful
for checking of e.g. leaked/dumped IPs against ASNs to see if there are matches, without having to use internet sources and thereby risking
the possibility of announcing your interest in the checked IPs.

# Requirements  
  
1) Python 2.7.x / 3.x (should work with both...)
2) [required] netaddr module (installable through PyPi etc.): https://pypi.python.org/pypi/netaddr
3) [required] For Python 2.7: ipaddress module: https://pypi.python.org/pypi/py2-ipaddress
4) [optional] MaxMind's GeoLite ASN databases: http://dev.maxmind.com/geoip/legacy/geolite/
  
# Installation  
  
1) git clone https://github.com/uforia/netchecker.git
2) pip install netaddr, apt-get install python-netaddr, emerge dev-python/netaddr or whatever else you use for package management
3) download the GeoLite ASN databases by running ./netchecker.py -u

# Usage  
  
1) Create a list of IPs in plaintext, one IP per line, in a single file, e.g.: 'ips.txt'
2) Run netchecker: ./netchecker.py and check the command line options

# Caveats, miscellaneous, TODO, etc.  
  
- The more AS names/numbers you check, the longer it takes to build the list of netblocks to verify against!
- This product uses GeoLite data created by MaxMind, available from http://www.maxmind.com
- TO-DO: build a lookup table/cache after running the -u (update) command, to speed up lookups
