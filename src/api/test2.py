from fastapi import APIRouter
from pydantic import EmailStr
from odmantic import Model, Reference
from odmantic import Field as OdField
from typing import List
from bson import ObjectId
from utils.db import motor_engine as engine
from utils.odmantic import ModelObjectId

router = APIRouter(
    prefix='/test2',
    tags=["test"]
)

class StudentFriendMongo(Model):
    fullname: str = OdField()
    email: EmailStr = OdField()
    status: str = OdField()
    isfamily: bool = OdField()

class ParentMongo(Model):
    fullname: str = OdField()
    email: EmailStr = OdField()
    relation: str = OdField()

class AddressMongo(Model):
    city: str = OdField()
    street: str = OdField()
    number: int = OdField()
    zipcode: str = OdField()
    other: str = OdField()
    
class SchoolMongo(Model):
    name: str = OdField()
    address: AddressMongo =  Reference()
    reputationscore: int = OdField()
    note: str = OdField()


class StudentMongo(Model):

    class ParentObjectId(ModelObjectId):
        _model = ParentMongo

    fullname: str = OdField()
    email: EmailStr = OdField()
    course_of_study: str = OdField()
    year: int = OdField(gt=0, lt=9)
    gpa: float = OdField(le=4.0)
    friends: List[StudentFriendMongo]   # nested object with uniq ID
    parents: List[ParentObjectId]       # reference list
    address: AddressMongo = Reference()
    school:SchoolMongo = Reference()


@router.post("/mongo/friend")
async def mongo_create_friends(friend: StudentFriendMongo):
    await engine.save(friend)
    return friend

@router.post("/mongo/parent")
async def mongo_create_parents(parent: ParentMongo):
    await engine.save(parent)
    return parent

# IMPORTANT: pour les création/update mettre le 'response_model=XXXX'
@router.post("/mongo", response_model=StudentMongo)
async def mongo_create(student: StudentMongo):
    await engine.save(student)
    return student

@router.get("/mongo")
async def mongo_all():
    students = await engine.find(StudentMongo, sort=StudentMongo.fullname)
    return students

@router.get("/mongo/friend")
async def mongo_all_friends():
    friends = await engine.find(StudentFriendMongo, sort=StudentFriendMongo.fullname)
    return friends

@router.get("/mongo/friend/{id}")
async def mongo_friend(id):
    friend = await engine.find_one(StudentFriendMongo, StudentFriendMongo.id == ObjectId(id))
    return friend

@router.get("/mongo/parents", response_model=ParentMongo)
async def mongo_all_parents():
    parents = await engine.find(ParentMongo, sort=ParentMongo.fullname)
    return parents


@router.get("/mongo/parent/{id}")
async def mongo_parent(id):
    parent = await engine.find_one(ParentMongo, ParentMongo.id == ObjectId(id))
    return parent

@router.get("/mongo/school")
async def mongo_all_school():
    schools = await engine.find(SchoolMongo, sort=SchoolMongo.name)
    return schools




import ormar
from utils.db import database, metadata
from typing import Optional

class Friend(ormar.Model):
    class Meta:
        tablename = "friend"
        metadata = metadata
        database = database
    id:int = ormar.Integer(primary_key=True)
    fullname:str = ormar.String(max_length=100)
    email: EmailStr = OdField()
    status:str = ormar.String(max_length=100)
    isfamily: bool = OdField()

class Parent(ormar.Model):
    class Meta:
        tablename = "parent"
        metadata = metadata
        database = database
    id:int = ormar.Integer(primary_key=True)
    fullname:str = ormar.String(max_length=100)
    email: EmailStr = ormar.String(max_length=100)
    relation:str = ormar.String(max_length=100)

class Address(ormar.Model):
    class Meta:
        tablename = "address"
        metadata = metadata
        database = database
    id:int = ormar.Integer(primary_key=True)
    city:str = ormar.String(max_length=100)
    street:str = ormar.String(max_length=100)
    number:int = ormar.Integer()
    zipcode:str = ormar.String(max_length=100)
    other:str = ormar.String(max_length=100)
    
class School(ormar.Model):
    class Meta:
        tablename = "school"
        metadata = metadata
        database = database
    id:int = ormar.Integer(primary_key=True)
    name:str = ormar.String(max_length=100)
    address:AddressMongo =  Reference()
    address:Optional[Address] = ormar.ForeignKey(Address, name="address_id")
    reputationscore:int = ormar.Integer()
    note:str = ormar.String(max_length=100)

# class StudentParent(ormar.Model):
#     class Meta:
#         tablename = "student_x_parent"
#         metadata = metadata
#         database = database

# class StudentAddress(ormar.Model):
#     class Meta:
#         tablename = "student_x_address"
#         metadata = metadata
#         database = database

# class StudentFriend(ormar.Model):
#     class Meta:
#         tablename = "student_x_friend"
#         metadata = metadata
#         database = database

class StudentPgsql(ormar.Model):
    class Meta:
        tablename = "students_2"
        metadata = metadata
        database = database

    id:int = ormar.Integer(primary_key=True)
    fullname: str = ormar.String(max_length=100)
    email: EmailStr = ormar.String(max_length=100)
    course_of_study: str = ormar.String(max_length=100)
    year: int = ormar.Integer()
    gpa: float = ormar.Float()
    # non_db_field: str = ormar.String(max_length=100, pydantic_only=True)

    friends:List[Friend] = ormar.ManyToMany(Friend)
    parents:List[Parent] = ormar.ManyToMany(Parent)
    address:List[Address] = ormar.ForeignKey(Address, name="address_id")
    school: School = ormar.ForeignKey(School, name="school_id")


@router.post("/pgsql/parent")
async def pgsql_create(student: StudentPgsql):
    await student.save()
    return student

@router.post("/pgsql")
async def pgsql_create(student: StudentPgsql):
    await student.save()
    return student

@router.get("/pgsql")
async def pgsql_all():
    s = await StudentPgsql.objects.all()
    return s