from datetime import date
from flask import Blueprint, request, jsonify, session
from werkzeug.security import check_password_hash, generate_password_hash
from App.Models.models import User, Room, Booking, Promotion
from App.forms import BookingForm, PromotionForm
from App.config import db

bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET'])
def home():
    return 'Hello, World!'

@bp.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password_hash, password):
        return jsonify({'message': 'Logged in successfully.'}), 200

    return jsonify({'message': 'Invalid username or password.'}), 401

@bp.route('/rooms', methods=['GET'])
def get_rooms():
    rooms = Room.query.all()
    return jsonify([room.serialize() for room in rooms])



@bp.route('/book', methods=['POST'])
def book():
    form = BookingForm()

    # Populate room_type choices
    form.room_type.choices = [(room.room_type, room.room_type) for room in Room.query.with_entities(Room.room_type).distinct()]

    if form.validate_on_submit():
        room_type = form.room_type.data
        room = Room.query.filter_by(room_type=room_type).first()

        if room:
            booking = Booking(
                user_id=session['user_id'],
                room_id=room.room_id,
                check_in_date=form.check_in_date.data,
                check_out_date=form.check_out_date.data,
                special_requests=form.special_requests.data
            )
            db.session.add(booking)
            db.session.commit()

            return jsonify({'message': 'Booking successful.'}), 200
        else:
            return jsonify({'message': 'Invalid room type.'}), 400

    return jsonify({'message': 'Invalid form data.'}), 400



@bp.route('/promotions/create', methods=['POST'])
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
        return jsonify({'message': 'Promotion created successfully.'}), 200

    return jsonify({'message': 'Invalid form data.'}), 400

@bp.route('/checkin', methods=['POST'])
def checkin():
    booking_id = request.form.get('booking_id')
    room_id = request.form.get('room_id')

    booking = Booking.query.filter_by(booking_id=booking_id, room_id=room_id).first()

    if booking and booking.check_in_date <= date.today():
        booking.status = "Checked In"
        db.session.commit()
        return jsonify({'message': 'Check-in successful.'}), 200

    return jsonify({'message': 'Invalid booking details or check-in date is in the future.'}), 400


@bp.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        first_name = request.form['first_name']
        last_name = request.form['last_name']

        # Check if the username or email already exists in the database
        existing_user = User.query.filter_by(username=username).first()
        existing_email = User.query.filter_by(email=email).first()

        if existing_user:
            return 'Username already exists. Please choose a different username.', 409

        if existing_email:
            return 'Email address already exists. Please use a different email.', 409

        # Create a new user object
        new_user = User(
            username=username,
            password_hash=generate_password_hash(password),
            email=email,
            first_name=first_name,
            last_name=last_name
        )

        # Add the user to the database
        db.session.add(new_user)
        db.session.commit()

        return 'Registration successful.', 201

    return 'Invalid request.', 400

