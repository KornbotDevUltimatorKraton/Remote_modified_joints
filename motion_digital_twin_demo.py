#Request the motion control for the digital twin controller 
import os 
import json 
import requests 
from itertools import count
user_name = os.listdir("/home/")[0] #Get the username of the current user 
'''
read_frame = open('/home/'+user_name+'/Remote_modified_joints/motion_frame.json','r') #Get the list of the motion frame reader 
loader_frame = read_frame.read()
animation_frame  = json.loads(loader_frame) #Get the json payload 
print("Reading the animation animation frame data",animation_frame)
frame_list = animation_frame['motion_frame'] #Get the total frame list input to running in the loop 
'''
def reset_pos_function(user_name):
        read_frame = open('/home/'+user_name+'/Remote_modified_joints/motion_frame.json','r') #Get the list of the motion frame reader 
        loader_frame = read_frame.read()
        animation_frame  = json.loads(loader_frame) #Get the json payload 
        print("Reading the animation animation frame data",animation_frame)
        frame_list = animation_frame['motion_frame']

#Post initial frame for starting point of motion to each distributed server 
for i in count(0):
  read_frame = open('/home/'+user_name+'/Remote_modified_joints/motion_frame.json','r') #Get the list of the motion frame reader 
  loader_frame = read_frame.read()
  animation_frame  = json.loads(loader_frame) #Get the json payload 
  print("Reading the animation animation frame data",animation_frame)
  frame_list = animation_frame['motion_frame'] #Get the total frame list input to running in the loop 
  for fl in range(0,len(frame_list)-1):
      print("Running the animation frame",frame_list[fl],list(frame_list[fl])[0]) #Detecting the key name of the actuation of the robot's motion

      if fl == 0:
          print("Initial frame reset ")  #Getting the initial position for the motion   
          req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})
          #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
          #AMR motion and pallett motion move  
          #Adding terminal goal distance in the range 
          terminal_xdis = 10 
          
          for amrdis_x in range(frame_list[fl]['AMRX']['Analog-read'],terminal_xdis,-1): #Getting the default paramter reading the JSON payload input 
                 print("Forward control AMR: ",amrdis_x) #Getting the JSON payload distance  
                 print("Default Pallet distance parameters: ",frame_list[fl]['PalletX1']['Analog-read'])
                 #Update the positioning data frame by frame 
                 frame_list[fl]['AMRX']['Analog-read'] = amrdis_x #Update the AMR distance position by frame
                 frame_list[fl]['PalletX1']['Analog-read'] = amrdis_x+30 #Compensate the distance of pallett X1 
                 req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})
          #Rotate the AMR and Pallet at the same time 
          for amrrevo_angle in range(frame_list[fl]['AMRREVO']['Analog-read'],91,-1):
                  print("Rotate AMR angle: ",amrrevo_angle)
                  frame_list[fl]['AMRREVO']['Analog-read'] = amrrevo_angle+0.5   
                  frame_list[fl]['PalletREVO1']['Analog-read'] = amrrevo_angle+0.5
                  req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})
          #Placing the pallet in place after rotation 
          for amrlift_range in range(frame_list[fl]['AMRZ']['Analog-read'],77): 
                  print("Range of the AMR lift: ",amrlift_range)  
                  frame_list[fl]['AMRZ']['Analog-read'] = amrlift_range
                  frame_list[fl]['PalletZ1']['Analog-read'] =  amrlift_range
                  req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})
          #Backward positioning control 
          for amrdis_y in range(frame_list[fl]['AMRY']['Analog-read'],0,-1):
                  print("Bacward control AMR: ",amrdis_y)
                  frame_list[fl]['AMRY']['Analog-read'] = amrdis_y        
                  req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}}) 
          #Rotate the backward position of AMR 
          for amrrevo2_angle in range(int(frame_list[fl]['AMRREVO']['Analog-read']),0,-1):
                  print("Rotate the AMR back ward control",amrrevo2_angle) 
                  frame_list[fl]['AMRREVO']['Analog-read'] = amrrevo2_angle  
                  req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}}) 
          #Forward to standby mode control 
          for amrdis_x in range(frame_list[fl]['AMRX']['Analog-read'],270):
                  print("Forward moving to standby position",amrdis_x) 
                  frame_list[fl]['AMRX']['Analog-read'] = amrdis_x #Getting  the AMr to the new position           
                  req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}}) 

          #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
               #This conveyer will working with the robotic arm in loop to the amount of the poons on the pallett
          #Conveyor 1 poons motion 
          #Conveyor 2 poons motion  
          #Conveyor 3 poons motion 
          #Robotic arm will move poons to the releasing conyer in loop proportional to amount of the poons on the palett
          #Count the amount of the poons to store the value in the array to place into the pallett to send the pallettto the packing machine 
          #If loop count the poons to the end of the conveyer then release the poons to nex position of the conyer 
          #Slide the packing poons pallettto the terminal of the machine and control packaging to hiding the position of the poons
         
          
          for poons_num  in range(0,24):
                  print("Control loop poons to conveyers: ",poons_num)  
                  #POONSZ1 ... POONSZ4
                  #Count len of the collected poon  

                  store_complete = {} #get the complete task store here  
            
                  poon_payload  = ["POONSZ1","POONSZ2","POONSZ3","POONSZ4"] #Getting all the poon 
                  package_poons = ["POONSZ5","POONSZ6","POONSZ7","POONSZ8"] #Getting all the package poon to put into the packaging machine 
                
                  #Do the loop of all set control function here 
                  #In range of poon6 
                  if poons_num <= 6:   
                             print("Activate the poons controller 1")
                             for cr in range(0,8):
                                     print("Range of the motion: ",cr*6)
                                     #Update the poon payload data  
                                     frame_list[fl][poon_payload[0]]['Analog-read'] = 42-cr*6-1   #reduce the payload data of the current poons
                                      
                                     req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}}) 
                                     #Reset the loop state function  
                                     frame_list[fl]['POONZ1']['Analog-read'] = 0 #Reset 
                                     frame_list[fl]['POONCONX1']['Analog-read'] = 0 #reset 
                                     frame_list[fl]['POONZ1']['Analog-read'] = 100
                                     frame_list[fl]['POONZ2']['Analog-read'] = 100 #Reset   
                                     frame_list[fl]['POONCONREVO1']['Analog-read'] = 0 
                                     frame_list[fl]['POONCONY3']['Analog-read'] = 0 #Reset the postiion of the conveyer sider 2 
                                     frame_list[fl]['POONCONREVO2']['Analog-read'] = 0 
                                     frame_list[fl]['POONZ4']['Analog-read'] =100
                                     frame_list[fl]['POONZ4']['Analog-read'] = 100
                                     frame_list[fl]['POONZ5']['Analog-read'] = 0
                                     frame_list[fl]['POONCONX5']['Analog-read'] = 330
                                     frame_list[fl]['POONZ6']['Analog-read'] = 0
                                     frame_list[fl]['PalletZ3']['Analog-read'] = 70
                                     frame_list[fl]['PalletX3']['Analog-read'] = 0
                                     frame_list[fl]['PalletZ4']['Analog-read'] = 100 
                                     frame_list[fl]['PalletX4']['Analog-read'] = 400 
                                     for convy in range(frame_list[fl]['POONCONX1']['Analog-read'],200):
                                                        
                                                        print("Processing the conveyer: ",convy)
                                                        frame_list[fl]['POONCONX1']['Analog-read'] = convy
                                                        req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})   
                                     frame_list[fl]['POONZ1']['Analog-read'] = 0
                                     #Revolute conveyer 1 
                                     frame_list[fl]['POONZ2']['Analog-read'] = 0 #Reset      
                                     #POONCONREVO1 Revolute default starter point 
                                     for revopoon in range(frame_list[fl]['POONCONREVO1']['Analog-read'],90):
                                                print("Revolute conveyer ",revopoon)
                                                frame_list[fl]['POONCONREVO1']['Analog-read'] = revopoon
                                                req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})
                                     #Hiding the revo poonz2 
                                     frame_list[fl]['POONZ2']['Analog-read'] = 100 #Hiding 
                                     #Loop control the conveyer 2 Slider X axis            
                                     frame_list[fl]['POONZ3']['Analog-read'] = 0 
                                     for convy2 in range(int(frame_list[fl]['POONCONY3']['Analog-read']),200):
                                               print("Conveyer 2 slider: ",convy2)
                                               frame_list[fl]['POONCONY3']['Analog-read'] = convy2
                                               req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})
                                     frame_list[fl]['POONZ3']['Analog-read'] = 100 #Hiding
                                     #Revolute conveyer 2 
                                     frame_list[fl]['POONZ4']['Analog-read'] = 0
                                     for revopoon2 in range(frame_list[fl]['POONCONREVO2']['Analog-read'],90):
                                                 print("Revolute conveyer 2: ",revopoon2) 
                                                 frame_list[fl]['POONCONREVO2']['Analog-read'] = revopoon2
                                                 req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})
                                     frame_list[fl]['POONZ4']['Analog-read'] = 100
                                     frame_list[fl]['POONZ5']['Analog-read'] = 100 
                                     for convy3 in range(frame_list[fl]['POONCONX5']['Analog-read'],0,-1):
                                                 print("Conveyer slider 3 ",convy3) 
                                                 frame_list[fl]['POONCONX5']['Analog-read'] = convy3
                                                 req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})
                                     #frame_list[fl]['POONZ5']['Analog-read'] = 0
                                     #frame_list[fl]['POONZ6']['Analog-read'] = 260 
                                     #Robotic arm pick and place poons 
                                     #Reading the position payload function 
                                     readarmpayload = open("/home/"+user_name+"/Remote_modified_joints/Robot_arm_parameters.json",'r')
                                     payloadarm = readarmpayload.read() #Reading the arm payload to manipulate the robot arm to the working area 
                                     armpayload = json.loads(payloadarm)
                                     standby_arm = armpayload['standby']
                                     default_arm = armpayload['default'] 
                                     poon1_arm = armpayload['poon1'] 
                                     #Forward arm position for poon1 positioning 
                                     if int(frame_list[fl]['IRB2']['Analog-read']) > default_arm['IRB2']['Analog-read']:
                                                print("Robotic arm standby mode activated")
                                                for st_angle in range(int(frame_list[fl]['IRB2']['Analog-read']),int(default_arm['IRB2']['Analog-read']),-1):
                                                                  frame_list[fl]['IRB2']['Analog-read'] = st_angle
                                                                  frame_list[fl]['IRB3']['Analog-read'] = st_angle 
                                                                  req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})
                                                frame_list[fl]['POONZ5']['Analog-read'] = 0
                                                frame_list[fl]['POONZ6']['Analog-read'] = 260                   
                                     if int(frame_list[fl]['IRB2']['Analog-read']) < default_arm['IRB2']['Analog-read']:
                                                print("Robotic arm standby mode activated")
                                                for st_angle in range(int(frame_list[fl]['IRB2']['Analog-read']),int(default_arm['IRB2']['Analog-read'])):
                                                                  frame_list[fl]['IRB2']['Analog-read'] = st_angle
                                                                  frame_list[fl]['IRB3']['Analog-read'] = st_angle 
                                                                  req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})
                                                frame_list[fl]['POONZ5']['Analog-read'] = 0    
                                                frame_list[fl]['POONZ6']['Analog-read'] = 260     
                                                     

                                     
                                     for se_angle in range(int(frame_list[fl]['IRB2']['Analog-read']),90,-1):
                                                        print("Control the Shoulder and Elbow joint angle: ",se_angle) 
                                                        frame_list[fl]['IRB2']['Analog-read'] = se_angle 
                                                        frame_list[fl]['IRB3']['Analog-read'] = se_angle 
                                                        req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})
                                     for base_angle in range(int(frame_list[fl]['IRB1']['Analog-read']),int(poon1_arm['IRB1']['Analog-read'])):
                                                        frame_list[fl]['IRB1']['Analog-read'] = base_angle 
                                                        req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})
                                                 
                                     calibrating_joint = ['IRB2','IRB3','IRB4','IRB5','IRB6'] 
                                     for ce in calibrating_joint:
                                           print("Calibrating joints data")
                                           joint_name = ce
                                           pos_joint = poon1_arm[ce] #getting the positiong joint angle for calibation  
                                              
                                     
                                           if frame_list[fl][joint_name]['Analog-read'] > pos_joint['Analog-read']:
                                                       print("Default joint angle more than target joint angle ",joint_name)
                                                       for angle_control in range(int(frame_list[fl][joint_name]['Analog-read']),int(pos_joint['Analog-read']),-1):
                                                                print("Now control max min: ",joint_name,angle_control)   
                                                                frame_list[fl][joint_name]['Analog-read'] = angle_control
                                                                req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})

                                           if frame_list[fl][joint_name]['Analog-read'] < pos_joint['Analog-read']:
                                                       print("Default joint angle lesser than target joint angle ",joint_name) 
                                                       for angle_control in range(int(frame_list[fl][joint_name]['Analog-read']),int(pos_joint['Analog-read'])):
                                                                print("Now control min max: ",joint_name,angle_control)
                                                                frame_list[fl][joint_name]['Analog-read'] = angle_control
                                                                req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})
                                                               
                                           if frame_list[fl][joint_name]['Analog-read'] == pos_joint['Analog-read']:
                                                       print("Default joint angle is equal to the target joint angle ",joint_name)
                                                       print("Adding the default joint angle data ",pos_joint['Analog-read']) 
                                                       frame_list[fl][joint_name]['Analog-read'] = pos_joint['Analog-read'] 
                                                       req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})
                                     frame_list[fl]['POONZ6']['Analog-read'] = 0 
                                     #Running the last pallett to send to the packaging machine 

                                     frame_list[fl][package_poons[0]]['Analog-read'] = frame_list[fl][poon_payload[0]]['Analog-read']-7 #frame_list[fl][poon_payload[0]]['Analog-read']                         
                                     #Backward arm to the default positioning 

                                     for base_angle in range(int(frame_list[fl]['IRB1']['Analog-read']),int(standby_arm['IRB1']['Analog-read']),-1):
                                                        frame_list[fl]['IRB1']['Analog-read'] = base_angle 
                                                        req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})  

                                     for se_angle in range(int(frame_list[fl]['IRB2']['Analog-read']),int(standby_arm['IRB2']['Analog-read'])):
                                                        print("Control the Shoulder and Elbow joint angle: ",se_angle) 
                                                        frame_list[fl]['IRB2']['Analog-read'] = se_angle 
                                                        frame_list[fl]['IRB3']['Analog-read'] = se_angle 
                                                        req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})   

                                     frame_list[fl]['IRB3']['Analog-read'] = standby_arm['IRB3']['Analog-read']                                
                                     #End effector calibration 
                                     endeffect_cab = ['IRB5','IRB6']  
                                     for ce in calibrating_joint:
                                           print("Calibrating joints data")
                                           joint_name = ce
                                           pos_joint = poon1_arm[ce] #getting the positiong joint angle for calibation  
                                              
                                     
                                           if frame_list[fl][joint_name]['Analog-read'] > standby_arm[joint_name]['Analog-read']:
                                                       print("Default joint angle more than target joint angle ",joint_name)
                                                       for angle_control in range(int(frame_list[fl][joint_name]['Analog-read']),int(standby_arm[joint_name]['Analog-read']),-1):
                                                                print("Now control max min: ",joint_name,angle_control)   
                                                                frame_list[fl][joint_name]['Analog-read'] = angle_control
                                                                req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})

                                           if frame_list[fl][joint_name]['Analog-read'] < standby_arm[joint_name]['Analog-read']:
                                                       print("Default joint angle lesser than target joint angle ",joint_name) 
                                                       for angle_control in range(int(frame_list[fl][joint_name]['Analog-read']),int(standby_arm[joint_name]['Analog-read'])):
                                                                print("Now control min max: ",joint_name,angle_control)
                                                                frame_list[fl][joint_name]['Analog-read'] = angle_control
                                                                req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})
                                                               
                                           if frame_list[fl][joint_name]['Analog-read'] == standby_arm[joint_name]['Analog-read']:
                                                       print("Default joint angle is equal to the target joint angle ",joint_name)
                                                       print("Adding the default joint angle data ",standby_arm[joint_name]['Analog-read']) 
                                                       frame_list[fl][joint_name]['Analog-read'] = standby_arm[joint_name]['Analog-read'] 
                                                       req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})  
                             store_complete['poon1'] = "complete"  
                             
                                
                  
                  if poons_num <=12: 
                             print("Activate the poons controller 2")
                             for ce in range(0,8):
                                     print("Range of the motion: ",ce*6)
                                     #Update the poon payload data  
                                     frame_list[fl][poon_payload[1]]['Analog-read'] = 42-ce*6-1      #reduce the payload data of the current poons 
                                     req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}}) 
                                     #Reset the loop state function  
                                     frame_list[fl]['POONZ1']['Analog-read'] = 0 #Reset 
                                     frame_list[fl]['POONCONX1']['Analog-read'] = 0 #reset 
                                     frame_list[fl]['POONZ1']['Analog-read'] = 100
                                     frame_list[fl]['POONZ2']['Analog-read'] = 100 #Reset   
                                     frame_list[fl]['POONCONREVO1']['Analog-read'] = 0 
                                     frame_list[fl]['POONCONY3']['Analog-read'] = 0 #Reset the postiion of the conveyer sider 2 
                                     frame_list[fl]['POONCONREVO2']['Analog-read'] = 0 
                                     frame_list[fl]['POONZ4']['Analog-read'] =100
                                     frame_list[fl]['POONZ4']['Analog-read'] = 100
                                     frame_list[fl]['POONZ5']['Analog-read'] = 0
                                     frame_list[fl]['POONCONX5']['Analog-read'] = 330
                                     frame_list[fl]['POONZ6']['Analog-read'] = 0
                                     frame_list[fl]['PalletZ3']['Analog-read'] = 70
                                     frame_list[fl]['PalletX3']['Analog-read'] = 0
                                     frame_list[fl]['PalletZ4']['Analog-read'] = 100 
                                     frame_list[fl]['PalletX4']['Analog-read'] = 400 
                                     for convy in range(frame_list[fl]['POONCONX1']['Analog-read'],200):
                                                        
                                                        print("Processing the conveyer: ",convy)
                                                        frame_list[fl]['POONCONX1']['Analog-read'] = convy
                                                        req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})   
                                     frame_list[fl]['POONZ1']['Analog-read'] = 0
                                     #Revolute conveyer 1 
                                     frame_list[fl]['POONZ2']['Analog-read'] = 0 #Reset      
                                     #POONCONREVO1 Revolute default starter point 
                                     for revopoon in range(frame_list[fl]['POONCONREVO1']['Analog-read'],90):
                                                print("Revolute conveyer ",revopoon)
                                                frame_list[fl]['POONCONREVO1']['Analog-read'] = revopoon
                                                req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})
                                     #Hiding the revo poonz2 
                                     frame_list[fl]['POONZ2']['Analog-read'] = 100 #Hiding 
                                     #Loop control the conveyer 2 Slider X axis            
                                     frame_list[fl]['POONZ3']['Analog-read'] = 0 
                                     for convy2 in range(int(frame_list[fl]['POONCONY3']['Analog-read']),200):
                                               print("Conveyer 2 slider: ",convy2)
                                               frame_list[fl]['POONCONY3']['Analog-read'] = convy2
                                               req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})
                                     frame_list[fl]['POONZ3']['Analog-read'] = 100 #Hiding
                                     #Revolute conveyer 2 
                                     frame_list[fl]['POONZ4']['Analog-read'] = 0
                                     for revopoon2 in range(frame_list[fl]['POONCONREVO2']['Analog-read'],90):
                                                 print("Revolute conveyer 2: ",revopoon2) 
                                                 frame_list[fl]['POONCONREVO2']['Analog-read'] = revopoon2
                                                 req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})
                                     frame_list[fl]['POONZ4']['Analog-read'] = 100
                                     frame_list[fl]['POONZ5']['Analog-read'] = 100 
                                     for convy3 in range(frame_list[fl]['POONCONX5']['Analog-read'],0,-1):
                                                 print("Conveyer slider 3 ",convy3) 
                                                 frame_list[fl]['POONCONX5']['Analog-read'] = convy3
                                                 req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})
                                     #frame_list[fl]['POONZ5']['Analog-read'] = 0
                                     #frame_list[fl]['POONZ6']['Analog-read'] = 260 
                                     #Robotic arm pick and place poons 
                                     #Reading the position payload function 
                                     readarmpayload = open("/home/"+user_name+"/Remote_modified_joints/Robot_arm_parameters.json",'r')
                                     payloadarm = readarmpayload.read() #Reading the arm payload to manipulate the robot arm to the working area 
                                     armpayload = json.loads(payloadarm)
                                     standby_arm = armpayload['standby']
                                     default_arm = armpayload['default'] 
                                     poon2_arm = armpayload['poon2'] 
                                     #Forward arm position for poon2 positioning 
                                     if int(frame_list[fl]['IRB2']['Analog-read']) > default_arm['IRB2']['Analog-read']:
                                                print("Robotic arm standby mode activated")
                                                for st_angle in range(int(frame_list[fl]['IRB2']['Analog-read']),int(default_arm['IRB2']['Analog-read']),-1):
                                                                  frame_list[fl]['IRB2']['Analog-read'] = st_angle
                                                                  frame_list[fl]['IRB3']['Analog-read'] = st_angle 
                                                                  req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})
                                                frame_list[fl]['POONZ5']['Analog-read'] = 0
                                                frame_list[fl]['POONZ6']['Analog-read'] = 260                   
                                     if int(frame_list[fl]['IRB2']['Analog-read']) < default_arm['IRB2']['Analog-read']:
                                                print("Robotic arm standby mode activated")
                                                for st_angle in range(int(frame_list[fl]['IRB2']['Analog-read']),int(default_arm['IRB2']['Analog-read'])):
                                                                  frame_list[fl]['IRB2']['Analog-read'] = st_angle
                                                                  frame_list[fl]['IRB3']['Analog-read'] = st_angle 
                                                                  req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})
                                                frame_list[fl]['POONZ5']['Analog-read'] = 0    
                                                frame_list[fl]['POONZ6']['Analog-read'] = 260     
                                                     

                                     
                                     for se_angle in range(int(frame_list[fl]['IRB2']['Analog-read']),90,-1):
                                                        print("Control the Shoulder and Elbow joint angle: ",se_angle) 
                                                        frame_list[fl]['IRB2']['Analog-read'] = se_angle 
                                                        frame_list[fl]['IRB3']['Analog-read'] = se_angle 
                                                        req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})
                                     for base_angle in range(int(frame_list[fl]['IRB1']['Analog-read']),int(poon2_arm['IRB1']['Analog-read'])):
                                                        frame_list[fl]['IRB1']['Analog-read'] = base_angle 
                                                        req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})
                                                 
                                     calibrating_joint = ['IRB2','IRB3','IRB4','IRB5','IRB6'] 
                                     for ce in calibrating_joint:
                                           print("Calibrating joints data")
                                           joint_name = ce
                                           pos_joint = poon2_arm[ce] #getting the positiong joint angle for calibation  
                                              
                                     
                                           if frame_list[fl][joint_name]['Analog-read'] > pos_joint['Analog-read']:
                                                       print("Default joint angle more than target joint angle ",joint_name)
                                                       for angle_control in range(int(frame_list[fl][joint_name]['Analog-read']),int(pos_joint['Analog-read']),-1):
                                                                print("Now control max min: ",joint_name,angle_control)   
                                                                frame_list[fl][joint_name]['Analog-read'] = angle_control
                                                                req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})

                                           if frame_list[fl][joint_name]['Analog-read'] < pos_joint['Analog-read']:
                                                       print("Default joint angle lesser than target joint angle ",joint_name) 
                                                       for angle_control in range(int(frame_list[fl][joint_name]['Analog-read']),int(pos_joint['Analog-read'])):
                                                                print("Now control min max: ",joint_name,angle_control)
                                                                frame_list[fl][joint_name]['Analog-read'] = angle_control
                                                                req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})
                                                               
                                           if frame_list[fl][joint_name]['Analog-read'] == pos_joint['Analog-read']:
                                                       print("Default joint angle is equal to the target joint angle ",joint_name)
                                                       print("Adding the default joint angle data ",pos_joint['Analog-read']) 
                                                       frame_list[fl][joint_name]['Analog-read'] = pos_joint['Analog-read'] 
                                                       req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})
                                     frame_list[fl]['POONZ6']['Analog-read'] = 0 
                                     #Running the last pallett to send to the packaging machine 

                                     frame_list[fl][package_poons[2]]['Analog-read'] = frame_list[fl][poon_payload[1]]['Analog-read']-7 #frame_list[fl][poon_payload[0]]['Analog-read']                         
                                     #Backward arm to the default positioning 

                                     for base_angle in range(int(frame_list[fl]['IRB1']['Analog-read']),int(standby_arm['IRB1']['Analog-read']),-1):
                                                        frame_list[fl]['IRB1']['Analog-read'] = base_angle 
                                                        req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})  

                                     for se_angle in range(int(frame_list[fl]['IRB2']['Analog-read']),int(standby_arm['IRB2']['Analog-read'])):
                                                        print("Control the Shoulder and Elbow joint angle: ",se_angle) 
                                                        frame_list[fl]['IRB2']['Analog-read'] = se_angle 
                                                        frame_list[fl]['IRB3']['Analog-read'] = se_angle 
                                                        req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})   

                                     frame_list[fl]['IRB3']['Analog-read'] = standby_arm['IRB3']['Analog-read']                                
                                     #End effector calibration 
                                     endeffect_cab = ['IRB5','IRB6']  
                                     for ce in calibrating_joint:
                                           print("Calibrating joints data")
                                           joint_name = ce
                                           pos_joint = poon2_arm[ce] #getting the positiong joint angle for calibation  
                                              
                                     
                                           if frame_list[fl][joint_name]['Analog-read'] > standby_arm[joint_name]['Analog-read']:
                                                       print("Default joint angle more than target joint angle ",joint_name)
                                                       for angle_control in range(int(frame_list[fl][joint_name]['Analog-read']),int(standby_arm[joint_name]['Analog-read']),-1):
                                                                print("Now control max min: ",joint_name,angle_control)   
                                                                frame_list[fl][joint_name]['Analog-read'] = angle_control
                                                                req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})

                                           if frame_list[fl][joint_name]['Analog-read'] < standby_arm[joint_name]['Analog-read']:
                                                       print("Default joint angle lesser than target joint angle ",joint_name) 
                                                       for angle_control in range(int(frame_list[fl][joint_name]['Analog-read']),int(standby_arm[joint_name]['Analog-read'])):
                                                                print("Now control min max: ",joint_name,angle_control)
                                                                frame_list[fl][joint_name]['Analog-read'] = angle_control
                                                                req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})
                                                               
                                           if frame_list[fl][joint_name]['Analog-read'] == standby_arm[joint_name]['Analog-read']:
                                                       print("Default joint angle is equal to the target joint angle ",joint_name)
                                                       print("Adding the default joint angle data ",standby_arm[joint_name]['Analog-read']) 
                                                       frame_list[fl][joint_name]['Analog-read'] = standby_arm[joint_name]['Analog-read'] 
                                                       req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})  
                             store_complete['poon2'] = "complete"       
                  if poons_num <= 18:
                             print("Activate the poons controller 3")
                             for cr in range(0,8):
                                     print("Range of the motion: ",cr*6)
                                     #Update the poon payload data  
                                     frame_list[fl][poon_payload[2]]['Analog-read'] = 42-cr*6-1      #reduce the payload data of the current poons 
                                     req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}}) 
                                     #Reset the loop state function  
                                     frame_list[fl]['POONZ1']['Analog-read'] = 0 #Reset 
                                     frame_list[fl]['POONCONX1']['Analog-read'] = 0 #reset 
                                     frame_list[fl]['POONZ1']['Analog-read'] = 100
                                     frame_list[fl]['POONZ2']['Analog-read'] = 100 #Reset   
                                     frame_list[fl]['POONCONREVO1']['Analog-read'] = 0 
                                     frame_list[fl]['POONCONY3']['Analog-read'] = 0 #Reset the postiion of the conveyer sider 2 
                                     frame_list[fl]['POONCONREVO2']['Analog-read'] = 0 
                                     frame_list[fl]['POONZ4']['Analog-read'] =100
                                     frame_list[fl]['POONZ4']['Analog-read'] = 100
                                     frame_list[fl]['POONZ5']['Analog-read'] = 0
                                     frame_list[fl]['POONCONX5']['Analog-read'] = 330
                                     frame_list[fl]['POONZ6']['Analog-read'] = 0
                                     frame_list[fl]['PalletZ3']['Analog-read'] = 70
                                     frame_list[fl]['PalletX3']['Analog-read'] = 0
                                     frame_list[fl]['PalletZ4']['Analog-read'] = 100 
                                     frame_list[fl]['PalletX4']['Analog-read'] = 400 
                                     for convy in range(frame_list[fl]['POONCONX1']['Analog-read'],200):
                                                        
                                                        print("Processing the conveyer: ",convy)
                                                        frame_list[fl]['POONCONX1']['Analog-read'] = convy
                                                        req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})   
                                     frame_list[fl]['POONZ1']['Analog-read'] = 0
                                     #Revolute conveyer 1 
                                     frame_list[fl]['POONZ2']['Analog-read'] = 0 #Reset      
                                     #POONCONREVO1 Revolute default starter point 
                                     for revopoon in range(frame_list[fl]['POONCONREVO1']['Analog-read'],90):
                                                print("Revolute conveyer ",revopoon)
                                                frame_list[fl]['POONCONREVO1']['Analog-read'] = revopoon
                                                req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})
                                     #Hiding the revo poonz2 
                                     frame_list[fl]['POONZ2']['Analog-read'] = 100 #Hiding 
                                     #Loop control the conveyer 2 Slider X axis            
                                     frame_list[fl]['POONZ3']['Analog-read'] = 0 
                                     for convy2 in range(int(frame_list[fl]['POONCONY3']['Analog-read']),200):
                                               print("Conveyer 2 slider: ",convy2)
                                               frame_list[fl]['POONCONY3']['Analog-read'] = convy2
                                               req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})
                                     frame_list[fl]['POONZ3']['Analog-read'] = 100 #Hiding
                                     #Revolute conveyer 2 
                                     frame_list[fl]['POONZ4']['Analog-read'] = 0
                                     for revopoon2 in range(frame_list[fl]['POONCONREVO2']['Analog-read'],90):
                                                 print("Revolute conveyer 2: ",revopoon2) 
                                                 frame_list[fl]['POONCONREVO2']['Analog-read'] = revopoon2
                                                 req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})
                                     frame_list[fl]['POONZ4']['Analog-read'] = 100
                                     frame_list[fl]['POONZ5']['Analog-read'] = 100 
                                     for convy3 in range(frame_list[fl]['POONCONX5']['Analog-read'],0,-1):
                                                 print("Conveyer slider 3 ",convy3) 
                                                 frame_list[fl]['POONCONX5']['Analog-read'] = convy3
                                                 req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})
                                     #frame_list[fl]['POONZ5']['Analog-read'] = 0
                                     #frame_list[fl]['POONZ6']['Analog-read'] = 260 
                                     #Robotic arm pick and place poons 
                                     #Reading the position payload function 
                                     readarmpayload = open("/home/"+user_name+"/Remote_modified_joints/Robot_arm_parameters.json",'r')
                                     payloadarm = readarmpayload.read() #Reading the arm payload to manipulate the robot arm to the working area 
                                     armpayload = json.loads(payloadarm)
                                     standby_arm = armpayload['standby']
                                     default_arm = armpayload['default'] 
                                     poon3_arm = armpayload['poon3'] 
                                     #Forward arm position for poon1 positioning 
                                     if int(frame_list[fl]['IRB2']['Analog-read']) > default_arm['IRB2']['Analog-read']:
                                                print("Robotic arm standby mode activated")
                                                for st_angle in range(int(frame_list[fl]['IRB2']['Analog-read']),int(default_arm['IRB2']['Analog-read']),-1):
                                                                  frame_list[fl]['IRB2']['Analog-read'] = st_angle
                                                                  frame_list[fl]['IRB3']['Analog-read'] = st_angle 
                                                                  req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})
                                                frame_list[fl]['POONZ5']['Analog-read'] = 0
                                                frame_list[fl]['POONZ6']['Analog-read'] = 260                   
                                     if int(frame_list[fl]['IRB2']['Analog-read']) < default_arm['IRB2']['Analog-read']:
                                                print("Robotic arm standby mode activated")
                                                for st_angle in range(int(frame_list[fl]['IRB2']['Analog-read']),int(default_arm['IRB2']['Analog-read'])):
                                                                  frame_list[fl]['IRB2']['Analog-read'] = st_angle
                                                                  frame_list[fl]['IRB3']['Analog-read'] = st_angle 
                                                                  req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})
                                                frame_list[fl]['POONZ5']['Analog-read'] = 0    
                                                frame_list[fl]['POONZ6']['Analog-read'] = 260     
                                                     

                                     
                                     for se_angle in range(int(frame_list[fl]['IRB2']['Analog-read']),90,-1):
                                                        print("Control the Shoulder and Elbow joint angle: ",se_angle) 
                                                        frame_list[fl]['IRB2']['Analog-read'] = se_angle 
                                                        frame_list[fl]['IRB3']['Analog-read'] = se_angle 
                                                        req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})
                                     for base_angle in range(int(frame_list[fl]['IRB1']['Analog-read']),int(poon3_arm['IRB1']['Analog-read'])):
                                                        frame_list[fl]['IRB1']['Analog-read'] = base_angle 
                                                        req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})
                                                 
                                     calibrating_joint = ['IRB2','IRB3','IRB4','IRB5','IRB6'] 
                                     for ce in calibrating_joint:
                                           print("Calibrating joints data")
                                           joint_name = ce
                                           pos_joint = poon3_arm[ce] #getting the positiong joint angle for calibation  
                                              
                                     
                                           if frame_list[fl][joint_name]['Analog-read'] > pos_joint['Analog-read']:
                                                       print("Default joint angle more than target joint angle ",joint_name)
                                                       for angle_control in range(int(frame_list[fl][joint_name]['Analog-read']),int(pos_joint['Analog-read']),-1):
                                                                print("Now control max min: ",joint_name,angle_control)   
                                                                frame_list[fl][joint_name]['Analog-read'] = angle_control
                                                                req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})

                                           if frame_list[fl][joint_name]['Analog-read'] < pos_joint['Analog-read']:
                                                       print("Default joint angle lesser than target joint angle ",joint_name) 
                                                       for angle_control in range(int(frame_list[fl][joint_name]['Analog-read']),int(pos_joint['Analog-read'])):
                                                                print("Now control min max: ",joint_name,angle_control)
                                                                frame_list[fl][joint_name]['Analog-read'] = angle_control
                                                                req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})
                                                               
                                           if frame_list[fl][joint_name]['Analog-read'] == pos_joint['Analog-read']:
                                                       print("Default joint angle is equal to the target joint angle ",joint_name)
                                                       print("Adding the default joint angle data ",pos_joint['Analog-read']) 
                                                       frame_list[fl][joint_name]['Analog-read'] = pos_joint['Analog-read'] 
                                                       req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})
                                     frame_list[fl]['POONZ6']['Analog-read'] = 0 
                                     #Running the last pallett to send to the packaging machine 

                                     frame_list[fl][package_poons[3]]['Analog-read'] = frame_list[fl][poon_payload[2]]['Analog-read']-7 #frame_list[fl][poon_payload[0]]['Analog-read']                         
                                     #Backward arm to the default positioning 

                                     for base_angle in range(int(frame_list[fl]['IRB1']['Analog-read']),int(standby_arm['IRB1']['Analog-read']),-1):
                                                        frame_list[fl]['IRB1']['Analog-read'] = base_angle 
                                                        req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})  

                                     for se_angle in range(int(frame_list[fl]['IRB2']['Analog-read']),int(standby_arm['IRB2']['Analog-read'])):
                                                        print("Control the Shoulder and Elbow joint angle: ",se_angle) 
                                                        frame_list[fl]['IRB2']['Analog-read'] = se_angle 
                                                        frame_list[fl]['IRB3']['Analog-read'] = se_angle 
                                                        req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})   

                                     frame_list[fl]['IRB3']['Analog-read'] = standby_arm['IRB3']['Analog-read']                                
                                     #End effector calibration 
                                     endeffect_cab = ['IRB5','IRB6']  
                                     for ce in calibrating_joint:
                                           print("Calibrating joints data")
                                           joint_name = ce
                                           pos_joint = poon3_arm[ce] #getting the positiong joint angle for calibation  
                                              
                                     
                                           if frame_list[fl][joint_name]['Analog-read'] > standby_arm[joint_name]['Analog-read']:
                                                       print("Default joint angle more than target joint angle ",joint_name)
                                                       for angle_control in range(int(frame_list[fl][joint_name]['Analog-read']),int(standby_arm[joint_name]['Analog-read']),-1):
                                                                print("Now control max min: ",joint_name,angle_control)   
                                                                frame_list[fl][joint_name]['Analog-read'] = angle_control
                                                                req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})

                                           if frame_list[fl][joint_name]['Analog-read'] < standby_arm[joint_name]['Analog-read']:
                                                       print("Default joint angle lesser than target joint angle ",joint_name) 
                                                       for angle_control in range(int(frame_list[fl][joint_name]['Analog-read']),int(standby_arm[joint_name]['Analog-read'])):
                                                                print("Now control min max: ",joint_name,angle_control)
                                                                frame_list[fl][joint_name]['Analog-read'] = angle_control
                                                                req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})
                                                               
                                           if frame_list[fl][joint_name]['Analog-read'] == standby_arm[joint_name]['Analog-read']:
                                                       print("Default joint angle is equal to the target joint angle ",joint_name)
                                                       print("Adding the default joint angle data ",standby_arm[joint_name]['Analog-read']) 
                                                       frame_list[fl][joint_name]['Analog-read'] = standby_arm[joint_name]['Analog-read'] 
                                                       req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})  
                             store_complete['poon3'] = "complete"        
                  if poons_num <=24:
                             print("Activate the poons controller 4")
                             for ce in range(0,8):
                                     print("Range of the motion: ",ce*6)
                                     #Update the poon payload data  
                                     frame_list[fl][poon_payload[3]]['Analog-read'] = 42-ce*6-1    #reduce the payload data of the current poons 
                                     req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}}) 
                                     #Reset the loop state function  
                                     frame_list[fl]['POONZ1']['Analog-read'] = 0 #Reset 
                                     frame_list[fl]['POONCONX1']['Analog-read'] = 0 #reset 
                                     frame_list[fl]['POONZ1']['Analog-read'] = 100
                                     frame_list[fl]['POONZ2']['Analog-read'] = 100 #Reset   
                                     frame_list[fl]['POONCONREVO1']['Analog-read'] = 0 
                                     frame_list[fl]['POONCONY3']['Analog-read'] = 0 #Reset the postiion of the conveyer sider 2 
                                     frame_list[fl]['POONCONREVO2']['Analog-read'] = 0 
                                     frame_list[fl]['POONZ4']['Analog-read'] =100
                                     frame_list[fl]['POONZ4']['Analog-read'] = 100
                                     frame_list[fl]['POONZ5']['Analog-read'] = 0
                                     frame_list[fl]['POONCONX5']['Analog-read'] = 330
                                     frame_list[fl]['POONZ6']['Analog-read'] = 0
                                     frame_list[fl]['PalletZ3']['Analog-read'] = 70
                                     frame_list[fl]['PalletX3']['Analog-read'] = 0
                                     frame_list[fl]['PalletZ4']['Analog-read'] = 100 
                                     frame_list[fl]['PalletX4']['Analog-read'] = 400

                                     for convy in range(frame_list[fl]['POONCONX1']['Analog-read'],200):
                                                        
                                                        print("Processing the conveyer: ",convy)
                                                        frame_list[fl]['POONCONX1']['Analog-read'] = convy
                                                        req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})   
                                     frame_list[fl]['POONZ1']['Analog-read'] = 0
                                     #Revolute conveyer 1 
                                     frame_list[fl]['POONZ2']['Analog-read'] = 0 #Reset      
                                     #POONCONREVO1 Revolute default starter point 
                                     for revopoon in range(frame_list[fl]['POONCONREVO1']['Analog-read'],90):
                                                print("Revolute conveyer ",revopoon)
                                                frame_list[fl]['POONCONREVO1']['Analog-read'] = revopoon
                                                req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})
                                     #Hiding the revo poonz2 
                                     frame_list[fl]['POONZ2']['Analog-read'] = 100 #Hiding 
                                     #Loop control the conveyer 2 Slider X axis            
                                     frame_list[fl]['POONZ3']['Analog-read'] = 0 
                                     for convy2 in range(int(frame_list[fl]['POONCONY3']['Analog-read']),200):
                                               print("Conveyer 2 slider: ",convy2)
                                               frame_list[fl]['POONCONY3']['Analog-read'] = convy2
                                               req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})
                                     frame_list[fl]['POONZ3']['Analog-read'] = 100 #Hiding
                                     #Revolute conveyer 2 
                                     frame_list[fl]['POONZ4']['Analog-read'] = 0
                                     for revopoon2 in range(frame_list[fl]['POONCONREVO2']['Analog-read'],90):
                                                 print("Revolute conveyer 2: ",revopoon2) 
                                                 frame_list[fl]['POONCONREVO2']['Analog-read'] = revopoon2
                                                 req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})
                                     frame_list[fl]['POONZ4']['Analog-read'] = 100
                                     frame_list[fl]['POONZ5']['Analog-read'] = 100 
                                     for convy3 in range(frame_list[fl]['POONCONX5']['Analog-read'],0,-1):
                                                 print("Conveyer slider 3 ",convy3) 
                                                 frame_list[fl]['POONCONX5']['Analog-read'] = convy3
                                                 req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})
                                     #frame_list[fl]['POONZ5']['Analog-read'] = 0
                                     #frame_list[fl]['POONZ6']['Analog-read'] = 260 
                                     #Robotic arm pick and place poons 
                                     #Reading the position payload function 
                                     readarmpayload = open("/home/"+user_name+"/Remote_modified_joints/Robot_arm_parameters.json",'r')
                                     payloadarm = readarmpayload.read() #Reading the arm payload to manipulate the robot arm to the working area 
                                     armpayload = json.loads(payloadarm)
                                     standby_arm = armpayload['standby']
                                     default_arm = armpayload['default'] 
                                     poon4_arm = armpayload['poon4'] 
                                     #Forward arm position for poon1 positioning 
                                     if int(frame_list[fl]['IRB2']['Analog-read']) > default_arm['IRB2']['Analog-read']:
                                                print("Robotic arm standby mode activated")
                                                for st_angle in range(int(frame_list[fl]['IRB2']['Analog-read']),int(default_arm['IRB2']['Analog-read']),-1):
                                                                  frame_list[fl]['IRB2']['Analog-read'] = st_angle
                                                                  frame_list[fl]['IRB3']['Analog-read'] = st_angle 
                                                                  req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})
                                                frame_list[fl]['POONZ5']['Analog-read'] = 0
                                                frame_list[fl]['POONZ6']['Analog-read'] = 260                   
                                     if int(frame_list[fl]['IRB2']['Analog-read']) < default_arm['IRB2']['Analog-read']:
                                                print("Robotic arm standby mode activated")
                                                for st_angle in range(int(frame_list[fl]['IRB2']['Analog-read']),int(default_arm['IRB2']['Analog-read'])):
                                                                  frame_list[fl]['IRB2']['Analog-read'] = st_angle
                                                                  frame_list[fl]['IRB3']['Analog-read'] = st_angle 
                                                                  req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})
                                                frame_list[fl]['POONZ5']['Analog-read'] = 0    
                                                frame_list[fl]['POONZ6']['Analog-read'] = 260     
                                                     

                                     
                                     for se_angle in range(int(frame_list[fl]['IRB2']['Analog-read']),90,-1):
                                                        print("Control the Shoulder and Elbow joint angle: ",se_angle) 
                                                        frame_list[fl]['IRB2']['Analog-read'] = se_angle 
                                                        frame_list[fl]['IRB3']['Analog-read'] = se_angle 
                                                        req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})
                                     for base_angle in range(int(frame_list[fl]['IRB1']['Analog-read']),int(poon4_arm['IRB1']['Analog-read'])):
                                                        frame_list[fl]['IRB1']['Analog-read'] = base_angle 
                                                        req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})
                                                 
                                     calibrating_joint = ['IRB2','IRB3','IRB4','IRB5','IRB6'] 
                                     for ce in calibrating_joint:
                                           print("Calibrating joints data")
                                           joint_name = ce
                                           pos_joint = poon4_arm[ce] #getting the positiong joint angle for calibation  
                                              
                                     
                                           if frame_list[fl][joint_name]['Analog-read'] > pos_joint['Analog-read']:
                                                       print("Default joint angle more than target joint angle ",joint_name)
                                                       for angle_control in range(int(frame_list[fl][joint_name]['Analog-read']),int(pos_joint['Analog-read']),-1):
                                                                print("Now control max min: ",joint_name,angle_control)   
                                                                frame_list[fl][joint_name]['Analog-read'] = angle_control
                                                                req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})

                                           if frame_list[fl][joint_name]['Analog-read'] < pos_joint['Analog-read']:
                                                       print("Default joint angle lesser than target joint angle ",joint_name) 
                                                       for angle_control in range(int(frame_list[fl][joint_name]['Analog-read']),int(pos_joint['Analog-read'])):
                                                                print("Now control min max: ",joint_name,angle_control)
                                                                frame_list[fl][joint_name]['Analog-read'] = angle_control
                                                                req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})
                                                               
                                           if frame_list[fl][joint_name]['Analog-read'] == pos_joint['Analog-read']:
                                                       print("Default joint angle is equal to the target joint angle ",joint_name)
                                                       print("Adding the default joint angle data ",pos_joint['Analog-read']) 
                                                       frame_list[fl][joint_name]['Analog-read'] = pos_joint['Analog-read'] 
                                                       req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})
                                     frame_list[fl]['POONZ6']['Analog-read'] = 0 
                                     #Running the last pallett to send to the packaging machine 

                                     frame_list[fl][package_poons[1]]['Analog-read'] = frame_list[fl][poon_payload[3]]['Analog-read']-7 #frame_list[fl][poon_payload[0]]['Analog-read']                         
                                     #Backward arm to the default positioning 

                                     for base_angle in range(int(frame_list[fl]['IRB1']['Analog-read']),int(standby_arm['IRB1']['Analog-read']),-1):
                                                        frame_list[fl]['IRB1']['Analog-read'] = base_angle 
                                                        req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})  

                                     for se_angle in range(int(frame_list[fl]['IRB2']['Analog-read']),int(standby_arm['IRB2']['Analog-read'])):
                                                        print("Control the Shoulder and Elbow joint angle: ",se_angle) 
                                                        frame_list[fl]['IRB2']['Analog-read'] = se_angle 
                                                        frame_list[fl]['IRB3']['Analog-read'] = se_angle 
                                                        req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})   

                                     frame_list[fl]['IRB3']['Analog-read'] = standby_arm['IRB3']['Analog-read']                                
                                     #End effector calibration 
                                     endeffect_cab = ['IRB5','IRB6']  
                                     for ce in calibrating_joint:
                                           print("Calibrating joints data")
                                           joint_name = ce
                                           pos_joint = poon4_arm[ce] #getting the positiong joint angle for calibation  
                                              
                                     
                                           if frame_list[fl][joint_name]['Analog-read'] > standby_arm[joint_name]['Analog-read']:
                                                       print("Default joint angle more than target joint angle ",joint_name)
                                                       for angle_control in range(int(frame_list[fl][joint_name]['Analog-read']),int(standby_arm[joint_name]['Analog-read']),-1):
                                                                print("Now control max min: ",joint_name,angle_control)   
                                                                frame_list[fl][joint_name]['Analog-read'] = angle_control
                                                                req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})

                                           if frame_list[fl][joint_name]['Analog-read'] < standby_arm[joint_name]['Analog-read']:
                                                       print("Default joint angle lesser than target joint angle ",joint_name) 
                                                       for angle_control in range(int(frame_list[fl][joint_name]['Analog-read']),int(standby_arm[joint_name]['Analog-read'])):
                                                                print("Now control min max: ",joint_name,angle_control)
                                                                frame_list[fl][joint_name]['Analog-read'] = angle_control
                                                                req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})
                                                               
                                           if frame_list[fl][joint_name]['Analog-read'] == standby_arm[joint_name]['Analog-read']:
                                                       print("Default joint angle is equal to the target joint angle ",joint_name)
                                                       print("Adding the default joint angle data ",standby_arm[joint_name]['Analog-read']) 
                                                       frame_list[fl][joint_name]['Analog-read'] = standby_arm[joint_name]['Analog-read'] 
                                                       req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})  
                             store_complete['poon4'] = "complete"        
                  print("State task: ",store_complete,len(store_complete)) 
                                                      
                  if len(store_complete) == 4:
                                     #Activate the pallett slider to the packaging 
                                     for convy3 in range(frame_list[fl]['PalletX3']['Analog-read'],270):
                                             print("Converyer 3 slider: ",convy3) #Conveyer 3 position control slider 
                                             frame_list[fl]['PalletX3']['Analog-read'] = convy3 
                                             req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})  
                                     #Hiding palletZ3 slider  
                                     frame_list[fl]['PalletZ3']['Analog-read'] = 0 
                                     req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})  

                                     for t_pallet in range(frame_list[fl]['PalletX4']['Analog-read'],0,-1):
                                             print("Pallet 3 slider ",t_pallet) #Getting the palletX4 update the position data 
                                             frame_list[fl]['PalletX4']['Analog-read'] = t_pallet
                                             req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})  
                  
                  frame_list[fl]['PalletZ4']['Analog-read']  = 100                       
                  frame_list[fl]['PalletX4']['Analog-read'] = 100   
                  frame_list[fl][package_poons[4]] #Hard reset
                
                  
                  ''' 
                  #frame_list = {} 
                  req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})  
                  #End of process     
                  #Reset the positioning of the process after the complete the task 
                  read_frame = open('/home/'+user_name+'/Remote_modified_joints/motion_frame.json','r') #Get the list of the motion frame reader 
                  loader_frame = read_frame.read()
                  animation_frame  = json.loads(loader_frame) #Get the json payload  
                  print("Reading the animation animation frame data",animation_frame)
                  reset_list = animation_frame['motion_frame'] #Get the total frame list input to running in the loop 
                  #reset_list 
                  for rl in range(0,len(reset_list)-1):
                        print("Running the animation frame",reset_list[fl],list(reset_list[fl])[0]) #Detecting the key name of the actuation of the robot's motion
                        if rl == 0:
                            print("Initial frame reset ")  #Getting the initial position for the motion   
                            req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':reset_list[rl]}})    
                            frame_list[rl] = reset_list[rl]
                  #Reset the AMR position in the loop to the same position 
                  terminal_xdis = 10 
          
                  for amrdis_x in range(frame_list[fl]['AMRX']['Analog-read'],terminal_xdis,-1): #Getting the default paramter reading the JSON payload input 
                       print("Forward control AMR: ",amrdis_x) #Getting the JSON payload distance  
                       print("Default Pallet distance parameters: ",frame_list[fl]['PalletX1']['Analog-read'])
                       #Update the positioning data frame by frame 
                       frame_list[fl]['AMRX']['Analog-read'] = amrdis_x #Update the AMR distance position by frame
                       frame_list[fl]['PalletX1']['Analog-read'] = amrdis_x+30 #Compensate the distance of pallett X1 
                       req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})
                  #Rotate the AMR and Pallet at the same time 
                  for amrrevo_angle in range(frame_list[fl]['AMRREVO']['Analog-read'],91,-1):
                       print("Rotate AMR angle: ",amrrevo_angle)
                       frame_list[fl]['AMRREVO']['Analog-read'] = amrrevo_angle+0.5   
                       frame_list[fl]['PalletREVO1']['Analog-read'] = amrrevo_angle+0.5
                       req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})
                  #Placing the pallet in place after rotation 
                  for amrlift_range in range(frame_list[fl]['AMRZ']['Analog-read'],77): 
                        print("Range of the AMR lift: ",amrlift_range)  
                        frame_list[fl]['AMRZ']['Analog-read'] = amrlift_range
                        frame_list[fl]['PalletZ1']['Analog-read'] =  amrlift_range
                        req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}})
                  #Backward positioning control 
                  for amrdis_y in range(frame_list[fl]['AMRY']['Analog-read'],0,-1):
                        print("Bacward control AMR: ",amrdis_y)
                        frame_list[fl]['AMRY']['Analog-read'] = amrdis_y        
                        req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}}) 
                  #Rotate the backward position of AMR 
                  for amrrevo2_angle in range(int(frame_list[fl]['AMRREVO']['Analog-read']),0,-1):
                        print("Rotate the AMR back ward control",amrrevo2_angle) 
                        frame_list[fl]['AMRREVO']['Analog-read'] = amrrevo2_angle  
                        req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}}) 
                  #Forward to standby mode control 
                  for amrdis_x in range(frame_list[fl]['AMRX']['Analog-read'],270):
                        print("Forward moving to standby position",amrdis_x) 
                        frame_list[fl]['AMRX']['Analog-read'] = amrdis_x #Getting  the AMr to the new position           
                        req_feedback = requests.post('http://192.168.50.161:8000/feedback_sensor',json={'teslacoil358@gmail.com':{'BD3':frame_list[fl]}}) 
                  ''' 
          #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        
