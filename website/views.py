from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from .models import User, Note, Review
from . import db
from datetime import datetime
import sqlite3
from sqlalchemy import desc
from sqlalchemy.sql import func
import random
import os

views = Blueprint('views', __name__)

@views.route('/')
def main():
    return render_template('main1.html', user=current_user)

@views.route('/signpage')
def signpage():
    authenticated = current_user.is_authenticated
    return render_template('entry.html', authenticated = authenticated, user = current_user)

@views.route('/profilepage', methods = ['GET', 'POST'])
@login_required
def profilepage():

    top_restaurants = (
        db.session.query(Review.restaurant_name)
        .filter(Review.rating >= 3)  # Рейтинг не менше 3
        .filter(Review.user_id == current_user.id)
        .group_by(Review.restaurant_name)  # Групувати за іменем ресторану
        .order_by(func.max(Review.rating).desc())  # Сортувати за максимальним рейтингом
        .limit(3)  # Обмежити результат до трьох ресторанів
        .all()
    )
    
    top_restaurants = [restaurant[0] for restaurant in top_restaurants]
    print(top_restaurants)
    restaurant_images = {}
    conn = sqlite3.connect('website/restaurants.db')
    cursor = conn.cursor()
    for restaurant_name in top_restaurants:
        cursor.execute("SELECT image_path FROM restaurants WHERE name = ?", (restaurant_name,))
        result = cursor.fetchone()  # Отримати перший рядок результату
        image_path = result[0]
        restaurant_images[restaurant_name] = image_path


    random_reviews = (
        db.session.query(Review)
        .filter_by(user_id=current_user.id)  # Фільтруємо за ідентифікатором поточного користувача
        .order_by(db.func.random())  # Рандомізуємо порядок записів
        .limit(3)  # Обмежуємо вибірку до трьох випадкових записів
        .all()
    )
    # random_reviews = [restaurant[0] for restaurant in random_reviews]
    restaurant_reviews={}
    for random_review in random_reviews:
        cursor.execute("SELECT image_path FROM restaurants WHERE name = ?", (random_review.restaurant_name,))
        result = cursor.fetchone()  # Отримати перший рядок результату
        image_path = result[0]
        restaurant_reviews[random_review] = image_path






    return render_template('profile.html', user = current_user, restaurant_images=restaurant_images, restaurant_reviews=restaurant_reviews)



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

@views.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            print("File received:", file.filename)
            folder_path = 'static/user_photos'
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                print("Folder created:", folder_path)
            filename = file.filename
            file_path = os.path.join(folder_path, filename)
            print("File path:", file_path)
            file.save(file_path)
            print("File saved successfully")
            current_user.image_file = '/static/user_photos/' + filename  # Update the user's image_file in the database
            db.session.commit()
            return redirect(url_for('views.profilepage'))  # Redirect to user's profile page
    return render_template('profile.html')

@views.route("/restpage/<restaurant_name>")
def restpage(restaurant_name):
    connection = sqlite3.connect('website/restaurants.db')
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
        views.rest = restaurant[0]
        restaurant_reviews = Review.query.filter_by(restaurant_name=views.rest).all()
        return render_template('rest.html', restaurant=restaurant, user = current_user, reviews=restaurant_reviews)
    else:
        return 'Restaurant not found', 404


@views.route("/submit_review", methods=['POST', 'GET'])
# @login_required
def submit_review():
    # connection = sqlite3.connect('website/restaurants.db')
    # cursor = connection.cursor()
    # cursor.execute("SELECT name, address, rating, tel, time, price, image_path, link FROM restaurants WHERE name=?", (views.rest,))
    # restaurant = cursor.fetchone()
    # connection.close()
    rating = request.form['rating']
    feedback = request.form['feedback']
    if 'rating' in request.form and 'feedback' in request.form:
        rating = request.form['rating']
        feedback = request.form['feedback']
        print(rating)
        print(feedback)
        review = Review(feedback=feedback, rating=rating, restaurant_name=views.rest, user_id = current_user.id, user_name = current_user.name, image_file = current_user.image_file)
        db.session.add(review)
        db.session.commit()
        # return redirect(url_for('views.restpage', restaurant_name=views.rest, user= current_user))
        return 'Success'
        # return render_template('rest.html', user=current_user)
        # return redirect(url_for('rest', user=current_user))
        # flash('Your review successfully added!', category='success')
        # return redirect(url_for('views.restpage', restaurant_name=views.rest))
    else:
        flash('Anonymous user', category='error')
        return 'Invalid request parameters', 400
    
# @views.route("/reviews")
# def reviews():
    # Отримання відгуків з бази даних
    # print(views.rest)
    # restaurant_reviews = Review.query.filter_by(restaurant_name=views.rest).all()
    # return render_template('reviews.html', reviews=restaurant_reviews)
