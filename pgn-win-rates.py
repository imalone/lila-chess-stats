#!/usr/bin/env python

import chess.pgn
import chess
import requests
import json
from functools import partial

dbs ={
    "lichess": {
        "url":"https://explorer.lichess.ovh/lichess",
        "speeds":["ultraBullet","bullet","blitz","rapid",
                  "classical","correspondence"],
        "ratings":[0,1000,1200,1400,1600,1800,2000,2200,2500]
    },
    "masters": {
        "url":"https://explorer.lichess.ovh/masters",
        "speeds":[None],
        "ratings":[None]
    }
}

pgn = open("test.pgn")

onlyratings = None
onlyspeeds = ["ultraBullet","bullet"]

for game in iter(partial(chess.pgn.read_game,pgn),None) :
    board = game.board()
    ucilist = []
    movelist = [ move for move in game.mainline_moves()]
    ucilist = [move.uci() for move in movelist]
    sanstr = board.variation_san(movelist)
    ucistr = ",".join(ucilist)
    for dbname, db in dbs.items():
        for speeds in db["speeds"]:
            if (onlyspeeds is not None and speeds is not None and
                speeds not in onlyspeeds):
                continue
            for ratings in db["ratings"]:
                if (onlyratings is not None and ratings is not None and
                    ratings not in onlyratings):
                    continue
                req = requests.get(db['url'],
                                   params={"play":ucistr,"speeds":speeds,
                                           "ratings":ratings})
                reqdat = req.json()
                report = ",".join(map(str,
                                       [sanstr,dbname,speeds,ratings,reqdat['white'],reqdat['draws'],reqdat['black']]))
                print(report)
