from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from .forms import RegistrationForm, LoginForm, ProfileForm, HousekeeperForm, EvaluationForm
from app import db
from .models import User, Housekeeper, Rating


main = Blueprint('main', __name__)

@main.route("/", methods=["GET"])
def home():
    search_query = request.args.get("search", "").strip()
    if search_query:
        # Filter housekeepers based on name, nationality, or working countries
        housekeepers = Housekeeper.query.filter(
            (Housekeeper.name.ilike(f"%{search_query}%")) |
            (Housekeeper.nationality.ilike(f"%{search_query}%")) |
            (Housekeeper.working_countries.ilike(f"%{search_query}%"))
        ).all()
    else:
        # If no search query, list all housekeepers
        housekeepers = Housekeeper.query.all()

    return render_template("home.html", housekeepers=housekeepers)

@main.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if the email already exists
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash("Email is already registered. Please use a different email.", "danger")
            return redirect(url_for("main.register"))

        # Create a new user
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,  # Ensure password is hashed
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            country=form.country.data,
            contact_email=form.contact_email.data,
            contact_number=form.contact_number.data
        )
        db.session.add(user)
        db.session.commit()
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("main.login"))
    return render_template("register.html", form=form)

from werkzeug.security import check_password_hash

'''@main.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("Logged in successfully!", "success")
            return redirect(url_for('main.home'))
        else: '''

'''@main.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):  # Use the `check_password` method
            login_user(user)
            flash("Logged in successfully!", "success")
            next_page = request.args.get('next')  # Redirect to the next page if available
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else: '''

@main.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):  # Use the `check_password` method
            login_user(user)
            flash("Logged in successfully!", "success")
            next_page = request.args.get('next')  # Redirect to the next page if available
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash("Login failed. Check your email and password.", "danger")
    return render_template("login.html", form=form)

'''''
@main.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    profile_form = ProfileForm()
    housekeeper_form = HousekeeperForm()

    if profile_form.validate_on_submit():
        current_user.username = profile_form.username.data
        current_user.email = profile_form.email.data
        current_user.first_name = profile_form.first_name.data
        current_user.last_name = profile_form.last_name.data
        current_user.country = profile_form.country.data
        current_user.contact_email = profile_form.contact_email.data
        current_user.contact_number = profile_form.contact_number.data
        if profile_form.password.data:
            current_user.set_password(profile_form.password.data)
        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for('main.profile'))

    if housekeeper_form.validate_on_submit():
        housekeeper = Housekeeper(
            name=housekeeper_form.name.data,
            passport_number=housekeeper_form.passport_number.data,
            nationality=housekeeper_form.nationality.data,
            working_countries=housekeeper_form.working_countries.data,
            note=housekeeper_form.note.data,
            user_id=current_user.id  # Associate the housekeeper with the logged-in user
        )
        db.session.add(housekeeper)
        db.session.commit()
        flash("Housekeeper added successfully!", "success")
        return redirect(url_for('main.profile'))

    profile_form.username.data = current_user.username
    profile_form.email.data = current_user.email
    profile_form.first_name.data = current_user.first_name
    profile_form.last_name.data = current_user.last_name
    profile_form.country.data = current_user.country
    profile_form.contact_email.data = current_user.contact_email
    profile_form.contact_number.data = current_user.contact_number

        # Fetch housekeepers created by the logged-in user
    user_housekeepers = current_user.housekeepers

    return render_template("profile.html", profile_form=profile_form, housekeeper_form=housekeeper_form, housekeepers=user_housekeepers)
'''

@main.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    profile_form = ProfileForm()
    housekeeper_form = HousekeeperForm()

    if profile_form.validate_on_submit():
        current_user.username = profile_form.username.data
        current_user.email = profile_form.email.data
        current_user.first_name = profile_form.first_name.data
        current_user.last_name = profile_form.last_name.data
        current_user.country = profile_form.country.data
        current_user.contact_email = profile_form.contact_email.data
        current_user.contact_number = profile_form.contact_number.data
        if profile_form.password.data:
            current_user.set_password(profile_form.password.data)
        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for('main.profile'))

    if housekeeper_form.validate_on_submit():
        # Check if the passport number already exists
        existing_housekeeper = Housekeeper.query.filter_by(passport_number=housekeeper_form.passport_number.data).first()
        if existing_housekeeper:
            flash("Passport number is already registered for another housekeeper. Please use a different passport number.", "danger")
            return redirect(url_for("main.profile"))

        # Create a new housekeeper
        housekeeper = Housekeeper(
            name=housekeeper_form.name.data,
            passport_number=housekeeper_form.passport_number.data,
            nationality=housekeeper_form.nationality.data,
            working_countries=housekeeper_form.working_countries.data,
            note=housekeeper_form.note.data,
            user_id=current_user.id
        )
        db.session.add(housekeeper)
        db.session.commit()
        flash("Housekeeper added successfully!", "success")
        return redirect(url_for("main.profile"))

    # Pre-fill the profile form with current user data
    profile_form.username.data = current_user.username
    profile_form.email.data = current_user.email
    profile_form.first_name.data = current_user.first_name
    profile_form.last_name.data = current_user.last_name
    profile_form.country.data = current_user.country
    profile_form.contact_email.data = current_user.contact_email
    profile_form.contact_number.data = current_user.contact_number

    # Fetch housekeepers created by the logged-in user
    user_housekeepers = current_user.housekeepers

    return render_template(
        "profile.html",
        profile_form=profile_form,
        housekeeper_form=housekeeper_form,
        housekeepers=user_housekeepers
    )


from flask_login import logout_user

@main.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('main.home'))
'''
@main.route("/housekeeper/<int:hk_id>", methods=["GET", "POST"])
@login_required
def housekeeper_detail(hk_id):
    housekeeper = Housekeeper.query.get_or_404(hk_id)
    form = RatingForm()

    if form.validate_on_submit():
        rating = Rating(
            score=form.score.data,
            comment=form.comment.data,
            user_id=current_user.id,
            housekeeper_id=hk_id
        )
        db.session.add(rating)
        db.session.commit()
        flash("Your rating has been submitted.", "success")
        return redirect(url_for('main.housekeeper_detail', hk_id=hk_id))

    ratings = housekeeper.ratings
    avg_rating = sum(rating.score for rating in ratings) / len(ratings) if ratings else None

    return render_template("housekeeper_detail.html", housekeeper=housekeeper, form=form, ratings=ratings, avg_rating=avg_rating)
'''

@main.route("/housekeeper/<int:hk_id>", methods=["GET", "POST"])
#@login_required
def housekeeper_detail(hk_id):
    housekeeper = Housekeeper.query.get_or_404(hk_id)
    form = EvaluationForm()

    if form.validate_on_submit():
        # Add the new rating to the database
        rating = Rating(
            cleaning=form.cleaning.data,
            timing=form.timing.data,
            cooking=form.cooking.data,
            childcare=form.childcare.data,
            respect=form.respect.data,
            user_id=current_user.id,
            housekeeper_id=hk_id
        )
        db.session.add(rating)
        db.session.commit()
        flash("Your evaluation has been submitted.", "success")
        return redirect(url_for('main.housekeeper_detail', hk_id=hk_id))

    # Fetch all ratings for the housekeeper
    ratings = housekeeper.ratings

    # Recalculate average ratings
    average_cleaning = sum([r.cleaning for r in ratings]) / len(ratings) if ratings else 0
    average_timing = sum([r.timing for r in ratings]) / len(ratings) if ratings else 0
    average_cooking = sum([r.cooking for r in ratings]) / len(ratings) if ratings else 0
    average_childcare = sum([r.childcare for r in ratings]) / len(ratings) if ratings else 0
    average_respect = sum([r.respect for r in ratings]) / len(ratings) if ratings else 0

    # Calculate overall percentage
    overall_percentage = (
        (average_cleaning + average_timing + average_cooking + average_childcare + average_respect) / 25
    ) * 100 if ratings else 0

    return render_template(
        "housekeeper_detail.html",
        housekeeper=housekeeper,
        form=form,
        ratings=ratings,
        average_cleaning=average_cleaning,
        average_timing=average_timing,
        average_cooking=average_cooking,
        average_childcare=average_childcare,
        average_respect=average_respect,
        overall_percentage=overall_percentage
    )