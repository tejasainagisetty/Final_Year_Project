from flask import Flask, render_template, request,jsonify
from keras.models import load_model
import cv2
import numpy as np
import base64
from PIL import Image
import io
import re

img_size=224

app = Flask(__name__) 

model=load_model('C:\PROJECT-3.O\webapp\model\my_model.keras')

label_dict={0:'Covid19 Negative', 1:'Covid19 Positive'}

def preprocess(img):
    img = np.array(img)

    if img.ndim == 3:
        # If the image has 3 channels, assume it's already in the correct format
        resized = cv2.resize(img, (img_size, img_size))
    else:
        # If the image is grayscale, convert it to RGB
        img_rgb = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        resized = cv2.resize(img_rgb, (img_size, img_size))

    # Normalize pixel values
    resized = resized / 255.0

    # Add batch dimension
    reshaped = np.expand_dims(resized, axis=0)

    return reshaped


@app.route("/")
def index():
	return(render_template("index.html"))

@app.route("/predict", methods=["POST"])
def predict():
	print('HERE')
	message = request.get_json(force=True)
	encoded = message['image']
	decoded = base64.b64decode(encoded)
	dataBytesIO=io.BytesIO(decoded)
	dataBytesIO.seek(0)
	image = Image.open(dataBytesIO)

	test_image=preprocess(image)

	prediction = model.predict(test_image)
	result=np.argmax(prediction,axis=1)[0]
	accuracy=float(np.max(prediction,axis=1)[0])

	label=label_dict[result]

	print(prediction,result,accuracy)

	response = {'prediction': {'result': label,'accuracy': accuracy}}

	return jsonify(response)

app.run(debug=True)

#<img src="" id="img" crossorigin="anonymous" width="400" alt="Image preview...">