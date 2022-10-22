import json
import pandas as pds

with open("keyboard_config.json", 'r') as f:
    kb = json.load(f)
    # print(kb)
    freq_map = {}
    for k, v in kb.items():
        freq_map.update({v['frequency']: k})
    with open('freq_letter_map_new.json', 'w') as out:
        out.write(json.dumps(freq_map))
