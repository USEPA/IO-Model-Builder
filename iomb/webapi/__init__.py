import os

from .data import *

from flask import Flask, jsonify, request, send_from_directory, abort

app = Flask(__name__)
models = {}


# no caching -> just for dev ...
@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


@app.route('/api/models')
def get_models():
    l = []
    for model_id in models.keys():
        l.append({'id': model_id})
    return jsonify(l)


@app.route('/api/<model>/sectors')
def get_sectors(model: str):
    m = models.get(model)  # type: data.Model
    if m is None:
        abort(404)
    l = []
    for s in m.sectors.values():
        l.append(s.as_json_dict())
    return jsonify(l)


@app.route('/api/<model>/indicators')
def get_indicators(model: str):
    m = models.get(model)  # type: data.Model
    if m is None:
        abort(404)
    l = []
    for i in m.indicators:
        l.append(i.as_json_dict())
    return jsonify(l)


def serve(data_folder: str, port='5000'):
    for name in os.listdir(data_folder):
        f = os.path.join(data_folder, name)
        if os.path.isdir(f):
            # TODO: check model folder (all data present etc.)
            model = Model(f)
            models[name] = model
    app.run('0.0.0.0', port)
