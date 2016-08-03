import os
import tornado.httpserver
import tornado.ioloop
import tornado.web
import requests
import datetime
import json

class MainHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	def get(self):
		self.write("EMF Badge Schedule API")
		self.content_type = 'text/plain'
		self.finish()


class SchedHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	def get(self):
		resp = requests.get('https://www.emfcamp.org/schedule.json')
		data = resp.json()
		now =  datetime.datetime.now()
		nowevents = []
		dummy = datetime.datetime.strptime('2016-08-05 13:11:00', '%Y-%m-%d %H:%M:%S')
		now = dummy
		output={}
		venues = ['Stage A', 'Stage B', 'Stage C']
		for v in venues:
			output[v] = list()

		for i in data:
			start = datetime.datetime.strptime(i['start_date'], '%Y-%m-%d %H:%M:%S')
			end = datetime.datetime.strptime(i['end_date'], '%Y-%m-%d %H:%M:%S')
			if end <= now:
				pass
			else:
				if i['venue'] in venues:
					v = i['venue']
					del i["is_fave"]
					del i["link"]
					del i["source"]
					del i["type"]
					del i["venue"]
					del i["may_record"]
					del i["description"]
					output[v].append(i)
		for v in output:
			output[v].sort(key=lambda x:x['start_date'])
			n =len(output[v]) - 2
			del output[v][-n:]
		#output['venues'] = venues = ['Stage A', 'Stage B', 'Stage C']
		self.write(json.dumps(output))
		self.set_header('Content-Type', 'application/json')
		self.finish()

class NowHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	def get(self):
		resp = requests.get('https://www.emfcamp.org/schedule.json')
		data = resp.json()
		now =  datetime.datetime.now()
		nowevents = []
		dummy = datetime.datetime.strptime('2016-08-06 13:11:00', '%Y-%m-%d %H:%M:%S')
		now = dummy
		output={}
		venues = ['Stage A', 'Stage B', 'Stage C']
		for v in venues:
			output[v] = list()
		for i in data:
			start = datetime.datetime.strptime(i['start_date'], '%Y-%m-%d %H:%M:%S')
			end = datetime.datetime.strptime(i['end_date'], '%Y-%m-%d %H:%M:%S')
			if start <= now <= end:
				nowevents.append(i)
		output['now'] = nowevents
		self.write(json.dumps(output))
		self.set_header('Content-Type', 'application/json')
		self.finish()
		
		
def main():

	application = tornado.web.Application([(r"/", MainHandler),
											(r"/schedule", SchedHandler),
											(r"/now", NowHandler)						
											])
	http_server = tornado.httpserver.HTTPServer(application)
	port = int(os.environ.get("PORT", 9002))
	http_server.listen(port)
	tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
	main()
	

