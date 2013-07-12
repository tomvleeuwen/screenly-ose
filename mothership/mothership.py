#/env/python


import web
import db
import re
import base64

### Url mappings

urls = (
    '/', 'Index',
	'/beacon', 'Beacon',
    '/dbcontents', 'DumpDB',
    '/login','Login',
    '/setlabel', 'SetLabel',
    '/delete', 'DeletePod',
)


### Templates
render = web.template.render('templates', base='base')

DB_JSON_TOP="["

DB_JSON_BOTTOM=']' 


def CheckAuth(headerdata):
	if headerdata == None:
		return False
		
	pwf=open('secret','r')
	if pwf == None:
		return False
	pw=pwf.readline().strip().split(":")
	pwf.close()
	auth = re.sub('^Basic ','',headerdata)
	username,password = base64.decodestring(auth).split(':')
	return str(pw[0]) == str(username) and str(pw[1]) == str(password)
	


class Login:
	
	def checkpw(self,username,passw):
		pwf=open('secret','r')
		if pwf == None:
			return False
		pw=pwf.readline().strip().split(":")
		print(str(pw))
		if  len(pw) != 2:
			return False
		return str(pw[0]) == str(username) and str(pw[1]) == str(passw)
		
	def GET(self):
		auth = web.ctx.env.get('HTTP_AUTHORIZATION')
		authreq = False
		if auth is None:
			authreq = True
		else:
			auth = re.sub('^Basic ','',auth)
			username,password = base64.decodestring(auth).split(':')
			
			if CheckAuth(auth):
				raise web.seeother('/')
			else:
				authreq = True
		if authreq:
			web.header('WWW-Authenticate','Basic realm="Enter credentials,"')
			web.ctx.status = '401 Unauthorized'
			return



class Index:
    def GET(self):
        """ Show page """
	if CheckAuth(web.ctx.env.get('HTTP_AUTHORIZATION')):
		return render.listing()
	else:
		raise web.seeother('/login')


class DumpDB:
	def GET(self):
		""" Get DB as JSON """
		if not CheckAuth(web.ctx.env.get('HTTP_AUTHORIZATION')):
			raise web.seeother('/login')
			return
			
		allPods=db.getAll()
		allPodsJSON=DB_JSON_TOP
		for pod in allPods:
			allPodsJSON+='["'+str(pod[0])+'", "'+str(pod[1])+'", "'+str(pod[2])+'", "'+str(pod[3]) +'"],'
		
		if len(allPods) >= 1:
			allPodsJSON=allPodsJSON[:-1]
        
		allPodsJSON+=DB_JSON_BOTTOM
		return allPodsJSON

class SetLabel:
	def POST(self):
		""" receive new label """
		if not CheckAuth(web.ctx.env.get('HTTP_AUTHORIZATION')):
			raise web.seeother('/login')
			return
		user_data = web.input(u=None, l=None)
		if user_data.l==None or user_data.u == None:
			print("INCOMPLETE")
			return "FAIL"
		else:
			#print("Change "+str(user_data.u)+" to "+str(user_data.l))
			db.updateLabel(str(user_data.u),str(user_data.l))
			return "OK"
		

class DeletePod:
	def POST(self):
		""" receive new label """
		if not CheckAuth(web.ctx.env.get('HTTP_AUTHORIZATION')):
			raise web.seeother('/login')
			return
		user_data = web.input(u=None)
		if user_data.u == None:
			print("INCOMPLETE")
			return "FAIL"
		else:
			#print("Delete "+str(user_data.u))
			db.delete(str(user_data.u))
			return "OK"


class Beacon:
	def POST(self):
		""" receive beacon """
		user_data = web.input(uuid=None, ip=None)
		if user_data.uuid==None or user_data.ip == None:
			print("INCOMPLETE")
			return
		print("Received "+user_data.uuid+" at "+user_data.ip)  
		db.addEntry(user_data.uuid,user_data.ip)
#	        model.del_todo(id)
#      	  raise web.seeother('/')


app = web.application(urls, globals())

if __name__ == '__main__':
    db.initDB()
    app.run()

