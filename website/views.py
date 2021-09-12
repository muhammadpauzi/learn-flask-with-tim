from flask import Blueprint, render_template, request, flash, jsonify
import json
from flask_login import login_required, current_user
from .models import Note
from . import db

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        body = request.form.get('body')

        if len(body.strip()) < 1:
            flash('Content must be required.', category='error')
        else:
            new_note = Note(body=body, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template('home.html', user=current_user)

@views.route('/delete', methods=['DELETE'])
@login_required
def delete_note():
    noteID = json.loads(request.data)['id']
    note = Note.query.get(noteID)
    if note and note.user_id == current_user.id:
        db.session.delete(note)
        db.session.commit()
    return jsonify({})
