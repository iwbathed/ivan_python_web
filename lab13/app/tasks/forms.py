from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired, Length
from flask_ckeditor import CKEditorField

from .models import Category
from app.models import User


def get_email_list():
    return [(user.id, user.email) for user in User.query.all()]


def get_category_list():
    return [(cat.id, cat.name) for cat in Category.query.all()]


class TaskForm(FlaskForm):
    title = StringField("Title",
                        [DataRequired("Please enter task title."),
                         Length(min=4, max=100, message='This field must be between 4 and 100 symbols')
                         ])
    description = CKEditorField('Description',
                                validators=[Length(max=2048, message='This field must be up to 2048 symbols')])
    deadline = DateField('Deadline')
    priority = SelectField('Priority', choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')])
    progress = SelectField('Progress', choices=[(1, 'Todo'), (2, 'Doing'), (3, 'Done')])
    category = SelectField("Category")
    submit = SubmitField("Send")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.category.choices = get_category_list()


class TaskDetailForm(FlaskForm):
    email = SelectField("Email")
    submit = SubmitField("Add")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.email.choices = get_email_list()


class CategoryForm(FlaskForm):
    name = StringField("Category",
                       [DataRequired("Please enter category name."),
                        Length(min=4, max=100, message='This field must be between 4 and 100 symbols')])
    submit = SubmitField("Add")


class CommentForm(FlaskForm):
    text = CKEditorField("Type your comment below",
                         [Length(min=10, max=1000, message='This field must be between 410 and 1000 symbols')])
    submit = SubmitField("Comment")
