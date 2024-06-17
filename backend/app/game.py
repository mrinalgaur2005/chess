from chess import Board,InvalidMoveError
from fastapi import WebSocket
from .messages import DISCONNECT,MOVE,INIT_GAME
import asyncio
import json


class Game():
    def __init__(self,user1:WebSocket,user2:WebSocket) -> None:
        self.user1=user1
        self.user2=user2
        self.board=Board()
        self.moves=[]
        
        data = json.dumps({
            'type': INIT_GAME,
            'payload': {
                'color': 'white'
            }
        })

        asyncio.create_task(self.user1.send_text(data))
        
        data = json.dumps({
            'type': INIT_GAME,
            'payload': {
                'color': 'black'
            }
        })

        asyncio.create_task(self.user2.send_text(data))

    

    async def makeMove(self,socket:WebSocket,move:str):
        print("in makeMoveve")
        print(self.moves)
        if (len(self.moves) % 2 ==0 and socket != self.user1):
            print("its in pass1")
            return
        if (len(self.moves) % 2 ==1 and socket != self.user2):
            print("its in pass2")
            return
                
        try:
            print("correct way")
            self.board.push_san(move)
            print("move done on board")
            if(len(self.moves) % 2 ==0):
                print("isnide game")
                data=json.dumps({
                    'type':MOVE,
                    'payload':move
                })
                await self.user1.send_text(data)
                
                
            else:
                print("inside user2")
                data=json.dumps({
                    'type':MOVE,
                    'payload':move
                })
                await self.user2.send_text(data)
                
                
            self.moves.append(move)
            print("inside the board")
            
        except InvalidMoveError:
            return
            
        
        if self.board.is_game_over():
            outcome = self.board.outcome()
            data = json.dumps({
                'type': DISCONNECT,
                'payload': {
                    'outcome': outcome.result(),
                    'winner': outcome.winner,
                    'termination': outcome.termination,
                }
            })
            await self.user1.send_text(data)
        
        
        
        
            
            
            
        
        
    
    