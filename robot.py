from flask import Flask,request, jsonify
import re
import requests
import time
import move
import RPIservo
app = Flask(__name__)
import json
move.setup()
direction_command = 'no'
turn_command = 'no'

@app.route('/sendCommand', methods=['POST'])
def sendCommand():
    print()
    type = request.json.get('type')
    print(type)
    recv_msg(type)
    return "ok",201


        
    


@app.route('/')
def hello():
    return 'Hello, World!'



functionMode = 0
speed_set = 100
rad = 0.5
turnWiggle = 60

scGear = RPIservo.ServoCtrl()
scGear.moveInit()

P_sc = RPIservo.ServoCtrl()
P_sc.start()

T_sc = RPIservo.ServoCtrl()
T_sc.start()

H1_sc = RPIservo.ServoCtrl()
H1_sc.start()

H2_sc = RPIservo.ServoCtrl()
H2_sc.start()

G_sc = RPIservo.ServoCtrl()
G_sc.start()
def robotCtrl(command_input, response):
    global direction_command, turn_command
    if 'forward' == command_input:
        direction_command = 'forward'
        move.move(speed_set, 'forward', 'no', rad)
    
    elif 'backward' == command_input:
        direction_command = 'backward'
        move.move(speed_set, 'backward', 'no', rad)

    elif 'DS' in command_input:
        direction_command = 'no'
        if turn_command == 'no':
            move.move(speed_set, 'no', 'no', rad)


    elif 'left' == command_input:
        turn_command = 'left'
        move.move(speed_set, 'no', 'left', rad)

    elif 'right' == command_input:
        turn_command = 'right'
        move.move(speed_set, 'no', 'right', rad)

    elif 'TS' in command_input:
        turn_command = 'no'
        if direction_command == 'no':
            move.move(speed_set, 'no', 'no', rad)
        else:
            move.move(speed_set, direction_command, 'no', rad)


    elif 'lookleft' == command_input:
        P_sc.singleServo(14, -1, 3)

    elif 'lookright' == command_input:
        P_sc.singleServo(14, 1, 3)

    elif 'LRstop' in command_input:
        P_sc.stopWiggle()


    elif 'up' == command_input:
        T_sc.singleServo(11, -1, 3)

    elif 'down' == command_input:
        T_sc.singleServo(11, 1, 3)

    elif 'UDstop' in command_input:
        T_sc.stopWiggle()


    elif 'handup' == command_input:
        # H1_sc.singleServo(12, 1, 7)
        
        H2_sc.singleServo(13, -1, 7)

    elif 'handdown' == command_input:
        # H1_sc.singleServo(12, -1, 7)

        H2_sc.singleServo(13, 1, 7)

    elif 'HAstop' in command_input:
        # H1_sc.stopWiggle()
        H2_sc.stopWiggle()

    elif 'armup' == command_input:
        H1_sc.singleServo(12, 1, 7)
        
        # H2_sc.singleServo(13, 1, 7)

    elif 'armdown' == command_input:
        H1_sc.singleServo(12, -1, 7)

        # H2_sc.singleServo(13, -1, 7)

    elif 'Armstop' in command_input:
        H1_sc.stopWiggle()
        # H2_sc.stopWiggle()

    elif 'grab' == command_input:
        G_sc.singleServo(15, 1, 3)

    elif 'loose' == command_input:
        G_sc.singleServo(15, -1, 3)

    elif 'stop' == command_input:
        G_sc.stopWiggle()

    elif 'home' == command_input:
        P_sc.moveServoInit([11])
        T_sc.moveServoInit([14])
        H1_sc.moveServoInit([12])
        H2_sc.moveServoInit([13])
        G_sc.moveServoInit([15])

response = {
            'status' : 'ok',
            'title' : '',
            'data' : None
        }
#robotCtrl("forward",  response )

#robotCtrl("DS", response )

def recv_msg(type):
    print(type)
    global speed_set, modeSelect
    move.setup()
    direction_command = 'no'
    turn_command = 'no'
    response = {
            'status' : 'ok',
            'title' : '',
            'data' : None
        }

    if isinstance(type,str):
        robotCtrl(type, response)

        #switchCtrl(data, response)

        #functionSelect(data, response)

        #configPWM(data, response)


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5400, debug=True)

