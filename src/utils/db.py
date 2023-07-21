import sqlalchemy
import databases

DB_URL = 'postgresql://root:root@fastapi-db-compare-postgres:5432/pgsqldb'
MONGO_URL = 'mongodb://fastapi-db-compare-mongo:27017/'
MONGO_DB = 'example_db'

database = databases.Database(DB_URL)
metadata = sqlalchemy.MetaData()


from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine
motor_client = AsyncIOMotorClient(MONGO_URL)
motor_engine = AIOEngine(client=motor_client, database=MONGO_DB)


from pymongo import MongoClient
from odmantic import SyncEngine

sync_client = MongoClient(MONGO_URL)
sync_engine = SyncEngine(client=sync_client, database=MONGO_DB)