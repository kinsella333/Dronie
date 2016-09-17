#!/usr/bin/env python

from dronekit import connect, VehicleMode
from pymavlink import mavutil
from Queue import Queue
from flask import Flask, render_template, jsonify, Response, request
import time
import json
import urllib
import atexit
import os
import sys
import socket
from threading import Thread
from subprocess import Popen
from flask import render_template
from flask import Flask, Response
from datetime import datetime

vehicle = None

# Allow us to reuse sockets after the are bound.
# http://stackoverflow.com/questions/25535975/release-python-flask-port-when-script-is-terminated
socket.socket._bind = socket.socket.bind
def my_socket_bind(self, *args, **kwargs):
    self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    return socket.socket._bind(self, *args, **kwargs)
socket.socket.bind = my_socket_bind

def sse_encode(obj, id=None):
    return "data: %s\n\n" % json.dumps(obj)

def state_msg():
    if vehicle.location.global_relative_frame.lat == None:
        raise Exception('no position info')
    if vehicle.armed == None:
        raise Exception('no armed info')
    return {
        "armed": vehicle.armed,
        "alt": vehicle.location.global_relative_frame.alt,
        "mode": vehicle.mode.name,
        "heading": vehicle.heading or 0,
        "lat": vehicle.location.global_relative_frame.lat,
        "lon": vehicle.location.global_relative_frame.lon
    }

project_root = os.path.dirname(__file__)
template_path = os.path.join(project_root, 'templates')
print("Project Root", project_root)
print "Template Path", template_path
app = Flask(__name__, template_folder=template_path)
#app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html', branding=False)

listeners_location = []
listeners_location

from threading import Thread
import time
def tcount():
    while True:
        time.sleep(0.25)
        try:
            msg = state_msg()
            for x in listeners_location:
                x.put(msg)
        except Exception as e:
            pass
t = Thread(target=tcount)
t.daemon = True
t.start()

@app.route("/api/sse/state")
def api_sse_location():
    def gen():
        q = Queue()
        listeners_location.append(q)
        try:
            while True:
                result = q.get()
                ev = sse_encode(result)
                yield ev.encode()
        except GeneratorExit: # Or maybe use flask signals
            listeners_location.remove(q)

    return Response(gen(), mimetype="text/event-stream")

# @app.route("/api/location", methods=['GET', 'POST', 'PUT'])
# def api_location():
#     if request.method == 'POST' or request.method == 'PUT':
#         try:
#             data = request.get_json()
#             (lat, lon) = (float(data['lat']), float(data['lon']))
#             goto(lat, lon)
#             return jsonify(ok=True)
#         except Exception as e:
#             print(e)
#             return jsonify(ok=False)
#     else:
#         return jsonify(**location_msg())


@app.route("/api/arm", methods=['POST', 'PUT'])
def api_location():
    if request.method == 'POST' or request.method == 'PUT':
        try:
            vehicle.armed = True
            vehicle.flush()
            return jsonify(ok=True)
        except Exception as e:
            print(e)
            return jsonify(ok=False)

@app.route("/api/mode", methods=['POST', 'PUT'])
def api_mode():
    if request.method == 'POST' or request.method == 'PUT':
        try:
            vehicle.mode = VehicleMode(request.json['mode'].upper())
            vehicle.flush()
            return jsonify(ok=True)
        except Exception as e:
            print(e)
            return jsonify(ok=False)

def connect_to_drone():
    global vehicle

    print 'connecting to drone...'
    while not vehicle:
        try:
            vehicle = connect(sys.argv[1], wait_ready=True, rate=10, heartbeat_timeout=0)
        except Exception as e:
            print 'waiting for connection... (%s)' % str(e)
            time.sleep(2)

    # if --sim is enabled...
    vehicle.parameters['ARMING_CHECK'] = 0
    vehicle.flush()

    print 'connected!'

# Never cache
@app.after_request
def never_cache(response):
    response.headers['Last-Modified'] = datetime.now()
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

t2 = Thread(target=connect_to_drone)
t2.daemon = True
t2.start()

def main():
    app.run(threaded=True, host='0.0.0.0', port=24403, debug=True)

if __name__ == "__main__":
    main()
