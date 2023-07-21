from bson import ObjectId
from utils.db import sync_engine

def fetch_database_model(modelClass, obj_id:ObjectId):
    # SYNC engine
    data = sync_engine.find_one(modelClass, modelClass.id == obj_id)   
    if not data:
        raise ValueError("No %s found with ObjectId(%s)"%(modelClass.__name__, obj_id))
    res = data.dict()
    res['id'] = str(res['id']) # convert ObjectId to str
    return res

class ModelObjectId(ObjectId):
    """
        Pydantic / ODMantic custom field type
        https://art049.github.io/odmantic/fields/#custom-field-types
    """
    _model = None
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if cls._model == None:
            raise ValueError("No model provided")
        # Handle data coming from FastAPI request
        if isinstance(v, str):
            return ObjectId(v)
        # Handle data coming from MongoDB
        if isinstance(v, ObjectId):
            return fetch_database_model(cls._model, v) # SYNC engine for validation
        else:
            raise ValueError("%s validation Error"%(cls.__name__))
