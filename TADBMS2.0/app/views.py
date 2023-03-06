import os, psycopg2
from flask import render_template, request, redirect, url_for, flash, session
from app import app, db
from app.storebooking import HotelBooking
from .forms import BookingForm, DeleteBooking

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/addbooking', methods=['GET','POST'])
def bookings():

    formObj = BookingForm()
    if formObj.is_submitted():
        res = request.form
        conn = psycopg2.connect(
            host="localhost",
            database="Bookings",
            user="postgres",
            password="INSERTPASSWORDHERE"
        )
        cur = conn.cursor()

        booking_data = {
            'hotel_name': res['hotel_name'],
            'check_in_date': res['check_in_date'],
            'check_out_date': res['check_out_date'],
            'num_guests': res['num_guests'],
            'cust_fname': res['cust_fname'],
            'cust_lname': res['cust_lname']
        }

        cur.execute("""
            INSERT INTO hotel_bookings (hotel_name, check_in_date, check_out_date, num_guests, cust_fname, cust_lname)
            VALUES (%(hotel_name)s, %(check_in_date)s, %(check_out_date)s, %(num_guests)s, %(cust_fname)s, %(cust_lname)s);
        """, booking_data)

        conn.commit()

        cur.close()
        conn.close()

        return redirect(url_for('home'))

    return render_template('storebooking.html', form=formObj)

@app.route('/bookings', methods=['GET','POST'])
def update():
    resMain = HotelBooking.query.all()
    BookingformObj = BookingForm()

    if BookingformObj.is_submitted():
        res = request.form
        # print(res['changeID'])

        conn = psycopg2.connect(
            host="localhost",
            database="Bookings",
            user="postgres",
            password="INSERTPASSWORDHERE"
        )
        cur = conn.cursor()

        booking_data = {
            'hotel_name': res['hotel_name'],
            'check_in_date': res['check_in_date'],
            'check_out_date': res['check_out_date'],
            'num_guests': res['num_guests'],
            'cust_fname': res['cust_fname'],
            'cust_lname': res['cust_lname'],
            'changeID' : res['changeID']
        }

        cur.execute("""
            UPDATE hotel_bookings
            SET
            hotel_name = %(hotel_name)s,
            check_in_date = %(check_in_date)s,
            check_out_date = %(check_out_date)s,
            num_guests = %(num_guests)s,
            cust_fname = %(cust_fname)s,
            cust_lname = %(cust_lname)s
            WHERE bookingid = %(changeID)s;
        """, booking_data)

        conn.commit()

        cur.close()
        conn.close()

        return redirect(url_for('update'))

    return render_template('updatebookings.html', data=resMain, form=BookingformObj)

@app.route('/delete', methods=['GET','POST'])
def delete():
    resMain = HotelBooking.query.all()
    DelformObj = DeleteBooking()
    print("#EASY MONEY#")

    if DelformObj.is_submitted():
        res = request.form

        conn = psycopg2.connect(
            host="localhost",
            database="Bookings",
            user="postgres",
            password="INSERTPASSWORDHERE"
        )
        cur = conn.cursor()

        cur.execute("""DELETE FROM hotel_bookings WHERE bookingid = %(deleteID)s""", res)

        conn.commit()

        cur.close()
        conn.close()

        return redirect(url_for('update'))

    return render_template('deleteform.html', data=resMain, delform=DelformObj)
