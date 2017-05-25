'''
Credits : Sayantan Mukherjee
	  Anis (https://stackoverflow.com/users/4022997/anis)

	  Simple Python logger to log an incoming TCP requests at port 8000 of local machine.
'''

from flask import Flask,g,request,session
import threading
import time,datetime,requests

app = Flask(__name__)

rfid_request_time=""
count=0
class Printer(object):

    def __init__(self, time_to_sleep):
        self.lock = threading.Lock()
        self.tts = time_to_sleep
        self.go_on = True

    def do_print(self):
    	global rfid_request_time
        global count
    	if rfid_request_time: 
    		if str(datetime.datetime.now()-rfid_request_time) >'0:00:03.000000':
    			print "Device Stopped"
    			count=0

    def loop(self):
        while self.go_on:
            time.sleep(self.tts)
            with self.lock:
                self.do_print()

    def exit(self):
        self.go_on = False


printer = Printer(1)


def lock_acquire(func):
    def __inner__(*args):
        with printer.lock:
            res = func(*args)
        return res
    return __inner__


@app.route("/RFID/data1",methods=['GET', 'POST'])
@lock_acquire
def hello_world():
    global count
    if request:
        if count<1:
            print "Device Started"
        count=count+1

    global rfid_request_time
    rfid_request_time=datetime.datetime.now()

    data=request.form["key"]
    print data
    return "Good Day"


def run_app():
    app.run(host='0.0.0.0',port=8000, debug=1, use_reloader=False)


if __name__ == "__main__":
    t = threading.Thread(target=printer.loop,
                     name="looper")
    t.start()
    run_app()
    printer.exit()
