from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField, SelectField, validationError
from wtforms.validators import Required, Length, EqualTo

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about youself.',validators = [Required()])
    submit = SubmitField('Submit')

class SubmitForm(FlaskForm):
	question = TextAreaField('question', validators=[Required()])
	option1 = TextAreaField('option1', validators=[Required()])
	option2 = TextAreaField('option2', validators=[Required()])
	option3 = TextAreaField('option3', validators=[Required()])
	option4 = TextAreaField('option4', validators=[Required()])
	answer = SelectField(
		'answer', 
		choices=[('option1', 'A'), ('option2', 'B'), ('option3', 'C'), ('option4', 'D')], 
		validators=[Required()]
	)
	category = SelectField(
		'category', 
		choices=[('math', 'Math'), ('python', 'Python'), ('Ruby', 'Ruby'), ('C++', 'C++'), ('C', 'C'), ('PHP', 'PHP'), ('JavaScript', 'JavaScript'), ('General', 'General')], 
		validators=[Required()]
	)
	difficulty = SelectField(
		'Difficulty', 
		choices=[('easy', 'Easy'), ('moderate', 'Moderate'), ('hard', 'Hard'), ('insane', 'Insane')],
		validators=[Required()]
	)

class QuizForm(FlaskForm):
	attempted_answer = SelectField(
		'attempted_answer',
		choices=[('option1', 'A'), ('option2', 'B'), ('option3', 'C'), ('option4', 'D')],
		validators=[Required()]
	)