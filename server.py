import asyncio
import json
from aiohttp import web
import aiohttp
import os
import mimetypes

class RPSGameServer:
    def __init__(self):
        self.players = []
        self.choices = {}
        self.scores = [0, 0]
        self.game_started = False
        
    async def register(self, ws):
        if len(self.players) >= 2:
            await ws.send_json({
                'type': 'error',
                'message': 'Game is full. Only 2 players allowed.'
            })
            return False
            
        self.players.append(ws)
        player_num = len(self.players)
        
        await ws.send_json({
            'type': 'connected',
            'player_num': player_num,
            'message': f'You are Player {player_num}'
        })
        
        print(f"Player {player_num} connected")
        
        if len(self.players) == 2:
            self.game_started = True
            await self.broadcast({
                'type': 'game_start',
                'message': 'Both players connected! Game starting...'
            })
            await self.start_round()
        else:
            await ws.send_json({
                'type': 'waiting',
                'message': 'Waiting for opponent...'
            })
            
        return True