from Stu_Teach_Details.settings import db
from bson import ObjectId
import json



class DbHelper:

    def insert_user(self, ins_query):
        """
        add new category for business user
        """
        result = db.user.insert_one(ins_query)
        return result



    def update_user_record(self, query, set_query):
        """
        save set query change for specified id of every
        """
        result = db.user.update_many(query, {"$set": set_query}, upsert=False)
        return result

    def delete_user_by_id(self, query):
        """
        permanent delete user record
        """
        print("=================",query)
        result= db.user.delete_many(query)

        return result

    def fetch_user_data(self, query):
        """
        return user from DB
        """
        result=db.user.aggregate(query)
        return result



    def fetch_users_by_ids(self, query):
       res = db.user.aggregate(query)
       return res



  # def fetch_user_data(self, query,skip,limit):
    #     """
    #     return user from DB
    #     """
    #     # print(limit,skip)
    #     result = db.user.find(query).skip(int(skip)).limit(int(limit)).sort([("_id", 1)])
    #     count = db.user.count_documents(query)
    #     return result, count

    # fetch_data= [{"$match": query}, {"$skip": int(skip)}, {"$limit": int(limit)}, {"$sort": {"-id": 1}}]
    # result= db.user.aggregate(fetch_data)
    # count = db.user.count_documents(query)
    # return result, count

 # result = db.user.find(query)
        # count = db.user.count_documents(query)
        # return result, count
