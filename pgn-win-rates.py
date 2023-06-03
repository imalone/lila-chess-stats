#!/usr/bin/env python

from functools import partial
from time import sleep
import argparse
import requests

import chess.pgn
import chess

retrytime=60

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

onlyratings =[1600,1800,2000,2200,2500]
onlyspeeds = ["blitz","rapid"]

parser = argparse.ArgumentParser(
    prog="pgn-win-rates.py",
    description="pull winning rates for pgn variations from a lila-openingexplorer host")
parser.add_argument("-p","--pgn", required=True,type=str, metavar="PGN",
                    help="Input PGN file. N.B. games should be separated by"+
                    " a double newline.")
parser.add_argument("-s","--speeds",default=None,type=str, metavar="SPEEDS",
                    help="Comma-separated list of time controls to retrieve"+
                    " allowed values "+
                    "ultraBullet,bullet,blitz,rapid,classical,correspondence")
parser.add_argument("-r","--ratings",default=None,type=str, metavar="RATINGS",
                    help="Comma-separated list of ratings to retrieve"+
                    " allowed values "+
                    "0,1000,1200,1400,1600,1800,2000,2200,2500")

args = parser.parse_args()

pgn = open(args.pgn)
if args.speeds is not None:
    onlyspeeds = args.speeds.split(",")
if args.ratings is not None:
    onlyratings = [ratings for ratings in map(int,args.ratings.split(","))]



def getEntryJSON(url, speeds, ratings, ucistr):
    while True:
        req = requests.get(url, params={"play":ucistr,
                                        "speeds":speeds,
                                        "ratings":ratings})
        if req.status_code == 200:
            break
        elif req.status_code == 429:
            sleep(retrytime)
        else:
            req.raise_for_status()
    return req.json()


for game in iter(partial(chess.pgn.read_game,pgn),None) :
    board = game.board()
    movelist = [ move for move in game.mainline_moves()]
    ucilist = [move.uci() for move in movelist]
    sanstr = board.variation_san(movelist)
    ucistr = ",".join(ucilist)
    opening = None
    for dbname, db in dbs.items():
        for speeds in db["speeds"]:
            if (onlyspeeds is not None and speeds is not None and
                speeds not in onlyspeeds):
                continue
            for ratings in db["ratings"]:
                if (onlyratings is not None and ratings is not None and
                    ratings not in onlyratings):
                    continue
                reqdat = getEntryJSON(db['url'],speeds,
                                      ratings,ucistr)
                if opening is None:
                    opening = reqdat['opening']
                report = ",".join(map(str,
                                       [sanstr,opening['eco'],opening['name'],dbname,speeds,ratings,reqdat['white'],reqdat['draws'],reqdat['black']]))
                print(report)
