from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, SubmitField, IntegerField, HiddenField
from wtforms.validators import Required
from models import User


class LoginForm(Form):
    openid = TextField('openid', validators=[Required()])
    remember_me = BooleanField('remember_me', default=False)
    submit = SubmitField('Login')


class EditForm(Form):
    nickname = TextField('nickname', validators=[Required()])

    def __init__(self, original_nickname, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.original_nickname = original_nickname

    def validate(self):
        if not Form.validate(self):
            return False
        if self.nickname.data == self.original_nickname:
            return True
        user = User.query.filter_by(nickname=self.nickname.data).first()
        if user != None:
            self.nickname.errors.append(
                'This nickname is already in use. Please choose another one.')
            return False
        return True

class SavedGraphForm(Form):
    graph_name = TextField('Graph Name', validators = [Required()])
    keyword_1 = HiddenField('', validators = [Required()])
    keyword_2 = HiddenField('')
    date_low =HiddenField('', validators = [Required()])
    date_high = HiddenField('', validators = [Required()])
    granularity = HiddenField('', validators=[Required()])
    submit = SubmitField('Save Graph')


class DeleteGraph(Form):
    graph_id = IntegerField('')
    submit = SubmitField('Delete')


class KeywordSearchForm(Form):
    keyword_1 = TextField('Keyword 1', validators = [Required()])
    keyword_2 = TextField('Keyword 2', validators = [Required()])
    submit = SubmitField('Graph!')

