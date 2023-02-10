from datetime import datetime
import csv
import math


class Game:
    def __init__(self, title, platform, rating, iconid, hundo, plat, year, hours, playthroughs):
        self.title = title
        self.platform = platform
        self.rating = rating
        self.iconid = iconid
        self.hundo = hundo
        self.plat = plat
        self.year = year
        self.hours = hours
        self.playthroughs = playthroughs


def get_quicknav_html():
    start = "<h2>Quick Navigation</h2>\n<p>\n"
    end = "</p>\n"
    links = "<a class=\"qn-link\" href=\"#qn-num\">#</a>\n"
    for letter in alphabet:
        links += "<a class=\"qn-link\" href=\"#qn-" + letter + "\">" + letter.upper() + "</a>\n"
    return start + links + end

def get_quicknav_anchor(letter):
    return "<span id=\"qn-" + letter + "\"></span>"

def get_rating_html(rating):
    start = "<span class=\"gamecard-rating flex\">"
    fullstars = rating // 1
    hashalf = not rating // 1 == rating
    empties = 5 - math.ceil(rating)
    content = "<img src=\"/resources/gif/star-filled.gif\">" * int(fullstars)
    if hashalf:
        content += "<img src=\"/resources/gif/star-half.gif\">"
    if empties > 0:
        content += "<img src=\"/resources/gif/star-empty.gif\">" * int(empties)
    end = "</span>"
    return start + content + end

def get_playtext(game):
    hourstext = str(game.hours) + " hours"
    playthroughtext = ""
    if game.playthroughs == 0:
        playthroughtext = " (incomplete)"
    elif game.playthroughs > 1:
        playthroughtext = ", played " + str(game.playthroughs) + " times"
    return hourstext + playthroughtext

def get_listing_html(game):
    start = "<div class=\"gamecard flex card\">\n<div class=\"gamecard-outer flex\">\n<img id=\"i"
    start += game.iconid + "\" alt=\"icon\" src=\"/resources/png/blank.png\">\n"
    start += "<div class=\"gamecard-inner flex\">\n"    
    platform = game.platform
    if platform in ["DS", "3DS", "Switch", "Wii"]:
        platform = "Nintendo " + platform
    if platform == "iOS":
        platform = "Mobile (iOS)"
    content = "<span class=\"gamecard-subtext\">" + game.year + "</span>\n"
    content += "<span class=\"gamecard-subtext\">" + platform + "</span>\n"
    content += get_rating_html(game.rating) + "\n"
    content += "</div>\n</div>\n"
    content += "<span class=\"gamecard-title\">" + game.title
    if game.hundo:
        content += " <img id=\"100\" alt=\"100\" src=\"/resources/png/100.png\">"
    if game.plat:
        content += "<img id=\"plat\" alt=\"plat\" src=\"/resources/png/plat.png\">"
    content += "</span>\n<span class=\"gamecard-playtext\" style=\"font-size:12px\">" + get_playtext(game) + "</span>"
    end = "</div>"
    return start + content + end

def get_icon_css(iconid):
    filename = "icons.png"
    if iconid[0:2] == "01":
        filename = "icons2.png"
    x = int(iconid[4:6])
    x *= -64
    y = int(iconid[2:4])
    y *= -64
    return "img#i" + iconid + "{background:url(/resources/png/" + filename + ") " + str(x) + "px " + str(y) + "px}"

def calc_stats():
    for game in game_list:
        # rating
        if game.rating == 5:
            stat_ratings[0][1] += 1
        elif game.rating == 4.5:
            stat_ratings[1][1] += 1
        elif game.rating == 4:
            stat_ratings[2][1] += 1
        elif game.rating == 3.5:
            stat_ratings[3][1] += 1
        elif game.rating == 3:
            stat_ratings[4][1] += 1
        elif game.rating == 2.5:
            stat_ratings[5][1] += 1
        else:
            stat_ratings[6][1] += 1
        # platform
        if game.platform == "PlayStation":
            stat_platforms[0][1] += 1
        elif game.platform in ["PlayStation 1", "PlayStation 2"]:
            stat_platforms[1][1] += 1
        elif game.platform in ["3DS", "DS", "DSi", "DSiWare"]:
            stat_platforms[2][1] += 1
        elif game.platform == "Switch":
            stat_platforms[3][1] += 1
        elif game.platform == "Wii":
            stat_platforms[4][1] += 1
        elif game.platform == "PC":
            stat_platforms[5][1] += 1
        else:
            stat_platforms[6][1] += 1
        # completion
        if game.hundo:
            stat_completion[0][1] += 1
        if game.plat:
            stat_completion[1][1] += 1  

def get_single_stat_html(title, values):
    content = "<div class=\"stat\">\n<span class=\"bold\">" + title + "</span><br>\n"
    for v in values:
        content += v[0] + " (" + str(v[1]) + ")<br>\n"
    # return without last <br> and add newline
    return content[:-5] + "</div>\n"

def get_stats_html():
    start = "<h2>Statistics</h2>\n<div class=\"stat-container\">\n"
    content = get_single_stat_html("Platforms", stat_platforms)
    content += get_single_stat_html("Ratings", stat_ratings)
    content += get_single_stat_html("Completion", stat_completion)
    end = "</div>\n<p>Total games: " + str(len(game_list)) + "</p>\n"
    return start + content + end


alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
                "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
datestring = datetime.today().strftime("%B%e, %Y at %I:%M %p")
if "at 0" in datestring:
    datestring = datestring.replace("at 0", "at ")
pageheader = "---\npermalink: /game-records/\nlayout: wnesenior\ntitle: Game Records\nbase_url: /\nlast_updated: "
pageheader += datestring + "\n---\n\n"
signaturehtml = "<!-- Generated by https://github.com/egartley/game-records !-->\n"
signaturehtml += "<link href=\"/resources/css/game-records.css\" rel=\"stylesheet\" type=\"text/css\">\n"
signaturehtml += "<p>This is a record of every game I've played since around 2006 or so. Each game has a rating out of 5, "
signaturehtml += "a rough estimate of the total play time, and the number of times played if more than once. Games that "
signaturehtml += "have been 100% completed include a tag next to the title, and those that I've gotten the platinum "
signaturehtml += "trophy for also have an icon. A vast majority was played on original hardware, however "
signaturehtml += "some of the older titles were emulated.</p>\n"
listinghtml = "<h2>All Games Played</h2>\n<div class=\"gamecard-container flex\">\n" + get_quicknav_anchor("#") + "\n"

alphabet_index = 0
lastletter = ""
nummode = True
game_list = []
iconcss = ""
stat_ratings = [["5 stars", 0], ["4.5 stars", 0], ["4 stars", 0], ["3.5 stars", 0],
                ["3 stars", 0], ["2.5 stars", 0], ["2 stars or below", 0]]
stat_platforms = [["PS4/PS5", 0], ["PS1/PS2", 0], ["3DS/DS/DSi", 0], ["Switch", 0],
                  ["Wii", 0], ["PC", 0], ["Other", 0]]
stat_completion = [["100% Complete", 0], ["Platinum Trophy", 0]]

# build list of game objects from csv
with open("games.csv", mode="r") as gamescsv:   
  file = csv.reader(gamescsv)
  for gl in file:
      game = Game(str(gl[0]), str(gl[3]), float(gl[5]), str(gl[8]), int(gl[6]) == 1, int(gl[7]) == 1, str(gl[2]), int(gl[9]), int(gl[10]))
      game_list.append(game)

# sort alphabetically by game title
game_list = sorted(game_list, key=lambda game: game.title)

# build non-listing html
calc_stats()
statshtml = get_stats_html()
quicknavhtml = get_quicknav_html()
mischtml = statshtml + quicknavhtml

# build listing html
for game in game_list:
    lastletter = game.title[0:1].upper()
    # check if finished with numbered titles
    if nummode and lastletter.isalpha():
        # finished with numbered titles, output quick link nav for A
        nummode = False
        listinghtml += get_quicknav_anchor(alphabet[alphabet_index]) + "\n"
    if not nummode:
        while not alphabet[alphabet_index].upper() == lastletter:
            # output quick nav link for the new letter
            alphabet_index += 1
            listinghtml += get_quicknav_anchor(alphabet[alphabet_index]) + "\n"
    listinghtml += get_listing_html(game)

# add remaining quick nav links
while alphabet_index < len(alphabet) - 1:
    alphabet_index += 1
    listinghtml += get_quicknav_anchor(alphabet[alphabet_index]) + "\n"
listinghtml += "</div>\n"

# output to actual HTML file
with open("game-records.html", mode="w") as outfile:
    outfile.write(pageheader + signaturehtml + mischtml + listinghtml)

# build CSS for icons
iconcss = "div.gamecard-container{display:flex;flex-direction:row;flex-wrap:wrap;align-items:center}"
iconcss += "div.gamecard-outer>img{height:64px;width:64px;box-shadow:0 0 4px #000}"
iconcss += "span.gamecard-title{font-size:16px;font-weight:700;padding-top:8px}"
iconcss += "span.gamecard-title>img{margin-left:4px}span.gamecard-subtext{font-size:12px;font-style:italic}"
iconcss += "div.gamecard{width:180px;padding:16px 16px 8px 16px;margin-right:24px;margin-bottom:24px;height:fit-content}"
iconcss += "div.gamecard-inner{justify-content:center;margin-left:8px}"
iconcss += "div.gamecard,div.gamecard-inner{flex-direction:column}"
iconcss += "div.gamecard-outer,span.gamecard-rating{flex-direction:row}a.qn-link{margin-right:10px;font-size:18px}"
iconcss += "div.stat-container{display:flex;flex-direction:row}div.stat{margin-right:28px}"
iconcss += "@media screen and (max-width:1072px){div.stat-container{flex-direction:column}}"

for game in game_list:
    iconcss += get_icon_css(game.iconid)

# output to actual CSS file
with open("game-records.css", mode="w") as outfile:
    outfile.write(iconcss)

print("Done!")
