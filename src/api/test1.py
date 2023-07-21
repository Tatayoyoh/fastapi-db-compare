from fastapi import APIRouter

router = APIRouter(
    prefix='/test1',
    tags=["test"]
)

#################################
# REDIS / redis-om
from pydantic import EmailStr
from redis_om import JsonModel, Field as redField

class Student(JsonModel):
    fullname: str = redField()
    email: EmailStr = redField()
    course_of_study: str = redField()
    year: int = redField(gt=0, lt=9)
    gpa: float = redField(le=4.0)

    class Config:
        schema_extra = {
            "example": {
                "fullname": "John Doe",
                "email": "jdoe@x.edu.ng",
                "course_of_study": "Water resources engineering",
                "year": 2,
                "gpa": "3.0",
            }
        }

@router.post("/redis")
async def redis_create(student:Student):
    student.save()
    return student

@router.get("/redis")
async def redis_all():
    return await Student.find().sort_by('fullname').all()

#################################
# MONGO / odmantic
from odmantic import Model
from odmantic import Field as OdField
from utils.db import motor_engine as engine
from utils.db import sync_engine as engine

class StudentMongo(Model):
    fullname: str = OdField()
    email: EmailStr = OdField()
    course_of_study: str = OdField()
    year: int = OdField(gt=0, lt=9)
    gpa: float = OdField(le=4.0)

    class Config:
        schema_extra = {
            "example": {
                "fullname": "John Doe",
                "email": "jdoe@x.edu.ng",
                "course_of_study": "Water resources engineering",
                "year": 2,
                "gpa": "3.0",
            }
        }

@router.post("/mongo")
async def mongo_create(student: StudentMongo):
    await engine.save(student)
    return student


@router.get("/mongo")
async def mongo_all():
    students = await engine.find(StudentMongo, sort=StudentMongo.fullname)
    return students


#################################
# PostgreSQL  / ormar
import ormar
from utils.db import database, metadata

class StudentPgsql(ormar.Model):
    class Meta:
        tablename = "students"
        metadata = metadata
        database = database

    id: int = ormar.Integer(primary_key=True)
    fullname: str = ormar.String(max_length=100)
    email: EmailStr = ormar.String(max_length=100)
    course_of_study: str = ormar.String(max_length=100)
    year: int = ormar.Integer()
    gpa: float = ormar.Float()
    # non_db_field: str = ormar.String(max_length=100, pydantic_only=True)

@router.post("/pgsql")
async def pgsql_create(student: StudentPgsql):
    await student.save()
    return student

@router.get("/pgsql")
async def pgsql_all():
    s = await StudentPgsql.objects.all()
    return s