from flask import Flask, Blueprint, render_template, url_for, redirect, request, flash
from flask_login import login_required, current_user
from . import db
from .models import User
from .models import Notes

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name = current_user.name)

@main.route('/new')
@login_required
def new_notes():
    return render_template('create_notes.html')

@main.route('/new', methods = ['POST'])
@login_required
def new_notes_post():
    subject = request.form.get('subject')
    comment = request.form.get('comment')

    notes = Notes(subject=subject, comment=comment, author=current_user)
    db.session.add(notes)
    db.session.commit()
    
    flash("New notes has been added")

    return redirect(url_for('main.user_notes'))

@main.route('/all')
@login_required
def user_notes():
    page = request.args.get('page', 1, type=int)
    notes = User.query.filter_by(email = current_user.email).first_or_404()
    user = current_user
    notes = Notes.query.filter_by(author=current_user).paginate(page=page, per_page=5)

    return render_template('all_notes.html', notes=notes, user=user)


@main.route("/notes/<int:notes_id>/update", methods=['GET', 'POST'])
@login_required
def update_notes(notes_id):
    notes = Notes.query.get_or_404(notes_id)
    if request.method == "POST":
        notes.subject = request.form['subject']
        notes.comment = request.form['comment']
        db.session.commit()
        flash('Your post has been updated!')
        return redirect(url_for('main.user_notes'))

    return render_template('update_notes.html', notes=notes)


@main.route("/notes/<int:notes_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_notes(notes_id):
    notes = Notes.query.get_or_404(notes_id)
    db.session.delete(notes)
    db.session.commit()
    flash('Your post has been deleted!')
    return redirect(url_for('main.user_notes'))