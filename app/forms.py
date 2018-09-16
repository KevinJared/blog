from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField
from wtforms.validators import Required

class PostForm(FlaskForm):
    category = SelectField('Category', choices=[('Technology','Technology'),('Pickuplines','Pickuplines'),('BusinessPitch','Business Pitch'),('Sales','Sales'),('Interview','Interview')])
    post = TextAreaField(('Say something'), validators=[Required()])
    submit = SubmitField(('Submit'))

class CommentForm(FlaskForm):
    details = StringField('Write a comment',validators=[Required()])
    submit = SubmitField('Comment')