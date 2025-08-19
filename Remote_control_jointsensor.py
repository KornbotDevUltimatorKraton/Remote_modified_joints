import requests 
import time 
import numpy as np 
from itertools import count 
import random

for r in count(0):
    #reqdata = requests.post("https://roboreactor.com/package_iot_control",json={'kornbot380@hotmail.com':{}})
    #current_feedback = reqdata.json()['Smart_Robots']['revolute'] 
    #res_feedback = requests.post('https://roboreactor.com/feedback_sensor',json={'kornbot380@hotmail.com':{'wrist':{'Analog-read':45.0},'base':{'Analog-read':140.4}}})
    #print(res_feedback.json())
    c= 1
    rc = 0 
    for i in range(0,90):
          #for r in range(0,8):
          '''
          try:
            reqdata = requests.post("https://roboreactor.com/package_iot_control",json={'kornbot380@hotmail.com':{}})
            current_feedback = reqdata.json()['Smart_Robots']['revolute'] 
            base  = current_feedback['base'] 
            print("Destination angle,current feedback",rc,base)
            d = rc -base
            i = rc+d    
            res_feedback = requests.post('https://roboreactor.com/feedback_sensor',json={'kornbot380@hotmail.com':{'wrist':{'Analog-read':i},'shoulder':{'Analog-read':i},'base':{'Analog-read':i}}})
            #for r in range(0,8):
            #      print("Forward: ",i)

          except:
                  print("No old data read")
          '''
          rc = i #+random.random()
       
          res_feedback = requests.post('https://roboreactor.com/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':{'IRB1':{'Analog-read':rc},'IRB2':{'Analog-read':rc},'IRB3':{'Analog-read':rc},'IRB4':{'Analog-read':rc},'IRB5':{'Analog-read':rc},'IRB6':{'Analog-read':rc},'CON V3':{'Analog-read':rc*4},'AMR11':{'Analog-read':rc*4}}}})
              #for r in range(0,8):
          print("Forward: ",rc)
          try:
             reqdata = requests.post("https://roboreactor.com/package_iot_control",json={'teslacoil358@gmail.com':{}})
             current_feedback = reqdata.json()['BD3']['revolute']
             print(current_feedback)
             #slider_feedback = reqdata.json()['BD3']['slider']
          except:
               print("No data input yet") 
    for i in range(90,0,-1):
          #for r in range(0,8): 
          rc = i #+random.random()
          res_feedback = requests.post('https://roboreactor.com/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':{'IRB1':{'Analog-read':rc},'IRB2':{'Analog-read':rc},'IRB3':{'Analog-read':rc},'IRB4':{'Analog-read':rc},'IRB5':{'Analog-read':rc},'IRB6':{'Analog-read':rc},'CON V3':{'Analog-read':rc*4},'AMR11':{'Analog-read':rc*2.5}}}})
          #for r in range(0,8):  
          print("Back ward: ",rc)
          try:
             reqdata = requests.post("https://roboreactor.com/package_iot_control",json={'teslacoil358@gmail.com':{}})
             current_feedback = reqdata.json()['BD3']['revolute']
             print(current_feedback)
          except:
             print("No data input yet") 
    #time.sleep(0.04)
#for i in np.arange(0.0, 270.0, 0.01):
#    print(i)   
#    res_feedback = requests.post('https://roboreactor.com/feedback_sensor',json={'kornbot380@hotmail.com':{'wrist':{'Analog-read':i},'shoulder':{'Analog-read':i},'base':{'Analog-read':i}}}) 	
#res_feedback = requests.post('https://roboreactor.com/feedback_sensor',json={'kornbot380@hotmail.com':{'wrist':{'Angle-read':
#270}}})
