from Stu_Teach_Details.settings import db
from bson import ObjectId
import json



class DbHelper:

    def insert_subjects(self, ins_query):
        """
        add subjects
        """
        result = db.subjects.insert_one(ins_query)
        return result


    def update_subjects_record(self, query, set_query):
        """
        save set query change for specified id of every
        """
        result = db.subjects.update_many(query, {"$set": set_query}, upsert=False)
        return result

    def delete_subjects_by_id(self, query):
        """
        permanent delete subjects record
        """
        result = db.subjects.delete_many(query)
        return result

    def fetch_subjects_data(self, query,skip, limit):
        """
        return subjects from DB
        """
        result = db.subjects.find(query).skip(int(skip)).limit(int(limit)).sort([("_id", 1)])
        count = db.subjects.count_documents(query)

        return result,count
        #
        # fetch_data = [{"$match": query}, {"$skip": int(skip)}, {"$limit": int(limit)}, {"$sort": {"-id": 1}}]
        # result = db.subjects.aggregate(fetch_data)
        # count = db.subjects.count_documents(query)
        # return result, count
