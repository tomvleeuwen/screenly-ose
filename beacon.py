import uuid
import httplib, urllib
import time, datetime
from settings import settings, DEFAULTS
#http://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib
import socket, struct, fcntl


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sockfd = sock.fileno()
SIOCGIFADDR = 0x8915

def get_ip(iface = 'eth0'):
     ifreq = struct.pack('16sH14s', iface, socket.AF_INET, '\x00'*14)
     try:
         res = fcntl.ioctl(sockfd, SIOCGIFADDR, ifreq)
     except:
         return None
     ip = struct.unpack('16sH2x4s8x', res)[2]
     return socket.inet_ntoa(ip)


 
ip=get_ip('eth0')
uuid="%x" % uuid.getnode()

sleep=30

mothership=settings['mothership']
port=settings.get_listen_port()

print("UUID is "+str(uuid)+" for IP "+str(ip))
print("Mothership location is at "+str(mothership))

while True:
	params = urllib.urlencode({'uuid': uuid, 'ip': str(ip)+":"+str(port)})
	headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
	conn = httplib.HTTPConnection(mothership)
	try:
		conn.request("POST", "/beacon", params, headers)
		response = conn.getresponse()
		print(str(datetime.datetime.now())+" Beacon to "+str(mothership)+": "+str(response.status)+" ("+str(response.reason)+")")
        	conn.close()
	except Exception as e:
		print(str(datetime.datetime.now())+" Beaconing to "+str(mothership)+" failed: "+str(e))
	time.sleep(sleep)

print("Beaconing stop")
