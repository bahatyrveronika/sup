from flask import Blueprint, render_template, request, flash
from flask_login import current_user, login_required
from .models import User, Note, Review
from . import db
from datetime import datetime
import sqlite3

views = Blueprint('views', __name__)

@views.route('/')
def main():
    # authenticated = current_user.is_authenticated
    return render_template('main1.html', user=current_user)

@views.route('/signpage')
def signpage():
    authenticated = current_user.is_authenticated
    return render_template('entry.html', authenticated = authenticated, user = current_user)

@views.route('/profilepage', methods = ['GET', 'POST'])
@login_required
def profilepage():
    # authenticated = current_user.is_authenticated
    # user = User.query.filter_by(id=current_user.id).first()
    # if request.method =='POST':
    #     note = request.form.get('review')
    #     if len(note)<1:
    #         flash('Note is too short', category='error')
    #     else:
    #         new_note = Note(data=note, user_id=user.id, date=datetime.now())
    #         print(new_note)
    #         db.session.add(new_note)
    #         db.session.commit()
    #         flash('Note added', category='success')
    return render_template('profile.html', user = current_user)


@views.route("/notebutton", methods = ['GET', 'POST'])
def notebutton():
    authenticated = current_user.is_authenticated
    user = User.query.filter_by(id=current_user.id).first()
    if request.method =='POST':
        note = request.form.get('review')
        if len(note)<1:
            flash('Note is too short', category='error')
        else:
            new_note = Note(data=note, user_id=user.id, date=datetime.now())
            print(new_note)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added', category='success')
    return render_template('profile.html', authenticated = authenticated, user = current_user)

@views.route("/restpage/<restaurant_name>")
def restpage(restaurant_name):
    connection = sqlite3.connect('/Users/veronikabagatyr-zaharcenko/Desktop/Flask web app tutoriall/website/restaurants.db')
    cursor = connection.cursor()
    cursor.execute("SELECT name, address, rating, tel, time, price, image_path, link FROM restaurants WHERE name=?", (restaurant_name,))
    restaurant = cursor.fetchone()
    connection.close()
    if restaurant:
        # print("Name:", restaurant[0])
        # print("Address:", restaurant[1])
        # print("Rating:", restaurant[2])
        # print("Tel:", restaurant[3])
        # print("Time:", restaurant[4])
        # print("Price:", restaurant[5])
        # print("Image Path:", restaurant[6])
        # print("Link:", restaurant[7])
        return render_template('rest.html', restaurant=restaurant, user = current_user)
    else:
        return 'Restaurant not found', 404
    
@views.route("/submit_review/<restaurant_name>", methods=['POST', 'GET'])
@login_required
def submit_review(restaurant_name):
    # rating = request.form['rating']
    # feedback = request.form['feedback']
    # print(rating)
    # print(feedback)
    if 'rating' in request.form and 'feedback' in request.form:
        rating = request.form['rating']
        feedback = request.form['feedback']
        review = Review(feedback=feedback, rating=rating, restaurant_name=restaurant_name, user_id = current_user.id)
        db.session.add(review)
        db.session.commit()
        return 'Review submitted successfully!'
    else:
        return 'Invalid request parameters', 400
