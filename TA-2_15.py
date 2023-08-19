import time
import requests
import math
import random
import RPi.GPIO as GPIO
import time

TOKEN = "BBFF-1wzxs5bk6d2wAeOHcmmdwBVVAvGDBt"  # Put your TOKEN here
DEVICE_LABEL = "zeta"  # Put your device label here 
VARIABLE_LABEL_1 = "touch"  # Put your first variable label here
VARIABLE_LABEL_2 = "ultrasonic"  # Put your second variable label here

#GPIO SETUP
GPIO.setmode(GPIO.BCM)
GPIO_TRIGGER = 15
GPIO_ECHO = 14
GPIO.setup (23,GPIO.IN)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
                
        
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance

def tosen() :
    if GPIO.input(23) == 1 : #isipin
       # print ("ada orang")
        tosen = 1
    elif GPIO.input (23) == 0 : #isipin
       # print ("tidak ada orang")
        tosen = 0

    return tosen


def build_payload(variable_1, variable_2):
    # Creates two random values for sending data
    value_1 = tosen()
    value_2 = distance()
   
    payload = {variable_1: value_1,
               variable_2: value_2,
              }

    return payload


def post_request(payload):
    # Creates the headers for the HTTP requests
    url = "http://industrial.api.ubidots.com"
    url = "{}/api/v1.6/devices/{}".format(url, DEVICE_LABEL)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

    # Makes the HTTP requests
    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = requests.post(url=url, headers=headers, json=payload)
        status = req.status_code
        attempts += 1
        time.sleep(1)

    # Processes results
    print(req.status_code, req.json())
    if status >= 400:
        print("[ERROR] Could not send data after 5 attempts, please check \
            your token credentials and internet connection")
        return False

    print("[INFO] request made properly, your device is updated")
    return True


def main():
    payload = build_payload(
        VARIABLE_LABEL_1, VARIABLE_LABEL_2)

    print("[INFO] Attemping to send data")
    post_request(payload)
    print("[INFO] finished")


if __name__ == '__main__':
    while (True):
        main()
        time.sleep(1)
