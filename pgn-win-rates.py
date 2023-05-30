#!/usr/bin/env python

import chess.pgn
import chess
import requests
import json

dbloc ={
    "lichess": "https://explorer.lichess.ovh/lichess",
    "masters": "https://explorer.lichess.ovh/masters"
    }

#speeds
timecon =["ultraBullet","bullet","blitz","rapid","classical","correspondence"]
#ratings
rating  =[0,1000,1200,1400,1600,1800,2000,2200,2500]

pgn = open("test.pgn")
gameslist = []
while True:
    game= chess.pgn.read_game(pgn)
    if game is not None:
        gameslist.append(game)
    else: 
        break

for game in gameslist:
    ucilist = ",".join([x.uci() for x in game.mainline_moves()])
    print(ucilist)
    req = requests.get(dbloc['lichess'], params={"play":ucilist,"speeds":"rapid","rating":1000})
    reqdat = req.json()
    print(reqdat['white'],reqdat['draws'],reqdat['black'])

#for cur_game in chess.pgn.read_game(pgn):
#  print (",".join([x.uci() for x in cur_game.mainline_moves()]))
#  for x in cur_game.mainline_moves():
#      print (x)
