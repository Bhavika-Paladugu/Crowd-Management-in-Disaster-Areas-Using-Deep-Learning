import json
from flask import Flask, render_template, request, Response, jsonify, send_file, url_for, send_from_directory, redirect
from roboflow import Roboflow
import supervision as sv
import os
import sys
from PIL import Image
import cv2
import base64
from io import BytesIO
from werkzeug.utils import secure_filename

person_detection_path = r'C:\Users\Hp\Downloads\UI UX\ml_model\injury_classification'
sys.path.append(person_detection_path)
from person_detection_image import process_frame

from flask_cors import CORS

app = Flask(__name__)
CORS(app)


UPLOAD_FOLDER = r'C:\\Users\\Hp\\Downloads\\UI UX\\static\\data'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

count = 0

@app.route('/imageapi', methods=['POST'])
def process_image():
    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        upload_folder = 'static/data'
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        
        file_path = os.path.join(upload_folder, file.filename)
        file.save(file_path)

        processed_image_path, count = process_uploaded_image(file_path)
        print('processed image from process_image function()', processed_image_path)
        print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
        print('count from image_api API: ', count)
        original_link = '<a href="' + url_for('original_html') + '">Original HTML</a>'
        processed_link = '<a href="' + url_for('processed_html') + '">Processed HTML</a>'
        
        # Concatenate links
        links = original_link + '<br>' + processed_link

    return links
    # return send_file(processed_image_path, mimetype='image/jpeg')   
    # return "file uploaded successfully"
        # Return the file path of the uploaded image
    #return jsonify({'message': 'File uploaded successfully', 'file_path': file_path}), 200

@app.route('/original')
def original_html():
    # Your logic to render original.html
    filename='uploaded_image.jpg'
    return render_template('original.html',  filename=filename)

@app.route('/processed')
def processed_html():
    # Your logic to render processed.html
    return render_template('processed.html')

def process_uploaded_image(file_path):    
    global count
    # Process the image using Roboflow or other methods
    rf = Roboflow(api_key="jNOBuOEl1QrhUQpP8jvj")#jNOBuOEl1QrhUQpP8jvj
    project = rf.workspace().project("flir-data-set")
    model = project.version(22).model
    result = model.predict(file_path)
    # detections = sv.Detections.from_roboflow(result)
    # print('Detections: ', detections)
    # print('length of detections is: ', len(detections))
    # print('printing result: ', result)
    count = 0
    for detection in result:
        detection_class = detection["class"]
        count+=1
        # print("Detection class:", detection_class)
    # print('printing result of class : ', result["class"])
    print('count is: ', count)

    result.save("static/data/processed_image.jpg")  # Adjust the path as needed    
        # Open the processed image
    processed_image = Image.open("static/data/processed_image.jpg")
    print('Image: ', processed_image)
        
        # Convert the processed image to base64 string 
        #with open("static/data/processed_image.jpg", 'rb') as f:
            #processed_image_bytes = f.read()
            #processed_image_b64 = base64.b64encode(processed_image_bytes).decode('utf-8')
        
        # Create a response containing the base64-encoded processed image
        #return Response(processed_image_b64, mimetype='text/plain')
    return "static/data/processed_image.jpg", count
    #return send_file(processed_image, mimetype='image/jpeg')


@app.route('/process_image', methods=['POST'])
def process_image_route():
    # Get the uploaded file
    uploaded_file = request.files['file']
    # Save the file to the static directory
    image_path = os.path.join("static", "data", uploaded_file.filename)
    uploaded_file.save(image_path)
    # Process the image
    processed_detections = process_image(image_path)
    # Save the processed image
    processed_image_path = os.path.join("static", "processed_images", "processed_" + uploaded_file.filename)
    # An example of saving the processed image, you need to implement it according to your requirement
    # Example: cv2.imwrite(processed_image_path, processed_detections)
    # Return the path to the processed image
    return processed_image_path


@app.route('/resources_render')
# Function to perform resource allocation
def resource_allocation():
    # Define the quantities for each item
    global count
    quantities = { 
        'non_food_items': {
            'Clothing/Bedding': count,
            'Mattresses/Mats': count,
            'Bathing Soap': count,
            'Laundry Soap': count,
            'Toothbrush': count,
            'Toothpaste': count,
            'Shampoo': count
        },
        'food_items': {
            'Clean Drinking Water (in litres)': 2.7 * count,
            'Cereals (Wheat, Rice, Maize in grams)': 420 * count,
            'Legumes (Beans, Lentils in grams)': 50 * count,
            'Meat/Fish (in grams)': 20 * count,
            'Cooking Oil (in grams)': 25 * count,
            'Sugar (in grams)': 20 * count,
            'Salt (in grams)': 5 * count,
            'High-Energy Biscuits (in grams)': 125 * count,
            'Milk Powder (in grams)': 10 * count
        }
    }
    return quantities


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/processed_image')
def processed_image():
    # Replace 'C:\\Users\\Hp\\Downloads\\UI UX\\static\\data' with the actual path to your folder
    folder_path = 'C:\\Users\\Hp\\Downloads\\UI UX\\static\\data'
    return send_from_directory(folder_path, 'processed_image.jpg')



'''@app.route('/stats', methods=[ 'GET',  'POST'])
def stats():
     if request.method == 'POST':
        f = request.files['file']
        
        # Get the filename and save it to the specified upload folder
        filename = secure_filename(f.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        f.save(image_path)

        annotated_image_path = process_image(image_path)
        print('in the loop')

        # Now, 'file_path' contains the full path where the file is saved
        return 'File uploaded successfully. Path: {}'.format(image_path)
     print('hehe')
     return render_template('uploader.html')'''






    # if request.method == 'POST':
    #     # Get the uploaded file
    #     uploaded_file = request.files['file']
    #     # Save the file to the static directory
    #     image_path = os.path.join('static', 'images', uploaded_file.filename)
    #     uploaded_file.save(image_path)
    #     # Process the image and get the path to the annotated image and the count
    #     annotated_image_path = process_image(image_path)
    #     print("I owe harshil a chocolate")
    #     # Render the stats template and pass the paths to the original and annotated images, and the count
    #     return render_template('stats.html',  annotated_image_path=annotated_image_path)
    # print("I owe harshil 2 chocolate")
    # return render_template( 'stats.html')


@app.route('/uploader', methods=['GET', 'POST'])
def uploader():
    return render_template('uploader.html')

@app.route('/stats')
def stats():
   return redirect("http://localhost:3000/")

@app.route('/help')
def help():
    return redirect("http://localhost:3001/")

@app.route('/hehe')
def hehe():
    global count
    return jsonify({'count': count})


'''@app.route('/upload')
def upload():
   
   return render_template('uploader.html')'''



global injury_label


@app.route('/injured')
def injured():
    global injury_label
    file_path = r'C:\Users\Hp\Downloads\UI UX\ml_model\injury_classification\IMAGES\render_images\render_image.jpeg'

    # Read the image using OpenCV
    image = cv2.imread(file_path)

    if image is None:
        return "Failed to read image", 400  # Return error message with status code 400

    # Process the image using the process_frame function
    processed_image, injury_label_1 = process_frame(image)
    injury_label = injury_label_1

    # Debugging: Print injury label and other information
    print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
    print("Injury Label:", injury_label)
    # You can print other information here for debugging purposes

    # Convert the processed image (numpy array) to bytes
    _, img_encoded = cv2.imencode('.jpg', processed_image)
    img_bytes = img_encoded.tobytes()

    # Return the processed image bytes as a response
    return send_file(BytesIO(img_bytes), mimetype='image/jpeg')

@app.route('/injured_image', methods=['POST'])
def injured_image():
    if 'file' not in request.files:
        return "No file part", 400
    
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    
    # Save the uploaded file to a temporary location
    temp_path = 'temp.jpg'
    file.save(temp_path)

    # Read the uploaded image using OpenCV
    image = cv2.imread(temp_path)
    os.remove(temp_path)  # Remove temporary file

    if image is None:
        return "Failed to read image", 400

    # Process the image using the process_frame function (imported from person_detection_image)
    processed_image, injury_label = process_frame(image)

    # Save the processed image to the desired path
    save_path = r'C:\Users\Hp\Downloads\UI UX\ml_model\injury_classification\IMAGES\render_images\render_image.jpeg'
    cv2.imwrite(save_path, processed_image)

    # Return the path to the saved image as a response
    return jsonify({"saved_image_path": save_path}), 200



@app.route('/label')
def label():
    global injury_label
    return injury_label




if __name__ =='__main__': # just a minute
    app.run(port=3002, debug=True)
