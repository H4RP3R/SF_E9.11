from flask import render_template, flash, redirect, request, url_for
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import app, db
from app.forms import LoginForm, RegistrationForm, EventForm
from app.models import User, Event


@app.route('/')
@app.route('/index')
@login_required
def index():
    events = Event.query.all()
    return render_template('index.html', title='All Events', events=events)


@app.route('/add_event', methods=['GET', 'POST'])
@login_required
def add_event():
    form = EventForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(username=current_user.username).first()
            event = Event(
                start=form.start.data,
                end=form.end.data,
                theme=form.theme.data,
                description=form.description.data,
                author_id=user.id
            )
            db.session.add(event)
            db.session.commit()
            flash('Added new event.')

    return render_template('event.html', title='Add Event', header='New Event', form=form)


@app.route('/event/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_event(id):
    event = Event.query.get_or_404(id)
    if event.author_id != current_user.id:
        return render_template('404.html', title='404'), 404
    form = EventForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            event = Event.query.get(id)
            event.start = form.start.data
            event.end = form.end.data
            event.theme = form.theme.data
            event.description = form.description.data
            db.session.add(event)
            db.session.commit()
            flash('Changes saved.')

    form.start.data = event.start
    form.end.data = event.end
    form.theme.data = event.theme
    form.description.data = event.description
    form.submit.label.text = 'Save'

    return render_template(
        'event.html', title='Edit Event', header='Edit Event', form=form)


@app.route('/delete/<int:id>')
@login_required
def delete_event(id):
    event = db.session.query(Event).get_or_404(id)
    if event.author_id != current_user.id:
        return render_template('404.html', title='404'), 404
    db.session.delete(event)
    db.session.commit()
    flash('Event deleted')
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
