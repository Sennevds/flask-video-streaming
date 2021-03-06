#!/usr/bin/env python3
from importlib import import_module
import os
from flask import Flask, render_template, Response, request
import RPi.GPIO as GPIO
# import camera driver
if os.environ.get('CAMERA'):
    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
else:
    raise RuntimeError('No environment variable CAMERA defined!')

Led = import_module('led').Led
# Raspberry Pi camera module (requires picamera package)
app = Flask(__name__)
led = Led(21)
cam = Camera(led)

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def gen_snapshot(camera):
    frame = camera.get_frame(True)
    return frame


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    if(not led.leds_on()):
        led.switch_leds(True)
    return Response(gen(cam),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/snapshot')
def snapshot():
    """Video streaming route. Put this in the src attribute of an img tag."""
    # if(not cam.leds_on):
    #     led.switch_leds(True)
    return Response(gen_snapshot(cam),
                    mimetype='image/jpeg')
        
@app.route('/control_leds', methods=['POST'])
def control_leds():
    """Video streaming route. Put this in the src attribute of an img tag."""
    json = request.json
    led_state = json["state"]
    if(led_state == 'on'):
        led.switch_leds(True)
        resp = 'true'
    elif(led_state == 'off'):
        led.switch_leds(False)
        resp = 'false'
    else:
        return ('', 504)
    return Response(f'{{"led_status": {resp}}}', mimetype="application/json")
    

@app.route('/leds_on')
def led_status():
    status = led.status()
    if(status == 1):
        resp = 'true'
    else:
        resp = 'false'
    return Response(f'{{"led_status": {resp}}}', mimetype="application/json")
    
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', threaded=True, port=3000)
