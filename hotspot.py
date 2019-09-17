'''
Hotspot model
'''
import requests
import js2py

BASE_URL = "https://alamo.helium.foundation/api/hotspots"
animalhash = js2py.require('angry-purple-tiger')

class Hotspot(object):
    '''
    Class to model hotspot data.
    '''
    def __init__(self):
        self.addr = None
        self.witnesses = 0
        self.receipts = 0
        self.lat = None
        self.long = None
        self.city = None
        self.name = None

    def __repr__(self):
        return (f"Hotspot(addr={self.addr},"
                f"witnesses={self.witnesses},"
                f"receipts={self.receipts},"
                f"city={self.city},"
                f"lat={self.lat},"
                f"long={self.long},"
                f"name={self.name}")

def get_hotspots():
    '''
    Get workable hotspot obj list.
    '''
    all_hotspots = fetch_hotspots()
    hotspots = []
    for hotspot in all_hotspots:
        new = Hotspot()
        new.addr = hotspot['address']
        new.lat = hotspot['lat']
        new.long = hotspot['lng']
        new.city = hotspot['short_city']
        new.name = animalhash(hotspot['address'])
        hotspots.append(new)
    return hotspots

def fetch_hotspots():
    '''
    Get hotspot data.
    '''
    r = requests.get(BASE_URL)
    if r.status_code == 200:
        hotspots = r.json()['data']
        return hotspots
    return Exception('Unable to get hotspots')

if __name__ == '__main__':
    pass
