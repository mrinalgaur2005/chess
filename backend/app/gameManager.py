from .messages import INIT_GAME,MOVE
from .game import Game
from fastapi import WebSocket,WebSocketDisconnect
import json

class GameManager():
    def __init__(self) -> None:
        self.pendingUser=None
        self.user=[]
        self.games=[]
        
    async def addUser(self,socket:WebSocket):
        self.user.append(socket)
        await self.addHandler(socket)
        
    def removeUser(self,socket:WebSocket):
        self.user.remove(socket)
        
    async def addHandler(self, socket: WebSocket):
        print("Handler initiated")
        while True:
            try:
                data = await socket.receive_text()
                print(f"Received data: {data}")
                new = json.loads(data)
                msg_type = new.get('type')

                if msg_type == INIT_GAME:
                    print("INIT_GAME message received")
                    if self.pendingUser:
                        print(f"Pending user found: {self.pendingUser}")
                        game = Game(self.pendingUser, socket)
                        self.games.append(game)
                        print("Game created and added to games list")
                        self.pendingUser = None
                        print("Pending user set to None")
                        print("INIT_GAME success")
                    else:
                        self.pendingUser = socket
                        print("Pending user set")
                elif msg_type == MOVE:
                    print("MOVE message received")
                    move = new.get('payload')
                    for game in self.games:
                        if game.user2 == socket:
                            print("I am user2")
                        if game.user1 == socket or game.user2 == socket:
                            print("Inside game match if statement")
                            print(f"move is {move}")
                            await game.makeMove(socket, move)
                            print("Move made successfully")
            except WebSocketDisconnect:
                print("WebSocket disconnected")
                break
            except Exception as e:
                print(f"An error occurred: {e}")


            
            # data_move = await socket.receive_text()
            # print(data_move)  
            # new_data = json.loads(data_move)
            # print(new_data)
            # if new_data.get('type') == MOVE:
            #     print('Inside GameManager')
            #     move = new_data.get('move')
            #     for game in self.games:
            #         if game.user2 == socket:
            #             print("i am user2")
            #         if game.user1 == socket or game.user2 == socket:
            #             print("inside if statement")
            #             await game.makeMove(socket, move)
                    
        
        
        