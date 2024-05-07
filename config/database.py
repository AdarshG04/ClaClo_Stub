from pymongo import MongoClient
#from pymongo.server_api import ServerApi
from gridfs import GridFS

client = MongoClient("mongodb+srv://19237466:Test123@cwstudent.phzlgn2.mongodb.net/?retryWrites=true&w=majority&appName=CWStudent")

db = client.student_db

teacher_collection = db["teacher_collection"]
collection_name = db["student_collection"]
assessment_collection = db["assessment_collection"]
learning_material_collection = db["learning_material_collection"]
feedback_collection = db["feedback_collection"]