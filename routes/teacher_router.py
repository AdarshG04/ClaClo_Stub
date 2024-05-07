from fastapi import APIRouter, UploadFile, File, HTTPException, Response, Depends
from config.database import db
from gridfs import GridFS
from bson import ObjectId
from models.feedback_model import Feedback
from config.database import learning_material_collection
from config.database import assessment_collection
from config.database import feedback_collection
from schema.teacher_schema import list_serial
from fastapi.security import OAuth2PasswordBearer
import mimetypes


fs = GridFS(db)

assignmentRouter = APIRouter()


# Upload Learning Material for Student

@assignmentRouter.post("/uploadLearningMaterial/",  tags=["Learning Material"])
async def uploadLearningMaterial(student_Id: str,
    class_Id: str,
    materialName: str, materialFile: UploadFile = File(...)):
    file_id = fs.put(materialFile.file, filename=materialFile.filename)
    
    # Save metadata to MongoDB
    dataToSave = {
        "class_id": class_Id,
        "materialName": materialName,
        "file_id": str(file_id),
        "studentId": student_Id
    }
    
    # Insert metadata into study_materials collection
    learning_material_collection.insert_one(dataToSave)
    
    return {"message": "Learning Material uploaded successfully"}



# Assessment Download from Student 

@assignmentRouter.get("/download/StudentAssessment",  tags=["Student Assessment"])
async def downloadStudentAssessment(assessment_id: str):
    try:
        student_assessment = db.assessment_collection.find_one({"file_id": assessment_id})
        if student_assessment is None:
            raise HTTPException(status_code=404, detail="Student Assessment not found for this class")

        # Retrieve file from GridFS using the file ID stored in the study material
        file_info = fs.get(ObjectId(student_assessment["file_id"]))
        if file_info is None:
            raise HTTPException(status_code=404, detail="File not found")

        # Determine media type based on file extension
        filename = file_info.filename
        media_type, _ = mimetypes.guess_type(filename)
        if media_type is None:
            media_type = "application/octet-stream"

        # Read file content into memory
        file_content = file_info.read()

        # Return file content as response
        return Response(content=file_content, media_type=media_type, headers={"Content-Disposition": f"attachment; filename={filename}"})
    except HTTPException:
        # Re-raise HTTPException to return specific error responses
        raise
    except Exception as e:
        # Handle any other exceptions
        raise HTTPException(status_code=500, detail="Failed to Download Student Assessment")
    

# Feedback and Grading student work
@assignmentRouter.post("/feedback/", tags=["Feedback and Grading to Student Work"])
async def create_feedback(feedback: Feedback):
    student_in_db = feedback_collection.find_one({"student": feedback.student_id})
    if student_in_db:
        raise HTTPException(status_code=400, detail="Student not found")
    feedback_dict = feedback.dict()
    # feedback_dict['teacher_id'] = "extracted_teacher_id_from_token"  # This should be extracted from the token
    feedback_collection.insert_one(feedback_dict)
    return {"status": "Feedback created successfully"}

@assignmentRouter.get("/feedback/{student_id}", tags=["Feedback and Grading to Student Work"])
async def get_feedback_by_student(student_id: str):
    feedbacks = list_serial(feedback_collection.find())
    return feedbacks