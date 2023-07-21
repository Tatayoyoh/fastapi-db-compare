from fastapi import APIRouter
from pydantic import EmailStr
from odmantic import Model, Reference
from odmantic import Field as OdField
from typing import List
from bson import ObjectId
from utils.db import motor_engine as engine

router = APIRouter(
    prefix='/test3',
    tags=["test"]
)

class StudentFriendOdmantic(Model):
    fullname: str
    email: EmailStr
    status: str
    isfamily: bool

class ParentOdmantic(Model):
    fullname: str
    email: EmailStr
    relation: str

class AddressOdmantic(Model):
    city: str
    street: str
    number: int
    zipcode: str
    other: str
    
class SchoolOdmantic(Model):
    name: str
    address: AddressOdmantic =  Reference()
    reputationscore: int
    note: str


from utils.odmantic import ModelObjectId

class StudentOdmantic(Model):

    class ParentObjectId(ModelObjectId):
        _model = ParentOdmantic

    fullname: str
    email: EmailStr
    course_of_study: str
    year: int = OdField(gt=0, lt=9)
    gpa: float = OdField(le=4.0)
    friends: List[StudentFriendOdmantic]   # nested object with uniq ID
    # parents: List[ParentObjectId]       # reference list
    parents: List[ObjectId]       # reference list
    address: AddressOdmantic = Reference()
    school:SchoolOdmantic = Reference()


@router.post("/odmantic/friend")
async def odmantic_create_friends(friend: StudentFriendOdmantic):
    await engine.save(friend)
    return friend

@router.post("/odmantic/parent")
async def odmantic_create_parents(parent: ParentOdmantic):
    await engine.save(parent)
    return parent

# IMPORTANT: pour les création/update mettre le 'response_model=XXXX'
@router.post("/odmantic", response_model=StudentOdmantic)
async def odmantic_create(student: StudentOdmantic):
    await engine.save(student)
    return student

@router.get("/odmantic")
async def odmantic_all():
    students = await engine.find(StudentOdmantic, sort=StudentOdmantic.fullname)
    return students

@router.get("/odmantic/friend")
async def odmantic_all_friends():
    friends = await engine.find(StudentFriendOdmantic, sort=StudentFriendOdmantic.fullname)
    return friends

@router.get("/odmantic/friend/{id}")
async def odmantic_friend(id):
    friend = await engine.find_one(StudentFriendOdmantic, StudentFriendOdmantic.id == ObjectId(id))
    return friend

@router.get("/odmantic/parents", response_model=ParentOdmantic)
async def odmantic_all_parents():
    parents = await engine.find(ParentOdmantic, sort=ParentOdmantic.fullname)
    return parents


@router.get("/odmantic/parent/{id}")
async def odmantic_parent(id):
    parent = await engine.find_one(ParentOdmantic, ParentOdmantic.id == ObjectId(id))
    return parent

@router.get("/odmantic/school")
async def odmantic_all_school():
    schools = await engine.find(SchoolOdmantic, sort=SchoolOdmantic.name)
    return schools







from beanie import Document, Link, PydanticObjectId
from pydantic import Field as pydField

class StudentFriendBeanie(Document):
    fullname: str
    email: EmailStr
    status: str
    isfamily: bool

class ParentBeanie(Document):
    fullname: str
    email: EmailStr
    relation: str

class AddressBeanie(Document):
    city: str
    street: str
    number: int
    zipcode: str
    other: str
    
class SchoolBeanie(Document):
    name: str
    address: AddressBeanie
    reputationscore: int
    note: str

class StudentBeanie(Document):
    fullname: str
    email: EmailStr
    course_of_study: str
    year: int = pydField(gt=0, lt=9)
    gpa: float = pydField(le=4.0)
    friends: List[StudentFriendBeanie]   # nested object with uniq ID
    parents: List[Link[ParentBeanie]]    # reference list (Link[])
    address: AddressBeanie
    school: SchoolBeanie


@router.post("/beanie/friend")
async def beanie_create_friends(friend: StudentFriendBeanie):
    await friend.save()
    return friend

@router.post("/beanie/parent")
async def beanie_create_parents(parent: ParentBeanie):
    await parent.save()
    return parent

@router.post("/beanie", response_model=StudentBeanie)
async def beanie_create(student: StudentBeanie):
    await student.save()
    return student

@router.get("/beanie", response_model=List[StudentBeanie], response_model_by_alias=False)
async def beanie_all():
    students = await StudentBeanie.all(sort=StudentBeanie.fullname, fetch_links=True).to_list()
    return students

@router.get("/beanie/friend")
async def beanie_all_friends():
    friends = await StudentFriendBeanie.all(sort=StudentFriendBeanie.fullname, fetch_links=True).to_list()
    return friends

@router.get("/beanie/friend/{id}")
async def beanie_friend(id):
    friend = await StudentFriendBeanie.find_one(StudentFriendBeanie.id == ObjectId(id), fetch_links=True)
    return friend

@router.get("/beanie/parents", response_model=ParentBeanie)
async def beanie_all_parents():
    parents = await ParentBeanie.all(sort=ParentBeanie.fullname, fetch_links=True).to_list()
    return parents


@router.get("/beanie/parent/{id}")
async def beanie_parent(id):
    parent = await ParentBeanie.find_one(ParentBeanie.id == ObjectId(id), fetch_links=True)
    return parent

@router.get("/beanie/school")
async def beanie_all_school():
    schools = await SchoolBeanie.find(sort=SchoolBeanie.name, fetch_links=True)
    return schools

