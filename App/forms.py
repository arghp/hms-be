
from flask_wtf import FlaskForm
from wtforms import SelectField, DateField, StringField, SubmitField, IntegerField, DateTimeField
from wtforms.validators import DataRequired

class BookingForm(FlaskForm):
    room_type = SelectField('Room Type', choices=[], validators=[DataRequired()])
    check_in_date = DateField('Check-In Date', format='%Y-%m-%d', validators=[DataRequired()])
    check_out_date = DateField('Check-Out Date', format='%Y-%m-%d', validators=[DataRequired()])
    special_requests = StringField('Special Requests')
    submit = SubmitField('Book')


class PromotionForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    discount = IntegerField('Discount Percentage', validators=[DataRequired()])
    start_date = DateTimeField('Start Date', validators=[DataRequired()])
    end_date = DateTimeField('End Date', validators=[DataRequired()])
    room_type = StringField('Room Type', validators=[DataRequired()])
    submit = SubmitField('Create Promotion')