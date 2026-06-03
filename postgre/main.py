from fastapi import FastAPI, Depends
from database import Base, SessionLocal, engine
from model import (courses,students,courses_data,students_data,student_data_response,update_student_data,
)
from sqlalchemy.orm import Session
import model
app = FastAPI()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

model.Base.metadata.create_all(bind=engine)

@app.post("/create_student", response_model=student_data_response)
def create_student(student: students_data, db: Session = Depends(get_db)):
    new_student = students(
        student_id=student.student_id,
        student_name=student.student_name,
        student_email=student.student_email,
        course_enrolled=student.course_enrolled,
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student

@app.post("/create_course")
def create_course(
    course: courses_data,
    db: Session = Depends(get_db)
):
    new_course = courses(
        course_code=course.course_code,
        course_name=course.course_name
    )

    db.add(new_course)
    db.commit()
    db.refresh(new_course)

    return new_course

@app.get("/get_student/{desired_student_id}", response_model=student_data_response)
def get_student(desired_student_id: int, db: Session = Depends(get_db)):
    desired_student = db.query(students).filter(students.student_id == desired_student_id).first()
    return desired_student

@app.delete("/delete_student/{desired_student_id}", response_model=student_data_response)
def delete_student(desired_student_id: int, db: Session = Depends(get_db)):
    desired_student = db.query(students).filter(students.student_id == desired_student_id).first()
    db.delete(desired_student)
    db.commit()
    return desired_student

@app.put("/update_student/{desired_student_id}", response_model=student_data_response)
def update_student(
    desired_student_id: int,
    desired_student_new_data: update_student_data,
    db: Session = Depends(get_db),
):
    desired_student = db.query(students).filter(students.student_id == desired_student_id).first()
    desired_student.student_name=desired_student_new_data.student_name
    desired_student.student_id=desired_student_new_data.student_id
    desired_student.student_email=desired_student_new_data.student_email
    db.commit()
    db.refresh(desired_student)
    return desired_student

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)