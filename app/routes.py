from app import app, db, login, photos
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm, EditProfileForm, AssignmentForm, SubmitForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Assignment, Submissions
from werkzeug.urls import url_parse
from datetime import datetime

from ocr.ocr import get_text as ocr_module
#from semanticsimilarity.textsim similarity_module

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/')
@app.route('/index')
@login_required
def index():
    assignments = []
    submissions = Submissions.query.filter_by(uid=current_user.id).all()
    if current_user.teacher:
        assignments = [a for a in Assignment.query.all() if a.setter_username==current_user.username]
    else:
        assignments = Assignment.query.all()

    ass_sub = zip(assignments, submissions)
    return render_template('index.html', title='Home',  ass_sub=ass_sub)

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

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(name=form.name.data, username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        user.set_teacher(form.teacher.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    else:
        print(form.errors)
    return render_template('register.html', title='Register', form=form)

@app.route('/evaluate/<aid>', methods=['GET'])
@login_required
def evaluate(aid):
    if not current_user.teacher:
        flash("You are not authorised to view this page")
        return redirect(url_for('index'))
    submissions = Submissions.query.filter_by(aid=aid).all()
    render = []
    for submission in submissions:
        eval_score = eval_module(submission.imglink, aid)
        render.append((submission, eval_score))
    return render_template('evaluation.html', render=render)

def eval_module(imagelink, aid):
    assignment = Assignment.query.filter_by(id=aid).first_or_404()
    segments = segmentation_module(imagelink) or ['./tmp/1.png']
    score = 0
    for i, segment in enumerate(segments):
        ocr_text = ocr_module(segment)
        print(ocr_text)
        actual_answer = ''
        if i == 1:
            actual_answer = assignment.a1
        if i == 2:
            actual_answer = assignment.a2
        if i == 3:
            actual_answer = assignment.a3
        score += similarity_module(ocr_text, actual_answer)
    return score

def segmentation_module(imagelink):
    return False

#def ocr_module(segment):
#    return "Filler"

def similarity_module(submission, metric):
    return 0.5

@app.route('/assignment/<aid>', methods=['GET', 'POST'])
@login_required
def assignment(aid):
    assignment = Assignment.query.filter_by(id=aid).first_or_404()
    submission = Submissions.query.filter_by(aid=aid).filter_by(uid=current_user.id).first()
    form = SubmitForm()
    print("getting to before validation")
    if form.validate_on_submit():
        print("beyond validation:")
        image = form.photo.data
        #filename = secure_filename(image.filename)
        #file_url = os.path.join(app.config['UPLOADS_DEFAULT_DEST'], filename)
        #image.save(file_url)
        filename = photos.save(image)
        file_url = photos.url(filename)
        submission.imglink = file_url
        submission.submitted = True
        db.session.add(submission)
        db.session.commit()
        flash('Your answer has been submitted')
        return redirect(url_for('index'))
    else:
        print(form.errors)
    return render_template('assignment.html', assignment=assignment, submission=submission, form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        current_user.name = form.name.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
        form.name.data = current_user.name
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)

@app.route('/create_assignment', methods=['GET', 'POST'])
@login_required
def create_assignment():
    if not current_user.teacher:
        return redirect(url_for('index'))
    form = AssignmentForm()
    if form.validate_on_submit():
        q1 = form.q1.data
        q2 = form.q2.data
        q3 = form.q3.data
        a1 = form.a1.data
        a2 = form.a2.data
        a3 = form.a3.data
        
        asgn = Assignment(setter_username=current_user.username, q1=q1,q2=q2,q3=q3,a1=a1,a2=a2,a3=a3)
        for user in User.query.all():
            asgn.users.append(user)

        db.session.add(asgn)
        db.session.commit()

        aid = asgn.get_id()
        for user in asgn.users:
            uid = user.id
            sub = Submissions(uid=uid,aid=aid)
            sub.submitted = False
            db.session.add(sub)
        db.session.commit()
        flash('Published assignment')
        return redirect(url_for('index'))
    return render_template('create_assignment.html', title='Create Assignment', form=form)


