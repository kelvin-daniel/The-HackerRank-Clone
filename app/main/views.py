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

@main.route('/submit', methods=['GET', 'POST'])
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
		flash('Your question has been recorded')
		return render_template('submit.html', form=form, users=getStandings())
	return render_template('submit.html', form=form, users=getStandings())

@main.route('/quiz', methods=['GET', 'POST'])
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


@main.route('/answer')
def fetch_answer():
	#id is the question id and userid is the User id
	#Storing the data from the request
	id = request.args.get('id', 0, type=int)
	value = request.args.get('value', 0, type=str)
	userId = request.args.get('userid', 0, type=int)

	#Fetching question and User data
	attempted_question = Questions.query.filter( Questions.questionid == id ).all()
	presentUser = User.query.get( userId )
	presentScore = presentUser.score

	#Appropirately changing the USER's score
	if attempted_question[0].answer == value:
		if attempted_question[0].difficulty == 'easy':
			presentScore = presentScore + 1
		elif attempted_question[0].difficulty == 'moderate':
			presentScore = presentScore + 2
		elif attempted_question[0].difficulty == 'hard':
			presentScore = presentScore + 3
		elif attempted_question[0].difficulty == 'insane':
			presentScore = presentScore + 4		
		
		presentUser.score = presentScore
		correct = 1
	else:
		presentScore = presentScore - 1
		presentUser.score = presentScore
		correct = 0


	beforePickle = current_user.answered
	afterPickle = loads(beforePickle)

	afterPickle.append(id)
	current_user.answered = dumps(afterPickle)
	db.session.commit()

	return jsonify(score = presentScore, correct = correct)

@main.route('/quiz/<string:category>')
@login_required
def categorywise(category):
	categoryList = ['math',
		'python',
		'Ruby',
		'C++',
		'C',
		'PHP',
		'JavaScript',
		'General',]
	if category in categoryList:
		form = QuizForm()
		if current_user.answered is None:
			current_user.answered = dumps([])
			db.session.commit()

		alreadyAns = loads(current_user.answered)
		#Check the questions to display
		questions_to_display = Questions.query.filter(Questions.creatorid != str(current_user.id)).filter( ~Questions.questionid.in_(alreadyAns)).filter( Questions.category == category ).all()

		if len(questions_to_display) is 0:
			flash("We're so sorry but it seems that there are no questions on this topic")
		return render_template('quiz.html', questions_to_display=questions_to_display, form=form, users=getStandings())
	else:
		form = QuizForm()
		if current_user.answered is None:
			current_user.answered = dumps([])
			db.session.commit()


		alreadyAns = loads(current_user.answered)
		#Check the questions to display
		questions_to_display = Questions.query.filter(Questions.creatorid != str(current_user.id)).filter( ~Questions.questionid.in_(alreadyAns)).all()
		flash('Please enter a url where the category is any one of' + str(categoryList))
		return redirect(url_for('quiz.html', questions_to_display=questions_to_display, form=form, users=getStandings()))

@main.route('/score')
@login_required
def scoreboard():
	#To allow sorting by username just do an ajax request back to score board with argument (like /score/#username then /score/#score)
	users = User.query.order_by(User.score.desc())
	return render_template('scoreboard.html', users=users)
