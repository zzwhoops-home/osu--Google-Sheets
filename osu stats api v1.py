import requests
import json
import time
import gspread
import numpy as np

# f = open('osu results.json', 'r+')

key = 'ENTER KEY HERE'

PLAYERS = ['zzwhoops', 'Okabe Lintahlo', 'DeathDrago', 'poizoni', 'autonoma', 'zzwhoops_wife', 'WaK3Up', 'syci']
DATA = ['pp_rank', 'pp_country_rank', 'pp_raw', 'ranked_score', 'total_score', 'count300', 'count100', 'count50', 'accuracy', 'playcount', 'total_seconds_played']

gc = gspread.service_account(filename='C:/Users/Zachary Deng/Desktop/Zachs Stuff/Python/Projects/python programs/osu! Google Sheets/osu-profiles-5c706e652467.json')

sheet = gc.open_by_key('SPREADSHEET URL HERE')
stats_worksheet = sheet.worksheet("User Stats")
recent_worksheet = sheet.worksheet("Recent Plays")

alphabet = "abcdefghijklmnopqrstuvwxyz"

def next_available_col(worksheet):
    str_list = list(filter(None, worksheet.row_values(1)))
    return str(len(str_list) + 1)

def get_stats(stats_result, data):
    stats_result = stats_result[0]
    final_stats = {}
    next_col = next_available_col(stats_worksheet)

    avatar = stats_result['user_id']

    url = 'https://a.ppy.sh/' + str(id)
    
    final_stats['username'] = stats_result['username']
    
    try:
        for val in data:
            final_stats[val] = stats_result[val]
    except KeyError:
        pass

    col_letter = alphabet[int(next_col) - 1]
    update_vals = list(final_stats.values())
    update_range = f'{col_letter}1:{col_letter}{len(update_vals)}'

    stats_worksheet.update(update_range, transpose(update_vals), value_input_option="USER_ENTERED")

    return(final_stats)

def get_recent_plays(recent_result):
    print(recent_result)

def transpose(arr):
    transposed = []
    for val in arr:
        transposed.append([val])
    return(transposed)

while True:
    sheet.values_clear("B1:Z12")

    for player in PLAYERS:
        STATS_URL = 'https://osu.ppy.sh/api/get_user?k=' + key + '&u=' + player
        RECENT_URL = 'https://osu.ppy.sh/api/get_user_recent?k=' + key + '&u=' + player
        STATS_RESULT = requests.get(url=STATS_URL).json()
        RECENT_RESULT = requests.get(url=RECENT_URL).json()
        get_stats(STATS_RESULT, DATA)
        get_recent_plays(RECENT_RESULT)
    time.sleep(1800)


# f.write(str(RESULT))
# user_stats = json.dumps(get_stats(RESULT, DATA), indent=4)

# f.write(user_stats)
# f.close()