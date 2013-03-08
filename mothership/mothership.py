#/env/python


import web
import db

### Url mappings

urls = (
    '/', 'Index',
	'/beacon', 'Beacon',
    '/dbcontents', 'DumpDB'
)


### Templates
render = web.template.render('templates', base='base')

DB_JSON_TOP="["

DB_JSON_BOTTOM=']' 



class Index:
    def GET(self):
        """ Show page """
        return render.listing()


class DumpDB:
	def GET(self):
		""" Get DB as JSON """
		allPods=db.getAll()
		allPodsJSON=DB_JSON_TOP
		for pod in allPods:
			allPodsJSON+='["'+str(pod[0])+'", "'+str(pod[1])+'", "'+str(pod[2])+'"],'
		
		if len(allPods) >= 1:
			allPodsJSON=allPodsJSON[:-1]
        
		allPodsJSON+=DB_JSON_BOTTOM
		return allPodsJSON

class Beacon:
    def POST(self):
        """ receive beacon """
        user_data = web.input(uuid=None, ip=None)
        if user_data.uuid==None or user_data.ip == None:
			print("INCOMPLETE")
			return
        print("Received "+user_data.uuid+" at "+user_data.ip)  
        db.addEntry(user_data.uuid,user_data.ip)
#        model.del_todo(id)
#        raise web.seeother('/')


app = web.application(urls, globals())

if __name__ == '__main__':
    db.initDB()
    app.run()

