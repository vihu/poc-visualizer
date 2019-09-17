'''
Basic flask application
'''

from flask import Flask
from mapper import generate

app = Flask(__name__)

@app.route('/')
def index():
    folium_map = generate()
    return folium_map._repr_html_()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
