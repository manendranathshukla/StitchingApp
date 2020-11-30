from flask import Flask, render_template
import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from flask import send_file
from imutils import paths
import numpy as np
import argparse
import imutils
import cv2
import glob





app = Flask(__name__)

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'static/uploaded_images/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['jpg'])

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# This route will show a form to perform an AJAX request
# jQuery is loaded to execute the request and update the
# value of the operation
@app.route('/')
def index():
    return render_template('index.html')


# Route that will process the file upload
@app.route('/', methods=['POST'])
def upload():
    # Get the name of the uploaded files
    uploaded_files = request.files.getlist("file[]")
    filenames = []
    for file in uploaded_files:
        # Check if the file is one of the allowed types/extensions
        if file and allowed_file(file.filename):
            # Make the filename safe, remove unsupported chars
            filename = secure_filename(file.filename)
            # Move the file form the temporal folder to the upload
            # folder we setup
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # Save the filename into a list, we'll use it later
            filenames.append(filename)
            # Redirect the user to the uploaded_file route, which
            # will basicaly show on the browser the uploaded file
    # Load an html page with a link to each uploaded file
    
    #print("[INFO] loading images...")
    imagePaths = glob.glob("static/uploaded_images/*.jpg")
    #print(imagePaths)
    images = []
    # loop over the image paths, load each one, and add them to our
# images to stich list
    for imagePath in imagePaths:
        image = cv2.imread(imagePath)
        images.append(image)

# initialize OpenCV's image sticher object and then perform the image
# stitching
    #print("[INFO] stitching images...")
    stitcher = cv2.createStitcher() if imutils.is_cv3() else cv2.Stitcher_create()
    (status, stitched) = stitcher.stitch(images)
    # if the status is '0', then OpenCV successfully performed image
# stitching
    if status == 0:
	# write the output stitched image to disk
        outputfile='output/shukla_output.png'
        cv2.imwrite('static/'+outputfile, stitched)
        cv2.waitKey(0)

    else:
        print("[INFO] image stitching failed ({})".format(status))


    return render_template('index.html', filename=outputfile)

# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
@app.route('/display/<filename>')
def display_image(filename):
	#print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='output/' + filename), code=301)
		
		
		
@app.route('/download/')
def return_files_tut():
	try:
		return send_file('static/output/shukla_output.png',attachment_filename='shukla_output.png')
	except Exception as e:
		return str(e)


# if __name__ == "__main__":
#     app.run(debug=True)
