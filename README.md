# lila-chess-stats

This project aims to be able to collect chess position statistics from [lila-openingexplorer](https://github.com/lichess-org/lila-openingexplorer), for example lichess's Master and Player databases.

The idea is to be able to take an opening sequence and produce data such as win/draw rates by time control and rating. For example, convert the sequence 1.d4 c5 into


| time  | rating | white | black |
| ----- | ------ | ----- | ----- |
| blitz | 2500   | 49    | 48    |
| blitz | 2200   | 48    | 45    |
| blitz | 2000   | 47    | 48    |
| ...   |        |       |       |

Currently pgn-win-rates.py will query entries in a pgn file (test.pgn), query Lichess's master and player databases, and report its results (game counts for white win, draw, black win) for each mainline position found. If requests trigger the servers rate limit it will wait before continuing.

Results look like this:
1. e4 e5 2. Nf3 Nc6 3. Bc4,lichess,blitz,1600,10339727,791029,9225226
1. e4 e5 2. Nf3 Nc6 3. Bc4,lichess,blitz,1800,6855871,584130,6239764
1. e4 e5 2. Nf3 Nc6 3. Bc4,lichess,blitz,2000,2863512,286746,2703096

If you find yourself making serious use of this you may wish to consider donating to [lichess](https://lichess.org/) towards their server costs. If you find yourself making heavy use then you may want to consider hosting your own private lila-opening explorer instance, as it may well be faster than making queries to lichess's servers.