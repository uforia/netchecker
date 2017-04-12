# Description  
  
Netchecker lets you offline-check a list of IP addresses against known AS numbers/names. Works with both IPv4 and IPv6! This tool is useful
for checking of e.g. leaked/dumped IPs against ASNs to see if there are matches, without having to use internet sources and thereby risking
the possibility of announcing your interest in the checked IPs.
  
# Installation  
  
1) pip install netaddr (or apt-get install python-netaddr, or whatever else your distro uses)
2) grab a list of IPs to check and put them in plaintext in a file, one per line, e.g.: "ips.txt"
3) ./netchecker.py ips.txt

# Configuration  
  
1) Should be only one thing: open up netchecker.py in your favourite editor and change the 'MyASN' variable's contents at the top!

# Requirements  
  
1) Python 2.7.x / 3.x (should work with both)
2) netaddr module (installable through PyPi etc.): https://pypi.python.org/pypi/netaddr
3) MaxMind's GeoLite ASN databases: http://dev.maxmind.com/geoip/legacy/geolite/

# Usage  
  
./netchecker \<file-with-list-of-IPs-to-check\>
  
# Caveats and miscellaneous  
  
- The more AS names/numbers you check, the longer it takes to build the list of netblocks to verify against!
- This product includes GeoLite data created by MaxMind, available from <a href="http://www.maxmind.com">http://www.maxmind.com</a>.

