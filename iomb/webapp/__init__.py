# experimental web-based user interface

from flask import Flask
import iomb.model as model
import json

app = Flask(__name__)


@app.route('/')
def root():
    return app.send_static_file('index.html')


@app.route('/api/sectors')
def sectors():
    l = []
    for s in app.model.sectors.mappings.values():
        l.append(s.__dict__)
    l.sort(key=lambda s: s['name'])
    data = json.dumps(l)
    return data, 200, {'Content-Type': 'application/json; charset=utf-8'}


def run(m: model.Model, port=8080):
    app.model = m
    app.run(port=port, debug=True)

if __name__ == '__main__':
    app.run(debug=True)
