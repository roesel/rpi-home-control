#import RPi.GPIO as GPIO
from flask import Flask, render_template, request, jsonify, abort
app = Flask(__name__, static_url_path='/static')

from yeelight import Bulb
from sonoff import Switch
import json

import Adafruit_DHT

# eWe link api key: b1aca638-0da2-483d-a10b-30f323d431f3

b = {
    "bedroom" : Bulb("192.168.1.66"),
    "lamp"    : Bulb("192.168.1.67"),
    "kitchen" : Bulb("192.168.1.68"),
    "couch" : Switch(host = "192.168.1.65", api_key = "7ba6977a-5cdd-4afa-9774-528fd9e28439", device_id="1000416b19"),
    "armchair" : Switch(host = "192.168.1.64", api_key = "d70cdd56-4aac-483a-aa68-1c791a6512ae", device_id="1000839445"),
}



def set_color(bid, color):
    if color=='red':
        b[bid].set_rgb(255, 0, 0)
    elif color=='green':
        b[bid].set_rgb(0, 255, 0)
    else:
        b[bid].set_rgb(255, 255, 255)     
    b[bid].set_brightness(100)

def set_ct(bid, temp):
    b[bid].set_color_temp(int(temp))
    b[bid].set_brightness(100)

def set_mode(bid, mode):
    if mode == "night":
        # Set RGB value.
        b[bid].set_rgb(255, 153, 0)
        # Set HSV value.    
        b[bid].set_hsv(36, 100, 1)
    
def set(bid, status):
    try:
        if status=="on":
            b[bid].turn_on()
        else:
            b[bid].turn_off()
        return True
    except:
        print('Unable to reach bulb.')
        return False

@app.route("/")
def main():
    ''' Main touch-compatible screen with all the controls. '''
    return render_template('light_control.html')

@app.route("/humitemp")
def get_humi_temp():
    humidity, temperature = Adafruit_DHT.read_retry(11, 4)
    return '{} °C<br/>{} %'.format(int(temperature), int(humidity))

@app.route('/yee', methods=['GET']) 
def yee():
    ''' Endpoint for changing the lightbulb state. '''
    bulb = request.values.get('bulb')
    action = request.values.get('action')
    param = request.values.get('param')
    
    # Actions for all lightbulbs
    if bulb=="all":
        if action=="off":
            for id, bu in b.items():
                set(id, 'off')
    else:
        # Go through all actions and run adequate functions
        if action == "color":
            if not set(bulb, 'on'): return "error"
            set_color(bulb, param)
        elif action == "ct":
            if not set(bulb, 'on'): return "error"
            set_ct(bulb, param)
        elif action == "mode":
            if not set(bulb, 'on'): return "error"
            set_mode(bulb, 'night')
        elif action == "on":
            if not set(bulb, 'on'): return "error"
        elif action == "off":
            if not set(bulb, 'off'): return "error"
    
    # TODO: return output (if there is any).
    return "test"

def get_status(bn, p):
    ''' Takes bulb_name and properties and decides what the current status is. '''
    # If the bulb says off, it doesn't matter which bulb it is, it's off
    if p['power'] == 'off':
        out = 'off'
    else:
        if bn == 'lamp':
            if p['ct'] == '3116':
                out = 'warm'
            elif p['ct'] == '5507':
                out = 'cool'
            else:
                out = 'on'
        elif bn == 'bedroom':  
            if p['color_mode'] == '1':
                out = 'night'
            elif p['ct'] == '5507':
                out = 'cool'
            else:
                out = 'on'
        #if bn in ['kitchen', 'couch']:
        else:
            out = p['power']  # this should always be 'on'
        
                
    return out
    
@app.route('/status/<bulb_name>')
def status(bulb_name):
    if bulb_name == 'all':
        bulbs = b
    else:
        bulbs = [bulb_name]
    
    out = {}
    for bn in bulbs:
        if bn in b:
            try:
            # TODO Handle for case of Sonoff
                p = b[bn].get_properties()
                out[bn] = get_status(bn, p)
            except:# yeelight.main.BulbException:
                print('Bulb "{}" unreachable.'.format(bn))
                out[bn] = "offline"
        else:
            print('Requested bulb not found.')
            out[bn] = "not found"
        
    j = json.dumps(out)
    return j
    
if __name__ == "__main__":
   app.run(host='0.0.0.0', debug=True)
