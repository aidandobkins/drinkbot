from flask import Flask, render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
import wtforms
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, InputRequired, AnyOf
import time
from time import sleep
import sys
import RPi.GPIO as GPIO
import json
import threading
import traceback
import logincreds
from makeDrink import *

app = Flask(__name__)
app.config['SECRET_KEY'] = ''

MAKINGDRINK = False
CUP_SIZE = 7
labels = ['Drink 1', 'Drink 2', 'Drink 3', 'Drink 4', 'Drink 5', 'Drink 6']

class DrinkForm(FlaskForm):
    drink1 = IntegerField()
    drink2 = IntegerField()
    drink3 = IntegerField()
    drink4 = IntegerField()
    drink5 = IntegerField()
    drink6 = IntegerField()
    submit = SubmitField('Make Drink')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        #if labels is None:
        #    labels = ['Drink 1', 'Drink 2', 'Drink 3', 'Drink 4', 'Drink 5', 'Drink 6']
        self['drink1'].label = wtforms.Label(self['drink1'].id, labels[0])
        self['drink2'].label = wtforms.Label(self['drink2'].id, labels[1])
        self['drink3'].label = wtforms.Label(self['drink3'].id, labels[2])
        self['drink4'].label = wtforms.Label(self['drink4'].id, labels[3])
        self['drink5'].label = wtforms.Label(self['drink5'].id, labels[4])
        self['drink6'].label = wtforms.Label(self['drink6'].id, labels[5])

class SettingsForm(FlaskForm):
    drink1 = StringField('PUMP 1', validators=[InputRequired()])
    drink2 = StringField('PUMP 2', validators=[InputRequired()])
    drink3 = StringField('PUMP 3', validators=[InputRequired()])
    drink4 = StringField('PUMP 4', validators=[InputRequired()])
    drink5 = StringField('PUMP 5', validators=[InputRequired()])
    drink6 = StringField('PUMP 6', validators=[InputRequired()])
    submit = SubmitField('Change Labels')

class loginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = StringField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')

@app.route('/', methods=['GET', 'POST'])
def home():
    global MAKINGDRINK
    form = DrinkForm()
    if form.validate_on_submit():
        mix = [form.drink1.data, form.drink2.data, form.drink3.data, form.drink4.data, form.drink5.data, form.drink6.data]

        sum = 0
        for i in range(6):
            sum = sum + mix[i]
            
        
        if sum > CUP_SIZE:
            flash('Error - Total Shots exceeds the maximum cup size of ' + str(CUP_SIZE) + ' shots.', 'danger')
        elif MAKINGDRINK == True:
            flash('Error - Someone is already making a drink! Please wait...', 'danger')
        else:
            MAKINGDRINK = True
            queueDrink(mix)
            MAKINGDRINK = False
            flash("Drink finished... Enjoy!", 'success')

        return redirect(url_for('home'))

    return render_template('landingPage.html', title='MakeDrinks', form=form)

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    form1 = SettingsForm()
    if form1.validate_on_submit():
        changes = [form1.drink1.data, form1.drink2.data, form1.drink3.data, form1.drink4.data, form1.drink5.data, form1.drink6.data]
        global labels
        labels = changes
        flash('Labels changed', 'success')

    return render_template('settingsPage.html', title='Settings', form=form1)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form2 = loginForm()
    namecheck = False
    passcheck = False
    if form2.validate_on_submit():
        if form2.username.data in logincreds.usernames:
            namecheck = True
        if form2.password.data in logincreds.passwords:
            passcheck = True
        if passcheck == True and namecheck == True:
            return redirect(url_for('settings'))
        else:
            flash("Incorrect credentials, please try again\n")

    return render_template('loginPage.html', title='Login', form=form2)

@app.route('/purge', methods=['GET', 'POST'])
def purge():
    purgePumps()
    flash('Pumps cleared', 'success')
    return redirect(url_for('settings'))

@app.route('/clear', methods=['GET', 'POST'])
def clear():
    clearStored()
    flash('Drinks cleared', 'success')
    return redirect(url_for('settings'))

@app.route('/recent') 
def recent(): 
	with open('drinklog.dat', 'r') as f: 
		return render_template('recentPage.html', text=f.read()) 

if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')

GPIO.cleanup()