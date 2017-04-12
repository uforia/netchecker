# Description  
  
Netchecker lets you offline-check a list of IP addresses against known AS numbers/names. Works with both IPv4 and IPv6! This tool is useful
for checking of e.g. leaked/dumped IPs against ASNs to see if there are matches, without having to use internet sources and thereby risking
the possibility of announcing your interest in the checked IPs.

# Requirements  
  
1) Python 2.7.x / 3.x (should work with both...)
2) netaddr module (installable through PyPi etc.): https://pypi.python.org/pypi/netaddr
3) MaxMind's GeoLite ASN databases: http://dev.maxmind.com/geoip/legacy/geolite/
  
# Installation and usage  
  
1) git clone https://github.com/uforia/netchecker.git
2) pip install netaddr / apt-get install python-netaddr / emerge dev-python/netaddr / or whatever you use for package management
3) download the GeoLite ASN databases: http://dev.maxmind.com/geoip/legacy/geolite/ and unpack them in the netchecker directory

# Configuration and usage  
  
1) Create a list of IPs in plaintext, one IP per line, in a single file, e.g.: 'ips.txt'
2) Open netchecker.py in an editor and change the 'MyASN' variable's contents at the top to reflect your AS names/numbers
3) Run netchecker: ./netchecker.py ips.txt

# Caveats, miscellaneous, TODO, etc.  
  
- The more AS names/numbers you check, the longer it takes to build the list of netblocks to verify against!
- This product includes GeoLite data created by MaxMind, available from http://www.maxmind.com
- Configuration option parsing at the CLI to specify the MyASNs
- An automatic GeoIPLite downloader might be included in the future
