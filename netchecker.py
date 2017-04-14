#!/usr/bin/env python

### (c) 2017 Arnim Eijkhoudt <arnime _squigglything_ kpn-cert.nl>, GPLv2 licensed except where
### otherwise indicated (e.g.: netaddr / MaxMind stuff).

### This product includes GeoLite data created by MaxMind, available from http://www.maxmind.com.
### You might have to change the following if MaxMind changes the filename URLs and/or schemes.
### URLs and names of GeoIP CSV files, used for grabbing the ZIP archives from the MaxMind website.
GeoIPURL='http://download.maxmind.com/download/geoip/database/asnum/'
GeoIPURLzip='GeoIPASNum2.zip'
GeoIPv6URLzip='GeoIPASNum2v6.zip'
GeoIP='GeoIPASNum2.csv'
GeoIPv6='GeoIPASNum2v6.csv'

### The 'netaddr' module can be downloaded through PyPi (pip install ...) or installed
### through your package manager of choice.
import netaddr,sys,re,csv,optparse,urllib2,zipfile,os

def UpdateGeoIP():
	"""
	Download the GeoLite IP databases from MaxMind and unpack them into the current working directory.
	This will overwrite any existing file(s) with the same name.
	"""
	try:
		response=urllib2.urlopen(GeoIPURL+GeoIPURLzip)
	except urllib2.URLError as e:
		print("E) An error occurred downloading "+GeoIPURL+GeoIPURLzip+": "+e.reason)
	try:
		with open(GeoIPURLzip,'wb') as f:
			f.write(response.read())
	except IOError:
		print("E) An error occurred writing "+GeoIPURLzip+ " to disk!")
	try:
		with zipfile.ZipFile(GeoIPURLzip,'r') as z:
			with open(GeoIP,'wb') as f:
				f.write(z.read(GeoIP))
				os.unlink(GeoIPURLzip)
	except:
		print("E) An error occured unzipping "+GeoIPURLzip)
	try:
		response=urllib2.urlopen(GeoIPURL+GeoIPv6URLzip)
	except urllib2.URLError as e:
		print("E) An error occurred downloading "+GeoIPURL+GeoIPv6URLzip+": "+e.reason)
	try:
		with open(GeoIPv6URLzip,'wb') as f:
			f.write(response.read())
	except IOError:
		print("E) An error occurred writing "+GeoIPv6URLzip+ " to disk!")
	try:
		with zipfile.ZipFile(GeoIPv6URLzip,'r') as z:
			with open(GeoIPv6,'wb') as f:
				f.write(z.read(GeoIPv6))
				os.unlink(GeoIPv6URLzip)
	except:
		print("E) An error occured unzipping "+GeoIPv6URLzip)

def IntIPtoStr(integervalue):
	"""
	Convert an integer-formatted IPv4 address into a tuple which can be converted into dot notation
	"""
	return str(int(integervalue/16777216)%256),str(int(integervalue/65536)%256),str(int(integervalue/256)%256),str(int(integervalue)%256)

def BuildNetblocks(ASNs,options):
	"""
	Build a list of netblocks based on the user-given list of AS numbers/names
	"""
	try:
		if GeoIP:
			with open(GeoIP,'rb') as f:
				IPv4ASNs=tuple(csv.reader(f))
		if GeoIPv6:
			with open(GeoIPv6,'rb') as f:
				IPv6ASNs=tuple(csv.reader(f))
	except IOError:
		print("E) Error opening/reading ASN file(s): "+GeoIP+" or "+GeoIPv6+" - try running with -u (update) option")
		sys.exit(1)
	netblocks={}
	if options.verbose:
		print("1) Building the list of netblocks (this may take a while, depending on the number of ASNs) ...")
	for ASN in ASNs:
		if options.verbose:
			print('2) Searching for AS number/name: '+ASN)
		prog=re.compile(ASN,re.IGNORECASE)
		if options.verbose:
			ipv4count=0
		for IPv4ASN in IPv4ASNs:
			try:
				netblockstartint,netblockendint,ASname=IPv4ASN
			except:
				print("E) An error occurred parsing the IPv4ASN: "+IPv4ASN)
			if prog.search(ASname):
				netblockstart='.'.join(IntIPtoStr(int(netblockstartint)))
				netblockend='.'.join(IntIPtoStr(int(netblockendint)))
				for item in netaddr.cidr_merge(list(netaddr.iter_iprange(netblockstart,netblockend))):
					netblocks[str(item)]=ASname
					if options.verbose:
						ipv4count+=1
						if (ipv4count%20==0):
							sys.stdout.write('.')
							sys.stdout.flush()
		if options.verbose:
			ipv6count=0
		for IPv6ASN in IPv6ASNs:
			try:
				ASname,netblockstartaddress,netblockendaddress,netmask=IPv6ASN
			except:
				print("E) An error occurred parsing the IPv6ASN: "+IPv6ASN)
			if prog.search(ASname):
				netblock=str([netaddr.IPNetwork(str(netblockstartaddress+'/'+netmask))][0])
				netblocks[str(netblock)]=ASname
				if options.verbose:
					ipv6count+=1
					if (ipv6count%20==0):
						sys.stdout.write(str('.'))
						sys.stdout.flush()
		if options.verbose:
			print("Found "+str(ipv4count+ipv6count)+" netblocks (IPv4:"+str(ipv4count)+"/IPv6:"+str(ipv6count)+")")
	if options.verbose:
		print("3) Done building the list of netblocks!")
	return netblocks

def CheckIPs(netblocks,options):
	"""
	Check if the given filename containing IP addresses has any that belong to the generated list of netblocks
	"""
	try:
		with open(options.filename) as ipfp:
			if options.verbose:
				print("4) Checking the list of IPs ...")
			else:
				print("\"IP\",\"Network\",\"ASname\"")
			for ip in ipfp.readlines():
				IPInNetblock(ip.strip(),netblocks)
	except IOError:
		print("E) Error opening "+ipfile+"!")
		sys.exit(1)
	if options.verbose:
		print("5) All done!")

def IPInNetblock(ip,netblocks):
	for netblock in netblocks:
		if netaddr.IPAddress(ip) in netaddr.IPNetwork(netblock):
			if options.verbose:
				print("!) "+ip+" --> "+netblock+" ("+netblocks[netblock]+")")
			else:
				print("\""+ip+"\",\""+netblock+"\",\""+netblocks[netblock]+"\"")

if __name__ == "__main__":
	cli=optparse.OptionParser(usage="usage: %prog -f <IPFILE> [options...] <list of AS names / numbers> ...\n\nE.g.: %prog -f ips.txt AS286 'KPN B.V.' BlepTech ...")
	cli.add_option('-f','--file',dest='filename',action='store',help='[required] File with IPs to check',metavar='IPFILE')
	cli.add_option('-q','--quiet',dest='verbose',action='store_false',default=True,help='[optional] Do not print progress, errors (quiet operation), CSV output format')
	cli.add_option('-u','--update',dest='update',action='store_true',default=False,help='[optional] Update the GeoLite databases (obviously requires an active internet connection)')
	(options,ASNs)=cli.parse_args()
	if options.update:
		if options.verbose:
			print("*) Updating GeoLite IP databases from "+GeoIPURL+'...')
		UpdateGeoIP()
		if options.verbose:
			print("*) Update done!")
	if (not options.filename or len(ASNs)<1) and not options.update:
		cli.print_help()
		sys.exit(1)
	CheckIPs(BuildNetblocks(ASNs,options),options)