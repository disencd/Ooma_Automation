import datetime
#import Adafruit_BBIO.GPIO as GPIO
from bb_gpio import bb_gpio_process
from flask import Flask, jsonify, request
app = Flask(__name__)



'''
Flask API for checking BeagleBone is Up for Home Automation
'''
@app.route("/")
def hello():
   now = datetime.datetime.now()
   timeString = now.strftime("%Y-%m-%d %H:%M")
   Data = {
      'title' : 'BeagleBone is Up for Home Automation',
      'time': timeString
      }
   #GPIO.setup("P8_10", GPIO.OUT)
   return jsonify({'Data': Data})


'''
Flask API for turning the 3 states
1) Which Sensor - Door/Water/Motion
2) Which Interface - Pair/Water Detection/Motion Dection/Door Open/Close etc
3) Switch - ON/OFF
http://10.66.11.36:5000/sensor/door/interface/pair/switch/on
/sensor/<sensor_id>/interface/<interface_id>/switch/<switch_state>
'''

# @app.route("/sensor/<sensor_id>/interface/<interface_id>", methods=('GET'))
@app.route("/sensor/<sensor_id>/interface/<interface_id>/switch/<switch_state>")
def process_request(sensor_id, interface_id, switch_state):
    #switch_state = request.args.get('swtich', '')
    bb_obj = bb_gpio_process()
    response = "Invalid Response"
    print sensor_id, interface_id, switch_state
    if sensor_id == "Door":
        print "process_door_sensor_request"
        response = bb_obj.process_door_sensor_request(interface_id, switch_state)

    elif sensor_id == "Water":
        print "process_water_sensor_request"
        response = bb_obj.process_water_sensor_request(interface_id, switch_state)

    elif sensor_id == "Motion":
        print "process_motion_sensor_request"
        response = bb_obj.process_motion_sensor_request(interface_id, switch_state)

    else:
        response = "Unable to Process the Door Sensor"

    now = datetime.datetime.now()

    Data = {
        'response' : response,
        'time': now.strftime("%Y-%m-%d %H:%M")
    }
    return jsonify({'Data': Data})

if __name__ == "__main__":
   app.run(host='10.66.11.36', port=5000, debug=True)