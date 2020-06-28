import random
import math

class MLPlay:
    
    alive = True
    
    
    def __init__(self, player):
        self.player = player
        if self.player == "player1":
            self.player_no = 0
        elif self.player == "player2":
            self.player_no = 1
        elif self.player == "player3":
            self.player_no = 2
        elif self.player == "player4":
            self.player_no = 3
        self.car_vel = 0
        self.car_pos = ()
        global alive
        alive = True
        pass

    def update(self, scene_info):
        """
        Generate the command according to the received scene information
        """
        global alive
        if(alive):
            
            if scene_info["status"] != "ALIVE":
                alive=False
                return "RESET"
            
        
            run_dis = [900,950,1000,1100,1105,1100,1000,950,900]
            run_dis_sort=[997,998,999,1000,1001,1000,999,998,997]
            run_dis_num = [0,1,2,3,4,5,6,7,8]
            route_vel = [0,0,0,0,0,0,0,0,0]
            run_pos = [900,900,900,900,900,900,900,900,900]
            
            self.car_pos = scene_info[self.player]
            if( not self.car_pos ):
                return 
            for car in scene_info["cars_info"]:
                if car["id"]==self.player_no:
                    self.car_vel = car["velocity"]
            for car in scene_info["cars_info"]:
                if car["id"]!=self.player_no:
                    if car["pos"][1] - self.car_pos[1] < -90  :
                        vel = self.car_vel - car["velocity"]                        
                        safe_dis = 80 + 11*vel + 15         # safe
                        dis = self.car_pos[1] - car["pos"][1]
                        route = math.floor(car["pos"][0] / 70)
                        if dis - safe_dis < run_dis[route]:
                            route_vel[route] = car["velocity"]
                            run_dis[route] = dis - safe_dis
                            run_dis_sort[route] = dis - safe_dis
                            run_pos[route] = car["pos"][1]
                        else:
                            if car["velocity"] < route_vel[route]:
                                diff = route_vel[route] -  car["velocity"]
                                if car["pos"][1] < run_pos[route] - 160 :
                                     run_dis[route] -= 5*diff
                                elif car["pos"][1] < run_pos[route] : 
                                     run_dis[route] -= 10*diff   # brake dif
                        if car["id"] < 3 and (car["pos"][0] % 70 < 20 or car["pos"][0] % 70 > 50):
                            route_2 = 0
                            if(car["pos"][0] % 70 < 20): route_2 = route-1
                            else : route_2 = route+1
                            if dis - safe_dis < run_dis[route_2]:
                                run_dis[route_2] = dis - safe_dis 
                                run_dis_sort[route_2] = dis - safe_dis 
                            
                    elif car["pos"][1] - self.car_pos[1] >= -90 and car["pos"][1] - self.car_pos[1] < 70:
                        route = math.floor( car["pos"][0] / 70 )
                        run_dis[route] = -100
                        run_dis_sort[route]=-100
                        if car["id"] < 3 and (car["pos"][0] % 70 < 20 or car["pos"][0] % 70 > 50):
                            route_2 = 0
                            if(car["pos"][0] % 70 < 20): route_2 = route-1
                            else : route_2 = route+1
                            run_dis[route_2] = -100
                            run_dis_sort[route_2]=-100
                    elif car["pos"][1] - self.car_pos[1] > 70 and car["pos"][1] - self.car_pos[1] < 80:
                        vel = self.car_vel - car["velocity"]                        
                        safe_dis = 80 + 12*(-1)*vel + 13
                        dis = self.car_pos[1] - car["pos"][1]
                        route = math.floor(car["pos"][0] / 70)
                        if dis - safe_dis < run_dis[route]:
                            run_dis[route] = dis - safe_dis
                            run_dis_sort[route] = dis - safe_dis
                        if car["id"] < 3 and (car["pos"][0] % 70 < 20 or car["pos"][0] % 70 > 50):
                            route_2 = 0
                            if(car["pos"][0] % 70 < 20): route_2 = route-1
                            else : route_2 = route+1
                            if dis - safe_dis < run_dis[route_2]:
                                run_dis[route_2] = dis - safe_dis 
                                run_dis_sort[route_2] = dis - safe_dis 
            """print(self.player,run_dis)"""
            if scene_info.__contains__("coins") :
                for coin in scene_info["coins"]:
                    if abs(coin[0]-self.car_pos[0]) == 0 :
                        continue
                    if -(coin[1]-self.car_pos[1])/abs(coin[0]-self.car_pos[0]) >= 5/3:
                        route = math.floor(coin[0] / 70)
                        if(run_dis[route]>50):
                            run_dis[route] = run_dis[route] + abs(coin[0]-self.car_pos[0])*500
                            run_dis_sort[route] = run_dis_sort[route] + abs(coin[0]-self.car_pos[0])*500
            for i in range(0,8):
                for j in range(i+1,9):
                    if run_dis_sort[i] < run_dis_sort[j]:
                        temp = run_dis_num[i]
                        run_dis_num[i] = run_dis_num[j]
                        run_dis_num[j] = temp
                        temp = run_dis_sort[i]
                        run_dis_sort[i] = run_dis_sort[j]
                        run_dis_sort[j] = temp
            command=[]
            can_go = True
            go_route = 0
            
           
            
            self_route = math.floor((self.car_pos[0])/70)
            for i in range(0,9):
                
                can_go=True
                if(self_route == run_dis_num[i]):
                    if(self.car_pos[0] < 35+70*self_route):
                        command.append("MOVE_RIGHT")
                    elif(self.car_pos[0] > 35+70*self_route):
                        command.append("MOVE_LEFT")
                    go_route = run_dis_num[i]
                    break
                elif self_route < run_dis_num[i] :
                    for j in range(self_route+1,run_dis_num[i]+1):
                        if(run_dis[j] < 10):
                            can_go=False
                            break
                    if(self.car_pos[1]>730 and run_dis[self_route]>40):
                        can_go=False
                    if(not can_go):
                        
                        continue
                    else:
                        
                        go_route = run_dis_num[i]
                        command.append("MOVE_RIGHT")
                        break
                else:
                    for j in range(run_dis_num[i],self_route):                       
                        if(run_dis[j] < 10):
                            can_go=False
                            break
                    if(self.car_pos[1]>730 and run_dis[self_route]>40):
                        can_go=False
                    if(not can_go):
                        
                        continue
                    else:
                        
                        go_route = run_dis_num[i]
                        command.append("MOVE_LEFT")
                        break
                    
           
            
            left = self.car_pos[0]%70
            self_route_2 = self_route
            if(left < 15): self_route_2-=1
            elif(left > 55): self_route_2+=1
            
            if(self_route_2<0 or self_route_2>8):self_route_2=self_route
            
            
            if(scene_info["frame"]<150):
                command.append("SPEED")
                return command
            
            if(go_route < self_route):
                if(run_dis[self_route] > 20 and run_dis[self_route_2] > 20 and run_dis[self_route-1] > 20 ):
                    command.append("SPEED")
                elif(run_dis[self_route] > 10 and run_dis[self_route_2] > 10 and run_dis[self_route-1] > 10):
                    return command
                else:
                    command.append("BRAKE")
            elif(go_route > self_route):
                if(run_dis[self_route] > 20 and run_dis[self_route_2] > 20 and run_dis[self_route+1] > 20):
                    command.append("SPEED")
                elif(run_dis[self_route] > 10 and run_dis[self_route_2] > 10 and run_dis[self_route+1] > 10):
                    return command
                else:
                    command.append("BRAKE")
            else:
               if(run_dis[self_route] > 20 and run_dis[self_route_2] > 20 ):
                    command.append("SPEED")
               elif(run_dis[self_route] > 10 and run_dis[self_route_2] > 10 ):
                    return command
               else:
                    command.append("BRAKE")

            
           
            
            return command


    def reset(self):
        """
        Reset the status
        """
        pass
