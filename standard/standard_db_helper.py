from Stu_Teach_Details.settings import db
from bson import ObjectId
import json



class DbHelper:

    def insert_standard(self, ins_query):
        """
        add standard
        """
        result = db.standard.insert_one(ins_query)
        return result


    def update_standard_record(self, query, set_query):
        """
        save set query change for specified id of every
        """
        result = db.standard.update_many(query, {"$set": set_query}, upsert=False)
        return result

    def delete_standard_by_id(self, query):
        """
        permanent delete standard record
        """
        result = db.standard.delete_many(query)
        return result

    def fetch_standard_data(self, query,skip, limit):
        """
        return standard from DB
        """
        result = db.standard.find(query).skip(int(skip)).limit(int(limit)).sort([("_id", 1)])
        count = db.standard.count_documents(query)
        return result,count

        # fetch_data = [{"$match": query}, {"$skip": int(skip)}, {"$limit": int(limit)}, {"$sort": {"-id": 1}}]
        # result = db.standard.aggregate(fetch_data)
        # count = db.standard.count_documents(query)
        # return result, count

