

import phonenumbers
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError, SelectField
from wtforms.validators import DataRequired, Email, Length

class Form(FlaskForm):
    name = StringField("Name",
                       [DataRequired("You must enter name."),
                        Length(min=4, max=10, message='This field must contain from 4 to 10 symbols')
                        ]
                       )
    email = StringField('Email',
                        validators=[DataRequired("Please enter your email."), Email("Please enter correct email")])
    phone = StringField('Phone', )
    subject = SelectField('Subject', choices=[('en', 'English'), ('py', 'Python'), ('ma', 'Math')])
    message = StringField('Message', validators=[DataRequired(),
                                                 Length(max=500, message='This field can be up to 500 symbols')])

    # @staticmethod
    # def validate_phone(form, field):
    #     if len(field.data) > 13:
    #         raise ValidationError('Invalid phone number.')
    #     try:
    #         input_number = phonenumbers.parse(field.data)
    #         if not (phonenumbers.is_valid_number(input_number)):
    #             raise ValidationError('Invalid phone number.')
    #     except:
    #         input_number = phonenumbers.parse("+38" + field.data)
    #         if not (phonenumbers.is_valid_number(input_number)):
    #             raise ValidationError('Invalid phone number.')

    submit = SubmitField("Send")