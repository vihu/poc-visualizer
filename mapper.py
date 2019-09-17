"""
Generate mapping data.
"""

import folium
from hotspot import get_hotspots
from fetch import append_witnesses_and_receipts

def gen_marker(hotspot):
    '''
    Generate marker to place on map
    '''
    tooltip = 'Hotspot!'
    popup = ("<ul>"
             "<li>"
             f"<i>{hotspot.name}</i>"
             "</li>"
             "<li>"
             f"<i>receipt_count: {hotspot.receipts}</i>"
             "</li>"
             "<li>"
             f"<i>witness_count: {hotspot.witnesses}</i>"
             "</li>"
             "</ul>")
    return folium.Marker(location=(hotspot.lat, hotspot.long),
                         popup=popup,
                         tooltip=tooltip,
                         icon=folium.Icon(icon='cloud'))

def add_markers(map_obj, hotspots):
    '''
    Generate folium marker objects from hotspots list
    '''
    markers = [gen_marker(hotspot) for hotspot in hotspots]
    _ = list(map(map_obj.add_child, markers))
    return map_obj

def generate():
    '''
    Generate folium map
    '''
    all_hotspots = get_hotspots()
    hotspots = [h for h in all_hotspots if h.lat is not None]
    append_witnesses_and_receipts(hotspots)
    folium_map = folium.Map(zoom_start=14)
    add_markers(folium_map, hotspots)
    return folium_map

if __name__ == '__main__':
    pass
