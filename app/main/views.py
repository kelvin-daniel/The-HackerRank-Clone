from flask import render_template,redirect,url_for,abort,request,flash,jsonify,session
from flask_login import login_required,current_user
from . import main
from .forms import *
from ..models import *
from .. import db, photos
import markdown2
from pickle import loads, dumps
import json
from .forms import SubmitForm, QuizForm

@main.route('/')
def index():
    return render_template('index.html',users=getStandings())

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path 
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))
    
    return render_template('profile/update.html',form =form)

@app.route('/submit', methods=['GET', 'POST'])
@login_required
def submit():
	form = SubmitForm()
	if form.validate_on_submit():
		questiondata = Questions(
			question=form.question.data,
			option1=form.option1.data,
			option2=form.option2.data,
			option3=form.option3.data,
			option4=form.option4.data,
			answer=form.answer.data,
			creatorid=current_user.id,
			category=form.category.data,
			difficulty=form.difficulty.data
		)
		db.session.add(questiondata)
		db.session.commit()
		flash('Your question has been nestled deep within the quizzing engine')
		return render_template('submit.html', form=form, users=getStandings())
	return render_template('submit.html', form=form, users=getStandings())

@app.route('/quiz', methods=['GET', 'POST'])
@login_required
def quiz():
	form = QuizForm()
	if current_user.answered is None:
		current_user.answered = dumps([])
		db.session.commit()
		questions_to_display = Questions.query.filter(Questions.creatorid != str(current_user.id)).all()
		return render_template('quiz.html', questions_to_display=questions_to_display, form=form, users=getStandings())

	else:
		alreadyAns = loads(current_user.answered)
		#Check the questions to display
		questions_to_display = Questions.query.filter(Questions.creatorid != str(current_user.id)).filter( ~Questions.questionid.in_(alreadyAns)).all()
		return render_template('quiz.html', questions_to_display=questions_to_display, form=form, users=getStandings())