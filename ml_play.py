"""
The template of the script for the machine learning process in game pingpong
"""
'''

# Import the necessary modules and classes
from mlgame.communication import ml as comm
import pickle
import numpy as np
from os import path
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor

def ml_loop(side: str):
    """
    The main loop for the machine learning process
    The `side` parameter can be used for switch the code for either of both sides,
    so you can write the code for both sides in the same script. Such as:
    ```python
    if side == "1P":
        ml_loop_for_1P()
    else:
        ml_loop_for_2P()
    ```
    @param side The side which this script is executed for. Either "1P" or "2P".
    """

    # === Here is the execution order of the loop === #
    # 1. Put the initialization code here
    ball_served = False
    
    
    def move_to(player, pred) : #move platform to predicted position to catch ball 
        if player == '1P':
            if scene_info["platform_1P"][0]+20  > (pred-10) and scene_info["platform_1P"][0]+20 < (pred+10): return 0 # NONE
            elif scene_info["platform_1P"][0]+20 <= (pred-10) : return 2 # goes right
            else : return 1 # goes left
        else :
            if scene_info["platform_2P"][0]+20  > (pred-10) and scene_info["platform_2P"][0]+20 < (pred+10): return 0 # NONE
            elif scene_info["platform_2P"][0]+20 <= (pred-10) : return 2 # goes right
            else : return 1 # goes left
    
    def ml_loop_for_1P(feature): 
        x = 2
        if x + 1 < scene_info["platform_1P"][0]+30 and x - 1 > scene_info["platform_1P"][0]+10:
            
            if 420 - scene_info["ball"][1] <= 7:
                if scene_info["ball_speed"][0]>0:
                    return 2
                elif scene_info["ball_speed"][0]<0:
                    return 1
            else:
                return 0
        elif x + 1 >= scene_info["platform_1P"][0]+30:
            return 2
        elif x - 1 <= scene_info["platform_1P"][0]+10:
            return 1
    


    
    def ml_loop_for_2P():  # as same as 1P
        if scene_info["ball_speed"][1] > 0 : 
            return move_to(player = '2P',pred = 100)
        else : 
            x = ( scene_info["platform_2P"][1]+30-scene_info["ball"][1] ) // scene_info["ball_speed"][1] 
            pred = scene_info["ball"][0]+(scene_info["ball_speed"][0]*x) 
            bound = pred // 200 
            if (bound > 0):
                if (bound%2 == 0):
                    pred = pred - bound*200 
                else :
                    pred = 200 - (pred - 200*bound)
            elif (bound < 0) :
                if bound%2 ==1:
                    pred = abs(pred - (bound+1) *200)
                else :
                    pred = pred + (abs(bound)*200)
            return move_to(player = '2P',pred = pred)
    
    # 2. Inform the game process that ml process is ready
    comm.ml_ready()
    #s = [93,93]
    
    
    def get_direction(ball_x,ball_y,ball_pre_x,ball_pre_y):
        VectorX = ball_x - ball_pre_x
        VectorY = ball_y - ball_pre_y
        if(VectorX>=0 and VectorY>=0):
            return 0
        elif(VectorX>0 and VectorY<0):
            return 1
        elif(VectorX<0 and VectorY>0):
            return 2
        elif(VectorX<0 and VectorY<0):
            return 3
    
    def get_prediction(ball_x,ball_y,vector_x,vector_y):
        prediction = [0,0]
        prediction[0] = ball_x
        prediction[1] = ball_y
        vector = [0,0]
        vector[0] = vector_x
        vector[1] = vector_y
        
        if vector != [-1,-1]:
                while prediction[1]<=400 and prediction[1]>=100:
                    if prediction[0]<=0 or prediction[0]>=200:
                        vector[0]*=-1
                        prediction[0]+=vector[0]
                    else:
                        prediction[0]+=vector[0]
                    if prediction[1]<=0:
                        vector[1]*=-1
                        prediction[1]+=vector[1]
                    else:
                        prediction[1]+=vector[1]
        return prediction
    
    
    # 3. Start an endless loop
    while True:
        # 3.1. Receive the scene information sent from the game process
        scene_info = comm.recv_from_game()
        feature = []
        #feature.append(scene_info["platform_1P"][0])
        feature.append(scene_info["ball"][0])
        feature.append(scene_info["ball"][1])
        
        feature.append(scene_info["ball_speed"][0])
        feature.append(scene_info["ball_speed"][1])
        
        feature.append(scene_info["blocker"][1])
        
        pred = get_prediction(scene_info["ball"][0],scene_info["ball"][1],scene_info["ball_speed"][0],scene_info["ball_speed"][1])
        feature.append(pred[0])
        
        #feature.append(direction)
        

        #s = [scene_info["ball"][0], scene_info["ball"][1]]
        feature = np.array(feature)
        feature = feature.reshape((1,len(feature)))

        # 3.2. If either of two sides wins the game, do the updating or
        #      resetting stuff and inform the game process when the ml process
        #      is ready.
        if scene_info["status"] != "GAME_ALIVE":
            # Do some updating or resetting stuff
            ball_served = False

            # 3.2.1 Inform the game process that
            #       the ml process is ready for the next round
            comm.ml_ready()
            continue

        # 3.3 Put the code here to handle the scene information

        # 3.4 Send the instruction for this frame to the game process
        if not ball_served:
            comm.send_to_game({"frame": scene_info["frame"], "command": "SERVE_TO_LEFT"})
            ball_served = True
        else:
            if side == "1P":
                command = ml_loop_for_1P(feature)
            else:
                command = ml_loop_for_2P()

            if command == 0:
                comm.send_to_game({"frame": scene_info["frame"], "command": "NONE"})
            elif command == 2:
                comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_RIGHT"})
            else :
                comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_LEFT"})
'''
"""
The template of the script for the machine learning process in game pingpong
"""

# Import the necessary modules and classes
import pickle
from os import path

import numpy as np
from mlgame.communication import ml as comm

def ml_loop(side: str):
    """
    The main loop for the machine learning process
    The `side` parameter can be used for switch the code for either of both sides,
    so you can write the code for both sides in the same script. Such as:
    ```python
    if side == "1P":
        ml_loop_for_1P()
    else:
        ml_loop_for_2P()
    ```
    @param side The side which this script is executed for. Either "1P" or "2P".
    """

    # === Here is the execution order of the loop === #
    # 1. Put the initialization code here
    ball_served = False
    file = 'knn_nor.pickle'
    filename = path.join(path.dirname(__file__), 'save', file)
    with open(filename, 'rb') as file:
        clf_nor = pickle.load(file)
    
    file = 'knn_sli.pickle'
    filename = path.join(path.dirname(__file__), 'save', file)
    with open(filename, 'rb') as file:
        clf_sli = pickle.load(file)
    def move_to(player, pred) : #move platform to predicted position to catch ball 
        if player == '1P':
            if scene_info["platform_1P"][0]+20  > (pred-10) and scene_info["platform_1P"][0]+20 < (pred+10): return 0 # NONE
            elif scene_info["platform_1P"][0]+20 <= (pred-10) : return 1 # goes right
            else : return 2 # goes left
        else :
            if scene_info["platform_2P"][0]+20  > (pred-10) and scene_info["platform_2P"][0]+20 < (pred+10): return 0 # NONE
            elif scene_info["platform_2P"][0]+20 <= (pred-10) : return 1 # goes right
            else : return 2 # goes left

    def ml_loop_for_1P():
            feature = []
            feature.append(scene_info['ball'][0])
            feature.append(scene_info['ball'][1])
            feature.append(scene_info['ball_speed'][0])
            feature.append(scene_info['ball_speed'][1])
            feature.append(scene_info['blocker'][0])
            feature.append(scene_info['platform_1P'][0])
            feature.append(scene_info['blocker'][0] - tmp[0])
            feature = np.array(feature)
            feature = feature.reshape((-1,7))
            y = clf_nor.predict(feature)   
            return y

    def ml_loop_for_2P():  # as same as 1P
        if scene_info["ball_speed"][1] > 0 and scene_info['ball'][1] < 250:
            x = (390 - scene_info["ball"][1]) // scene_info["ball_speed"][1]
            pred = scene_info["ball"][0]+(scene_info["ball_speed"][0]*x)
            bound = pred // 200
            if (bound > 0): # pred > 200 # fix landing position
                if (bound%2 == 0) : 
                    pred = pred - bound*200                    
                else :
                    pred = 200 - (pred - 200*bound)
            elif (bound < 0) : # pred < 0
                if (bound%2 ==1) :
                    pred = abs(pred - (bound+1) *200)
                else :
                    pred = pred + (abs(bound)*200)
            return move_to(player = '1P',pred = pred)
        elif scene_info["ball_speed"][1] > 0 : 
            return move_to(player = '2P',pred = 100)
        else : 
            x = ( scene_info["platform_2P"][1]+30-scene_info["ball"][1] ) // scene_info["ball_speed"][1] 
            pred = scene_info["ball"][0]+(scene_info["ball_speed"][0]*x) 
            bound = pred // 200 
            if (bound > 0):
                if (bound%2 == 0):
                    pred = pred - bound*200 
                else :
                    pred = 200 - (pred - 200*bound)
            elif (bound < 0) :
                if bound%2 ==1:
                    pred = abs(pred - (bound+1) *200)
                else :
                    pred = pred + (abs(bound)*200)
            return move_to(player = '2P',pred = pred)


    # 2. Inform the game process that ml process is ready
    comm.ml_ready()

    # 3. Start an endless loop
    while True:
        # 3.1. Receive the scene information sent from the game process
        scene_info = comm.recv_from_game()
        prediction = [0,0]
        prediction[0] = scene_info["ball"][0]
        prediction[1] = scene_info["ball"][1]
        vector = [0,0]
        vector[0] = scene_info["ball_speed"][0]
        vector[1] = scene_info["ball_speed"][1]
        plat1y = 420 
        plat2y = 80
        if vector == [0,0]:
            prediction = prediction 
        else:
            while prediction[1] < plat1y:
                prediction[0] += vector[0]
                prediction[1] += vector[1]
                #print(prediction)
                if prediction[0] < 0:#x < 0
                    dx = 0 - prediction[0]
                    prediction[0] = 0
                    if vector[1] > 0:
                        prediction[1] -= dx
                    else:
                        prediction[1] += dx
                    vector[0] *= -1
                elif prediction[0] > 200:
                    dx = prediction[0] - 200
                    prediction[0] = 200
                    if vector[1] > 0:
                        prediction[1] -= dx
                    else:
                        prediction[1] += dx
                    vector[0] *= -1
                elif prediction[1] < plat2y:
                    dy = plat2y - prediction[1]
                    prediction[1] = plat2y
                    if vector[0] > 0:
                        prediction[0] -= dy
                    else:
                        prediction[0] += dy
                    vector[1] *= -1
                elif prediction[1] > plat1y:
                    dy = prediction[1] - plat1y
                    prediction[1] = plat1y
                    if vector[0] > 0:
                        prediction[0] -= dy
                    else:
                        prediction[0] += dy
                    vector[1] *= -1
        # 3.2. If either of two sides wins the game, do the updating or
        #      resetting stuff and inform the game process when the ml process
        #      is ready.
        if scene_info["status"] != "GAME_ALIVE":
            # Do some updating or resetting stuff
            ball_served = False

            # 3.2.1 Inform the game process that
            #       the ml process is ready for the next round
            comm.ml_ready()
            continue

        # 3.3 Put the code here to handle the scene information

        # 3.4 Send the instruction for this frame to the game process
        if not ball_served:
            if scene_info["ball_speed"][0] != 0:
                ball_served = True
            else:
                pass
            
        else:
            if side == "1P":
                if prediction[0] < scene_info["platform_1P"][0] + 30 and prediction[0] > scene_info["platform_1P"][0] +10:
                    command = 0
                elif prediction[0] >= scene_info["platform_1P"][0] + 30:
                    command = 1
                elif prediction[0] <= scene_info["platform_1P"][0] + 10:
                    command = 2
            else:
                command = ml_loop_for_2P()

            if command == 0:
                comm.send_to_game({"frame": scene_info["frame"], "command": "NONE"})
            elif command == 1:
                comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_RIGHT"})
            else :
                comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_LEFT"})
