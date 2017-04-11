#!/usr/bin/env python

### My ASNs is a Python tuple of AS numbers and/or AS names, as listed in the MaxMind GeoIP
### files. Pattern matching is based on regex matching: 'KPN' will also yield the 'KPNQwest'
### netblocks. The easiest way of preventing false matches is by adding a space or something
### similar at the end of the list item. Remember to add a loose 'comma' to a single entry
### in the tuple, to prevent it being split into individual characters.
MyASNs=('KPN B.V.',)
#MyASNs=('AS286 ','AS1136 ','AS2043 ','AS5615 ','AS8737 ','AS12871','AS21286')

### This product includes GeoLite data created by MaxMind, available from
### <a href="http://www.maxmind.com">http://www.maxmind.com</a>.

### You might have to change the following if MaxMind changes the filename scheme
### Names of GeoIP CSV files, grab the ASN ZIP archives from the MaxMind website
GeoIP='GeoIPASNum2.csv'
GeoIPv6='GeoIPASNum2v6.csv'

### The 'netaddr' module can be downloaded through PyPi (pip install ...) or installed
### through your package manager of choice
import netaddr,sys,re,csv

def IntIPtoStr(integervalue):
	return str(int(integervalue/16777216)%256),str(int(integervalue/65536)%256),str(int(integervalue/256)%256),str(int(integervalue)%256)

def BuildNetblocks(MyASNs):
	try:
		if GeoIP:
			with open(GeoIP,'rb') as f:
				IPv4MyASNs=tuple(csv.reader(f))
		if GeoIPv6:
			with open(GeoIPv6,'rb') as f:
				IPv6MyASNs=tuple(csv.reader(f))
	except IOError:
		print("Error opening/reading ASN file(s): "+IPv4MyASNs+" or "+IPv6MyASNs+"!")
		sys.exit(1)
	netblocks=[]
	print("1) Building the list of netblocks (this may take a while, depending on the number of ASNs) ...")
	for ASN in MyASNs:
		print('2) Searching for AS number/name: '+ASN)
		prog=re.compile(ASN)
		for IPv4ASN in IPv4MyASNs:
			try:
				netblockstartint,netblockendint,ASname=IPv4ASN
			except:
				print("E) An error occurred persing the IPv4ASN: "+IPv4ASN)
			if prog.search(ASname):
				netblockstart='.'.join(IntIPtoStr(int(netblockstartint)))
				netblockend='.'.join(IntIPtoStr(int(netblockendint)))
				netblock=netaddr.cidr_merge(list(netaddr.iter_iprange(netblockstart,netblockend)))
				netblocks.append(netblock)
		for IPv6ASN in IPv6MyASNs:
			try:
				ASname,netblockstartaddress,netblockendaddress,netmask=IPv6ASN
			except:
				print("E) An error occurred persing the IPv6ASN: "+IPv6ASN)
			if prog.search(ASname):
				netblock=[netaddr.IPNetwork(str(netblockstartaddress+'/'+netmask))]
				netblocks.append(netblock)
	print("3) Done building the list of netblocks!")
	return [item for sublist in netblocks for item in sublist]

def CheckIPs(netblocks,ipfile):
	try:
		with open(ipfile) as ipfp:
			print("4) Checking the list of IPs ...")
			for ip in ipfp.readlines():
				IPInNetblock(ip.strip(),netblocks)
	except IOError:
		print("E) Error opening "+ipfile+"!")
		sys.exit(1)
	print("5) All done!")

def IPInNetblock(ip,netblocks):
	#print(ip)
	#print(netblocks)
	matchingblocks=netaddr.all_matching_cidrs(ip,netblocks)
	if len(matchingblocks)>0:
		for matchingblock in matchingblocks:
			print(ip+" --> "+str(matchingblock))

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print("*) Usage: "+sys.argv[0]+" <file-with-IPs-to-check>")
	else:
		CheckIPs(BuildNetblocks(MyASNs),sys.argv[1])
