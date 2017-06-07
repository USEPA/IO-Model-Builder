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
    m = models.get(model)  # type: Model
    if m is None:
        abort(404)
    l = []
    for s in m.sectors.values():
        l.append(s.as_json_dict())
    return jsonify(l)


@app.route('/api/<model>/indicators')
def get_indicators(model: str):
    m = models.get(model)  # type: Model
    if m is None:
        abort(404)
    l = []
    for i in m.indicators:
        l.append(i.as_json_dict())
    return jsonify(l)


@app.route('/api/<model>/matrix/<name>')
def get_matrix(model: str, name: str):
    m = models.get(model)  # type: Model
    if m is None:
        abort(404)
    if name in ('A', 'B', 'C', 'D', 'L', 'U'):
        return __get_numeric_matrix(m, name)
    elif name in ('B_dqi', 'D_dqi', 'U_dqi'):
        return __get_dqi_matrix(m, name)
    else:
        abort(404)


def __get_numeric_matrix(m: Model, name: str):
    mat = m.get_matrix(name)
    if mat is None:
        abort(404)
    col = __get_index_param('col', mat.shape[1])
    if col >= 0:
        return jsonify(mat[:, col].tolist())
    row = __get_index_param('row', mat.shape[0])
    if row >= 0:
        return jsonify(mat[row, :].tolist())
    return jsonify(mat.tolist())


def __get_dqi_matrix(m: Model, name: str):
    mat = m.get_dqi_matrix(name)
    if mat is None:
        abort(404)
    if len(mat) == 0:
        abort(404)
    col = __get_index_param('col', len(mat[0]))
    if col >= 0:
        vals = [row[col] for row in mat]
        return jsonify(vals)
    row = __get_index_param('row', len(mat))
    if row >= 0:
        return jsonify(mat[row])
    return jsonify(mat)


def __get_index_param(name: str, size: int) -> int:
    val = request.args.get(name)
    if val is None or len(val) == 0:
        return -1
    try:
        idx = int(val)
        if idx >= size:
            abort(400)
        return idx
    except:
        abort(400)


def serve(data_folder: str, port='5000'):
    for name in os.listdir(data_folder):
        f = os.path.join(data_folder, name)
        if os.path.isdir(f):
            # TODO: check model folder (all data present etc.)
            model = Model(f)
            models[name] = model
    app.run('0.0.0.0', port)
