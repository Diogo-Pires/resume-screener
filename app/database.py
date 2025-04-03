from pymongo import MongoClient
from pymongo.collection import Collection

def get_database_client() -> MongoClient:
    client = MongoClient("mongodb://localhost:27017/")
    return client["resume_screener"]

def get_job_collection() -> Collection:
    return get_database_client()["jobs"]

def get_resume_collection() -> Collection:
    return get_database_client()["resumes"]