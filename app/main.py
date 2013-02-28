# do not change or move the following lines if you still want to use the box.py auto generator
from app import app, db
from models import Contact

# you can freely change the lines below
from flask import render_template
from flask import json
from flask import session
from flask import url_for
from flask import redirect
from flask import request
from flask import abort
from flask import Response
import logging
from helpers import generate_key
# define global variables here

# home root controller
# @app.route('/')
# def index():
# 	# define your controller here
# 	return render_template('welcome.html')

@app.route('/') #Link
def home_control():
	# add your controller here
	return render_template('home.html')


@app.route('/about/') #Link
def about_control():
	# add your controller here
	return render_template('about.html')


########### contact data model controllers area ###########

@app.route('/data/contact/')
def data_contact():
	# this is the controller for JSON data access
	contact_list = Contact.query.all()

	if contact_list:
		json_result = json.dumps([contact.dto() for contact in contact_list])
	else:
		json_result = None

	return json_result

@app.route('/contact/view-all')
def contact_view_controller():
	#this is the controller to view all data in the model
	contact_list = Contact.query.all()

	if contact_list:
		contact_entries = [contact.dto() for contact in contact_list]
	else:
		contact_entries = None

	return render_template('contact.html',contact_entries = contact_entries, title = "Contact List")

def get_single_contact(contact_id):
	contact = None
	single_contact = Contact.query.filter(Contact.contact_id == contact_id).first()
	if single_contact:
		contact = single_contact.dto()
	result = contact
	return result

@app.route('/contact/<contact_id>.json')
def get_single_contact_json(contact_id):
	#this is the controller to get single entry in json format
	result = json.dumps(dict(contact=get_single_contact(contact_id)))
	return result

@app.route('/contact/<contact_id>')
def view_single_contact(contact_id):
	#this is the controller to get single entry view
	contact = get_single_contact(contact_id)
	return render_template('contact_view.html', contact = contact)

@app.route('/contact/')
def contact_add_controller():
	#this is the controller to add new model entries
	return render_template('contact_add.html', title = "Add New Entry")

@app.route('/contact/create/',methods=['POST','GET'])
def contact_create_data_controller():
	# this is the contact data create handler
	contact_name = request.values.get('contact_name')
	contact_email = request.values.get('contact_email')
	message = request.values.get('message')

	new_contact = Contact(
									contact_id = generate_key(),
									contact_name = contact_name,
									contact_email = contact_email,
									message = message
								)

	db.session.add(new_contact)
	db.session.commit()

	return 'Contact message sent <a href="/">back to home</a>'

@app.route('/contact/edit/<id>')
def contact_edit_controller(id):
	#this is the controller to edit model entries
	contact_item = Contact.query.filter(Contact.contact_id == id).first()
	return render_template('contact_edit.html', contact_item = contact_item, title = "Edit Entries")

@app.route('/contact/update/<id>',methods=['POST','GET'])
def contact_update_data_controller(id):
	# this is the contact data update handler
	contact_name = request.values.get('contact_name')
	contact_email = request.values.get('contact_email')
	message = request.values.get('message')
	contact_item = Contact.query.filter(Contact.contact_id == id).first()
	contact_item.contact_name = contact_name
	contact_item.contact_email = contact_email
	contact_item.message = message

	db.session.add(contact_item)
	db.session.commit()

	return 'data update successful <a href="/contact/">back to Entries</a>'

@app.route('/contact/delete/<id>')
def contact_delete_controller(id):
	#this is the controller to delete model entries
	contact_item = Contact.query.filter(Contact.contact_id == id).first()

	db.session.delete(contact_item)
	db.session.commit()

	return 'data deletion successful <a href="/contact/">back to Entries</a>'

