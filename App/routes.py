from datetime import date

from flask import Blueprint, request, redirect, url_for, flash, render_template, session
from werkzeug.security import check_password_hash
from . import db
from .Models.models import User, Room, Booking, Promotion
from .forms import BookingForm, PromotionForm


bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET'])
def home():
    return 'Hello, World!'

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.user_id
            # store additional user details in the session
            session['username'] = user.username
            session['first_name'] = user.first_name
            session['last_name'] = user.last_name
            flash('Logged in successfully.')
            return redirect(url_for('dashboard'))

        flash('Invalid username or password.')

    return render_template('login.html')


@bp.route('/rooms', methods=['GET'])
def get_rooms():
    rooms = Room.query.all()
    return render_template('rooms.html', rooms=rooms)


@bp.route('/book', methods=['GET', 'POST'])
def book():
    form = BookingForm()
    form.room_type.choices = [(room.room_type, room.room_type) for room in Room.query.distinct(Room.room_type)]
    if form.validate_on_submit():
        booking = Booking(
            user_id=session['user_id'],
            room_id=Room.query.filter_by(room_type=form.room_type.data).first().room_id,
            check_in_date=form.check_in_date.data,
            check_out_date=form.check_out_date.data,
            special_requests=form.special_requests.data
        )
        db.session.add(booking)
        db.session.commit()
        flash('Booking successful.')
        return redirect(url_for('dashboard'))
    return render_template('book.html', form=form)


@bp.route('/promotions/create', methods=['GET', 'POST'])
def create_promotion():
    form = PromotionForm()
    if form.validate_on_submit():
        new_promotion = Promotion(
            title=form.title.data,
            discount=form.discount.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            room_type=form.room_type.data
        )
        db.session.add(new_promotion)
        db.session.commit()
        flash('Promotion created successfully.')
        return redirect(url_for('index'))
    return render_template('create_promotion.html', form=form)


@bp.route('/checkin', methods=['GET', 'POST'])
def checkin():
    if request.method == 'POST':
        booking_id = request.form.get('booking_id')
        room_id = request.form.get('room_id')

        # Fetch the booking from the database
        booking = Booking.query.filter_by(booking_id=booking_id, room_id=room_id).first()

        # Check if the booking exists and if the check-in date is today or in the past
        if booking and booking.check_in_date <= date.today():
            booking.status = "Checked In"
            db.session.commit()
            flash('Check-in successful.')
            return redirect(url_for('dashboard'))

        flash('Invalid booking details or check-in date is in the future.')

    return render_template('checkin.html')