from flask import Flask, request
from flask_cors import CORS
from pydantic import BaseModel
import tensorflow as tf
import numpy as np
import cv2
import os


class ImageItem(BaseModel):
    image: str


__name__ = "api"

app = Flask(__name__)
cors = CORS(app)
app.config["DEBUG"] = True


@app.route("/api/predict", methods=["POST"])
def predict():
    print(request.files)
    prediction_model = tf.keras.models.load_model(os.path.join('models', 'dog_or_cat_classifier_model.h5'))
    image = request.files["image"]
    image.save(os.path.join('uploads', image.filename))
    img = cv2.imread(os.path.join('uploads', image.filename))
    resized_img = tf.image.resize(img, (256, 256))
    yhat = prediction_model.predict(np.expand_dims(resized_img / 255, 0))
    if yhat[0][0] > 0.5:
        return {"prediction": "dog"}
    else:
        return {"prediction": "cat"}


app.run(debug=True)
