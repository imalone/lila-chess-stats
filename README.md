# lila-chess-stats

This project aims to be able to collect chess position statistics from [lila-openingexplorer](https://github.com/lichess-org/lila-openingexplorer), for example lichess's Master and Player databases.

The idea is to be able to take an opening sequence and produce data such as win/draw rates by time control and rating. For example, convert the sequence 1.d4 c5 into


| time  | rating | white | black |
| ----- | ------ | ----- | ----- |
| blitz | 2500   | 49    | 48    |
| blitz | 2200   | 48    | 45    |
| blitz | 2000   | 47    | 48    |
| ...   |        |       |       |

Currently pgn-win-rates.py will query entries in a pgn file (-p arguemnt), query Lichess's master and player databases, and report its results (game counts for white win, draw, black win) for each mainline position found. If requests trigger the servers rate limit it will wait before continuing. The ratings and speeds to query in the player database can be controlled by -r and -s options.

Results look like this:
1. e4 e5 2. Nf3 Nc6 3. Bc4,C50,Italian Game,lichess,blitz,1200,9274322,640141,8174457
1. e4 e5 2. Nf3 Nc6 3. Bc4,C50,Italian Game,lichess,blitz,1400,11495424,820170,10219813
1. e4 e5 2. Nf3 Nc6 3. Bc4,C50,Italian Game,lichess,rapid,1200,3928876,290786,3333522

If you find yourself making serious use of this you may wish to consider donating to [lichess](https://lichess.org/) towards their server costs. If you find yourself making heavy use then you may want to consider hosting your own private lila-opening explorer instance, as it may well be faster than making queries to lichess's servers.