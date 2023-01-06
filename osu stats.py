import requests
import json
import gspread
import numpy as np

# f = open('osu results.json', 'r+')

access_token = 'ACCESS TOKEN HERE'
access = 'Bearer ' + access_token

PLAYERS = ['zzwhoops', 'DeathDrago', 'poizoni', 'autonoma', 'zzwhoops_wife']
DATA = ['global_rank', 'country_rank', 'pp', 'ranked_score', 'total_score', 'total_hits', 'hit_accuracy', 'play_count', 'play_time']

PARAMS = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': access
}

gc = gspread.service_account(filename='C:/Users/Zachary Deng/Desktop/Zach\'s Stuff/Python/Projects/python programs/osu! Google Sheets/osu-profiles-5c706e652467.json')

sheet = gc.open_by_key('SPREADSHEET URL HERE')
worksheet = sheet.worksheet("User Stats")


alphabet = "abcdefghijklmnopqrstuvwxyz"

def get_auth_code():
    url = 'https://osu.ppy.sh/oauth/token'
    f = open('osu stats.json', 'r+')

    data = {
        'client_id': CLIENT_ID,
        'client_secret': 'CLIENT_SECRET',
        'code': 'CODE',
        'grant_type': 'authorization_code',
        'redirect_uri': 'http://example.com/'
    }

    x = requests.post(url, data=data)
    print(x.text)
    f.writelines(x.text)
    f.close()



def next_available_col(worksheet):
    str_list = list(filter(None, worksheet.row_values(1)))
    return str(len(str_list) + 1)

def get_stats(result, data):
    stats = result["statistics"]
    final_stats = {}
    next_col = next_available_col(worksheet)

    avatar = result['id']
    url = 'https://a.ppy.sh/' + str(id)
    
    final_stats['username'] = result['username']
    
    try:
        for val in data:
            final_stats[val] = stats[val]
    except KeyError:
        pass

    col_letter = alphabet[int(next_col) - 1]
    update_vals = list(final_stats.values())
    update_range = f'{col_letter}1:{col_letter}{len(update_vals)}'

    worksheet.update(update_range, transpose(update_vals))

    return(final_stats)

def transpose(arr):
    transposed = []
    for val in arr:
        transposed.append([val])
    return(transposed)

sheet.values_clear("B1:Z")

for player in PLAYERS:
    URL = 'https://osu.ppy.sh/api/v2/users/' + player + '/'
    RESULT = requests.get(url=URL, headers=PARAMS).json()
    get_stats(RESULT, DATA)


# f.write(str(RESULT))
# user_stats = json.dumps(get_stats(RESULT, DATA), indent=4)

# f.write(user_stats)
# f.close()