"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file contains the routes for your application.
"""

import os
from app import app, db
from flask import render_template, request, redirect, url_for, flash, session, abort, send_from_directory
from app.forms import PropertyForm
from werkzeug.utils import secure_filename
from app.models import Properties##THIS##


#from app.models import UserProfile##THIS##



###
# Routing for your application.
###
lst=[]
def get_uploaded_images():
    rootdir = os.getcwd()#Gets current working dir
    #print(rootdir)
    for subdir, dirs, files in os.walk(rootdir + '/uploads'):
        for file in files:
            #name=os.path.join(subdir, file)
            name=os.path.join(file)
            lst.append(name)
            #print(os.path.join(subdir, file))

@app.route('/uploads/<filename>')
def get_image(filename):
    return(send_from_directory(os.path.join(os.getcwd(),app.config['UPLOAD_FOLDER']), filename))

@app.route('/properties/create',methods=['GET', 'POST'])
def new_property():
    form=PropertyForm()
    """Render website's new property page."""
    if request.method == 'POST':
        photo=form.photo.data
        if form.validate_on_submit():
            photo=form.photo.data
            filename=secure_filename(photo.filename)
            photo.save(os.path.join( app.config['UPLOAD_FOLDER'], filename ))
            new_property=Properties(
                title=form.title.data,
                bedrooms=form.bedrooms.data,
                bathrooms=form.bathrooms.data,
                location=form.location.data,
                price=form.price.data,
                type=form.type.data,
                description=form.description.data,
                filename=secure_filename(photo.filename)
            )
            db.session.add(new_property)
            db.session.commit()

            flash("Property Added Successfully!")
            return redirect(url_for('property'))
    return render_template('new_property.html', form=form)

@app.route('/properties')
def property():
    """Render website's property page."""
    return render_template('property.html')

@app.route('/properties/<propertyid>')
def get_property():
    #NOT SURE YET
    return render_template('.html')

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")


###
# The functions below should be applicable to all Flask apps.
###

# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404
