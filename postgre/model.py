from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from pydantic import BaseModel


class courses(Base):
    __tablename__ = "courses_database"
    course_code = Column(Integer, primary_key=True, nullable=False, index=True)
    course_name = Column(String, nullable=False, index=True)


class students(Base):
    __tablename__ = "students_database"
    student_id = Column(Integer, primary_key=True, nullable=False, index=True)
    student_name = Column(String, nullable=False, index=True)
    student_email = Column(String, nullable=False, index=True)
    course_enrolled = Column(Integer, ForeignKey("courses_database.course_code"), nullable=False)


class students_data(BaseModel):
    student_id: int
    student_name: str
    student_email: str
    course_enrolled: int


class student_data_response(BaseModel):
    student_id: int
    student_name: str
    student_email: str


class courses_data(BaseModel):
    course_code: int
    course_name: str

class update_student_data(BaseModel):
    student_id: int
    student_name: str
    student_email: str

    class Config:
        orm_mode = True