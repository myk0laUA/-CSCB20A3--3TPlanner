#imports
from flask import Flask, render_template, flash, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_sqlalchemy import SQLAlchemy
from werkzeug.urls import url_parse
from config import Config
from datetime import datetime, timedelta

#initialization
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# the following imports must be called after the initialization not to cause the input error.
from models import User, Task, Tip, Comment, Like
from forms import LoginForm, RegistrationForm, TaskForm, TipForm, CommentForm, SettingsForm

# create database tables before first request
@app.before_first_request
def create_tables():
    db.create_all()

# index route
@app.route('/')
def index():
    return render_template('index.html')

# manages the login use case. Uses the input to login form validates, and asks accordingly.
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('my_day'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password',category='danger')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('my_day')
        return redirect(next_page)
    return render_template('login.html', title='Login', form=form)

# logout route
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# manages the registration use case. Validates the input. If input is valid creates a new instance of user and updates the database.
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('my_day'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!', category='success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


# manages tasks of a user for the current day. It first instantiates a TaskForm object and checks if the form has been validated.
# If the form has been validated, it adds a new Task object to the database and redirects to the same page. If the total time spent on tasks in the day exceeds 8 hours, it flashes a warning message to the user.
@app.route('/my_day', methods=['GET', 'POST'])
@login_required
def my_day():
    form = TaskForm()
    if form.validate_on_submit():
        total_time = sum(task.duration for task in Task.query.filter_by(user_id=current_user.id, completed=False).all())
        if total_time + form.duration.data > 480:
            flash("You've reached the maximum allowed task time for the day. Please take care of yourself and get some rest.", category='warning')
            return redirect(url_for('my_day'))

        task = Task(title=form.title.data, duration=form.duration.data, user=current_user)
        db.session.add(task)
        db.session.commit()
        flash('Task added!', category='success')
        return redirect(url_for('my_day'))

    tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.timestamp.desc()).all()

    now = datetime.utcnow()
    planned_tasks = [task for task in tasks if not task.start_time and not task.completed]
    started_tasks = [task for task in tasks if task.start_time and not task.completed and task.start_time + timedelta(minutes=task.duration) > now]
    overdue_tasks = [task for task in tasks if task.start_time and not task.completed and task.start_time + timedelta(minutes=task.duration) <= now]

    return render_template('my_day.html', title='My Day', form=form, planned_tasks=planned_tasks, started_tasks=started_tasks, overdue_tasks=overdue_tasks)

@app.route('/start_task/<int:task_id>', methods=['POST'])
@login_required
def start_task(task_id):
    task = Task.query.get_or_404(task_id)

    task.start_time = datetime.utcnow()
    db.session.commit()
    flash('Task started', 'success')
    return redirect(url_for('my_day'))

# changes the status of the task from incomplete to complete.
@app.route('/complete_task/<int:task_id>', methods=['POST'])
@login_required
def complete_task(task_id):
    task = Task.query.get_or_404(task_id)

    task.completed = True
    db.session.commit()

    flash('Task completed.', 'success')
    return redirect(url_for('my_day'))


# used for displaying and submitting tips. It first creates a
# TipForm object, and on successful validation, adds a new Tip object to the database.
@app.route('/tips', methods=['GET', 'POST'])
@login_required
def tips():
    form = TipForm()
    if form.validate_on_submit():
        tip = Tip(content=form.content.data, user=current_user)
        current_user.tokens -= 20
        db.session.add(tip)
        db.session.commit()
        flash('Tip submitted!', category='success')
        return redirect(url_for('tips'))
    tips = Tip.query.order_by(Tip.timestamp.desc())
    return render_template('tips.html', title='Tips', form=form, tips=tips)


# displays a single tip with all comments.
@app.route('/tip/<int:tip_id>', methods=['GET', 'POST'])
@login_required
def view_tip(tip_id):
    tip = Tip.query.get_or_404(tip_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(content=form.content.data, user=current_user, tip=tip)
        db.session.add(comment)
        db.session.commit()
        flash('Comment added!', category='success')
        return redirect(url_for('view_tip', tip_id=tip_id))
    return render_template('view_tip.html', title='View Tip', tip=tip, form=form)


# used for submitting comments on tips.
@app.route('/add_comment/<int:tip_id>', methods=['POST'])
@login_required
def add_comment(tip_id):
    tip = Tip.query.get_or_404(tip_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(content=form.content.data, timestamp=datetime.now(), tip_id=tip_id, user_id=current_user.id)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been added.', category='success')
        return redirect(url_for('tips'))
    return render_template('add_comment.html', form=form, tip=tip)

#  adds or removes a like on a tip.
@app.route('/like_tip/<int:tip_id>', methods=['POST'])
@login_required
def like_tip(tip_id):
    tip = Tip.query.get_or_404(tip_id)
    like = Like.query.filter_by(user_id=current_user.id, tip_id=tip_id).first()
    if like:
        db.session.delete(like)
        db.session.commit()
        flash('You unliked this tip.', category='danger')
    else:
        like = Like(user_id=current_user.id, tip_id=tip_id)
        db.session.add(like)
        db.session.commit()
        flash('You liked this tip.',category='success')
    return redirect(url_for('tips'))


#  used for managing user settings. It creates a SettingsForm object and updates the user's information in the database on successful validation.
@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = SettingsForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        if form.profile_picture.data:
            current_user.save_profile_picture(form.profile_picture.data)
        current_user.dark_mode = form.dark_mode.data
        db.session.commit()
        flash('Your settings have been updated!', 'success')
        return redirect(url_for('settings'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.dark_mode.data = current_user.dark_mode
    return render_template('settings.html', form=form)

# used to provide additional context to templates.
@app.context_processor
def utility_processor():
    def get_brand():
        return "Friendly Task"
    return dict(get_brand=get_brand)

# starts the Flask application in debug mode.
if __name__ == '__main__':
    app.run(debug=True)