""" flask_example.py

    Required packages:
    - flask
    - folium

    Usage:

    Start the flask server by running:

        $ python flask_example.py

    And then head to http://127.0.0.1:5000/ in your browser to see the map displayed

"""

import folium
import requests
from multiprocessing import Pool
import os
from flask import Flask
import js2py

API = os.environ['API']
animalhash = js2py.require('angry-purple-tiger')

app = Flask(__name__)

def get_hotspots():
    '''
    Get hotspot data
    '''
    r = requests.get(f"{API}/hotspots")
    if r.status_code == 200:
        hotspots = r.json()['data']
        return hotspots
    return Exception('Unable to get hotspots')

def get_receipts(hotspot_address):
    '''
    Get receipts for a given hotspot_address
    '''
    r = requests.get(f"{API}/hotspots/{hotspot_address}/receipts")
    if r.status_code == 200:
        receipts = r.json()['data']
        return len(receipts)
    return Exception('Unable to get receipts for {hotspot_address}')

def get_witnesses(hotspot_address):
    '''
    Get witnesses for a given hotspot_address
    '''
    r = requests.get(f"{API}/hotspots/{hotspot_address}/witnesses")
    if r.status_code == 200:
        witnesses = r.json()['data']
        return len(witnesses)
    return Exception('Unable to get witnesses for {hotspot_address}')

def gen_marker(data):
    '''
    Generate marker to place on map
    '''
    name = data[0]
    location = data[1]
    receipts = data[2]
    witnesses = data[3]
    tooltip = 'Hotspot!'
    popup = ("<ul>"
             "<li>"
             f"<i>{name}</i>"
             "</li>"
             "<li>"
             f"<i>rx_total: {receipts}</i>"
             "</li>"
             "<li>"
             f"<i>wx_total: {witnesses}</i>"
             "</li>"
             "</ul>")
    return folium.Marker(location, popup, tooltip)

def add_markers(map_obj, hotspots):
    '''
    Generate folium marker objects from hotspots list
    '''
    hotspots = [i for i in hotspots[1:] if i['location'] != None]
    hotspot_addresses = [i['address'] for i in hotspots]
    hotspot_names = [animalhash(addr) for addr in hotspot_addresses]
    hotspot_locations = [(hotspot['lat'], hotspot['lng']) for hotspot in hotspots]
    rx_pool = Pool()
    hotspot_receipts = [rx_pool.apply(get_receipts, args=(addr, )) for addr in hotspot_addresses]
    wx_pool = Pool()
    hotspot_witnesses = [wx_pool.apply(get_witnesses, args=(addr, )) for addr in hotspot_addresses]
    data = zip(hotspot_names, hotspot_locations, hotspot_receipts, hotspot_witnesses)

    markers = [gen_marker(d) for d in data]
    _ = list(map(map_obj.add_child, markers))
    return map_obj

@app.route('/')
def index():
    hotspots = get_hotspots()
    first_spot = hotspots[0]
    start_coords = (first_spot['lat'], first_spot['lng'])

    folium_map = folium.Map(location=start_coords, zoom_start=14)

    add_markers(folium_map, hotspots)

    return folium_map._repr_html_()

if __name__ == '__main__':
    app.run(debug=True)
