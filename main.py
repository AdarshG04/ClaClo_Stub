from fastapi import FastAPI
from routes.admin_router import auth_router
from routes.teacher_router import assignmentRouter

app = FastAPI()


app.include_router(auth_router)
app.include_router(assignmentRouter)
