'''
flask web app
'''

from flask import Flask
from config import generate_map
import redis

app = Flask(__name__)
redis = redis.Redis(host='redis', port=6379)

@app.route('/')
def index():
    folium_map = generate_map()
    return folium_map._repr_html_()

if __name__ == '__main__':
    print(f'redis: {redis.client_list()}')
    print(f'{redis.ping()}')

    app.run(host='0.0.0.0', port=5000, debug=True)
