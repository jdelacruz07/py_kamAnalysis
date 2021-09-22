from flask import (
    Blueprint, request
)
from werkzeug.exceptions import abort

from analysis.auth import login_required
from analysis.db import get_db
from flask import json

bp = Blueprint('gap', __name__,url_prefix='/gap')

@bp.route('')
def get_gaps():
    db = get_db()
    gaps = db.execute(
            'SELECT *'
            ' FROM gap '
            ' ORDER BY dateSelected DESC'
            ).fetchall()
    result = [dict(gap) for gap in gaps]
    return json.jsonify(result)

@bp.route('', methods=('POST',))
@login_required
def add_gap():
    print("Agregar gap: ",request.get_json())
    request_data = request.get_json()
    isClose = request_data['isClose']
    dateSelected = request_data['dateSelected']
    try:
        db = get_db()
        db.execute(
           'INSERT INTO gap (isClose, dateSelected)'
            ' VALUES (?, ?)', (isClose, dateSelected ))
        db.commit()
    
        gap = get_gap(dateSelected)
        return json.jsonify(gap)
    except:
        print("Fecha duplicada ")
        db.rollback()
        abort(302)

def get_gap(id):
    if type(id) == str:
        gap = get_db().execute(
            'SELECT *'
            ' FROM  gap'
            ' WHERE dateSelected = ?',(id,)
           ).fetchone()
    else:
        gap = get_db().execute(
            'SELECT *'
            ' FROM  gap'
            ' WHERE id = ?',(id,)
           ).fetchone()

    if gap is None:
        abort(404, f"Gap id {id} doesn't exist.")

    return dict(gap)

@bp.route('', methods=('PUT',))
@login_required
def update_gap():
    print("Este es el gap a actualizar ", request.get_json())
    data = request.get_json()
    isClose = data['isClose']
    dateSelected = data['dateSelected']
    id = data['id']
    gap = get_gap(id)

    db = get_db()
    db.execute(
                'UPDATE gap SET isClose = ?, dateSelected = ?'
                ' WHERE id = ?',
                (isClose, dateSelected, id)
            )
    db.commit()
    gap = get_gap(id)
    return json.jsonify(gap)

    
@bp.route('<int:id>', methods=('DELETE',))
@login_required
def delete(id):
    gap = get_gap(id)
    print("Gap a eliminar ", gap)
    
    db = get_db()
    db.execute('DELETE FROM gap WHERE id = ?', (id,))
    db.commit()
    
    return json.jsonify(gap)
    
class Gap:
    def __init__(self, id, isClose, dateSelected):
        self.dateSelected = dateSelected
        self.isClose = isClose
        self.id = id

def jsonDefault(object):
    return object.__dict__