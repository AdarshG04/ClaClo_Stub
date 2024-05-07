def individual_serial(feedback) -> dict:
    return{
        "student_id": str(feedback["_id"]),
        "teacher_id": feedback["teacher_id"],
        "grade": feedback["grade"],
        "comments": feedback["comments"],
        "created_at": feedback["created_at"]
    }
def list_serial(feedbacks) -> list:
    return[individual_serial(feedback) for feedback in feedbacks]