"""
Configuration for generating map
"""

from multiprocessing import Pool
import folium
import requests
import os
import js2py

API = "https://alamo.helium.foundation/api"
animalhash = js2py.require('angry-purple-tiger')

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
             f"<i>receipt_count: {receipts}</i>"
             "</li>"
             "<li>"
             f"<i>witness_count: {witnesses}</i>"
             "</li>"
             "</ul>")
    return folium.Marker(location=location,
                         popup=popup,
                         tooltip=tooltip,
                         icon=folium.Icon(icon='cloud'))

def add_markers(map_obj, hotspots):
    '''
    Generate folium marker objects from hotspots list
    '''
    hotspots = [i for i in hotspots[1:] if i['location'] != None]
    hotspot_addresses = [i['address'] for i in hotspots]
    hotspot_names = [animalhash(addr) for addr in hotspot_addresses]
    hotspot_locations = [(hotspot['lat'], hotspot['lng']) for hotspot in hotspots]
    rx_pool = Pool(10)
    hotspot_receipts = [rx_pool.apply(get_receipts, args=(addr, )) for addr in hotspot_addresses]
    wx_pool = Pool(10)
    hotspot_witnesses = [wx_pool.apply(get_witnesses, args=(addr, )) for addr in hotspot_addresses]
    data = zip(hotspot_names, hotspot_locations, hotspot_receipts, hotspot_witnesses)

    markers = [gen_marker(d) for d in data]
    _ = list(map(map_obj.add_child, markers))
    return map_obj

def generate_map():
    '''
    Generate folium map
    '''
    hotspots = get_hotspots()
    first_spot = hotspots[0]
    start_coords = (first_spot['lat'], first_spot['lng'])
    folium_map = folium.Map(location=start_coords, zoom_start=14)
    add_markers(folium_map, hotspots)
    return folium_map
