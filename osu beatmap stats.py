import requests
import json
import time
import gspread
import numpy as np

# f = open('osu results.json', 'r+')

key = 'KEY HERE'
limit = 50

PLAYERS = ['zzwhoops', 'DeathDrago', 'poizoni', 'autonoma', 'zzwhoops_wife', 'WaK3Up']

player = PLAYERS[2]
STATS_URL = 'https://osu.ppy.sh/api/get_user_best?k=' + key + '&u=' + player + '&limit=' + str(limit)
STATS_RESULT = requests.get(url=STATS_URL).json()

DATA = []

for x in STATS_RESULT:
    DATA.append(x['beatmap_id'])

TIMES = []

for id in DATA:
    BM_URL = 'https://osu.ppy.sh/api/get_beatmaps?k=' + key + '&b=' + id
    BM_RESULT = requests.get(url=BM_URL).json()

    TIMES.append(BM_RESULT[0]['total_length'])

print(TIMES)

total = 0
for x in TIMES:
    total += int(x)

print("Average map length: " + str(round(total / limit, 2)) + " seconds")

# f.write(str(RESULT))
# user_stats = json.dumps(get_stats(RESULT, DATA), indent=4)

# f.write(user_stats)
# f.close()