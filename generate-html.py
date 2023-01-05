class Game:
    def __init__(self, title, platform, rating, iconid, hundo, plat):
        self.title = title
        self.platform = platform
        self.rating = rating
        self.iconid = iconid
        self.hundo = hundo
        self.plat = plat
    def __str__(self):
        return self.title

import csv

game_list = []

with open('games.csv', mode ='r') as gamescsv:   
  file = csv.reader(gamescsv)
  for gl in file:
      game = Game(str(gl[0]), str(gl[3]), float(gl[5]), 10, int(gl[6]) == 1, int(gl[7]) == 1)
      game_list.append(game)

game_list = sorted(game_list, key=lambda game: game.title)