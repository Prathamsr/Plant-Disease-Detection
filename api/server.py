from fastapi import FastAPI, File, UploadFile ,Form
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf
import pymongo
import sys

try:
    client = pymongo.MongoClient(
        "mongodb+srv://pratham:<password>@diseasedetect.tgp72fs.mongodb.net/?retryWrites=true&w=majority")
    print("connected")
except pymongo.errors.ConfigurationError:
    print("An Invalid URI host error was received. Is your Atlas host name correct in your connection string?")
    sys.exit(1)

db = client.myDatabase
my_collection = db["diseases"]
my_solutions = db["solutions"]

def get_solution(disease):
    my_doc = my_solutions.find_one({"disease":disease})
    return my_doc
def get_Classes(plant):
    my_doc = my_collection.find_one({"name": plant})
    return my_doc
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CLASS_NAMES = ["Early Blight", "Late Blight", "Healthy"]

@app.get("/ping")
async def ping():
    return "Hello, I am alive"

def read_file_as_image(data) -> np.ndarray:
    image = np.array(Image.open(BytesIO(data)))
    return image

@app.post("/predict")
async def predict(
    file: UploadFile = File(...),
    plant: str =Form(...),
):
    image = read_file_as_image(await file.read())
    img_batch = np.expand_dims(image, 0)
    MODEL = tf.keras.models.load_model(f"./models/{plant}")
    
    predictions = MODEL.predict(img_batch)
    classes=get_Classes(plant)
    predicted_class = classes["disease"][np.argmax(predictions[0])]
    confidence = np.max(predictions[0])
    data=get_solution(predicted_class)
    return {
        'class': predicted_class,
        'confidence': float(confidence),
        'plant':plant,
        'solutin':data['solution']
    }

if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8000)