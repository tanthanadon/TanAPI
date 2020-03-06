from flask import Flask, jsonify, render_template, request
import os
import json
from pathlib import Path
import numpy as np
import pandas as pd

from math import sin, cos, sqrt, atan2, radians

# Thaadwada

"""
Mefaefaa
"""

'''
wadwadawd
wadad
'''

'''
wdawdwadw
awdawdwadwa
'''
#dwadawdawdw
#dwadadwdw

app = Flask(__name__)

@app.route('/')
def results():
    url = "https://www.google.com"
    
    return jsonify({"result":  country_list})

@app.route('/AddressLookup')


def query_example():
    #if key doesn't exist, returns None
    lat = request.args.get('lat')
    long = request.args.get('long')
    print(type(lat))
    print(type(long))
    distance = []
    filename = Path('/home/thanadon/TanAPI/data.json')
    data = json.loads(filename.read_text())
    

    for i in data:
        # print(i['city'])
        # print(type(i['lat']))
        # print(type(i['long']))
        
        d = calculateDistance(lat, long, i['lat'], i['long'])
        distance.append(d)
        i['distance'] = d
        print(d)

    df = pd.DataFrame(data)
    df.sort_values('distance', ascending=True, inplace=True)
    print(df)

    
    return '''<h1>{0}</h1>'''.format(df.iloc[0, 0])

def calculateDistance(lat, long, lat2, lon2):
    R = 6373.0
    lon1 = float(long)
    lat1 = float(lat)
    
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    
    a = sin(dlat / 2)
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return  R * c

if __name__ == "__main__":
    app.run(debug=True)


