import uuid
import socket
import httplib, urllib
import time
import signal


def sigusr1(signum, frame):
	print("Sigusr catched")

uuid=uuid.getnode()
ip=[ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1]

print("UUID is "+str(uuid)+" for IP "+str(ip))


params = urllib.urlencode({'@number': 12524, '@type': 'issue', '@action': 'show'})
headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
conn = httplib.HTTPConnection("bugs.python.org")
conn.request("POST", "", params, headers)
response = conn.getresponse()
print response.status, response.reason
data = response.read()
print (str(data))
conn.close()


signal.signal(signal.SIGUSR1, sigusr1)
print("Waiting ...")
time.sleep(60)
print("Done")