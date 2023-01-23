import ast

from .users_db_helper import DbHelper
from .users_response_helper import UsersResponses
from datetime import datetime, date

from bson import ObjectId
import pandas as pd
from Stu_Teach_Details.settings import db

DbHelper = DbHelper()
UsersResponses = UsersResponses()


class UsersOperations:

    # def getAge(self, dob):
    #     dob=data["date_of_birth"]
    #     now =datatime.today()
    #     result=(now.date-dob.date,now.month-dob.month,now.year-dob.year)

    def calculate_age(self, born):
        today = date.today()
        age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
        return age

    def addUser(self, data):
        """
        get user and send it to DbHelper
        """

        ins_query = {
            "name": data['name'], "role": data["role"],
            "address": data["address"],
            "subjects": data["subjects"],
            "standard": data["standard"],
            "kyc_doc": data["kyc_doc"],
            "date_of_birth": data["date_of_birth"],
            "gender": data["gender"],
            "status": data["status"]
        }

        result = DbHelper.insert_user(ins_query)
        return result.inserted_id

    def update_user(self, id, **kwargs):
        """
        get user and send it to DbHelper
        """
        #### insert user data ####
        set_query = kwargs
        query = {'_id': id}
        response = DbHelper.update_user_record(query, set_query)

        return response

    def remove_user(self, id_list, permanent):
        """
        delete user record
        """
        #### init result obj ####
        print(id_list)
        result = {}

        #### this will check for permanent request ####
        if permanent == True:
            query = {"_id": id_list}
            print("hello")
            print(query)
            res= DbHelper.delete_user_by_id(query)
            print("---------------------------------",res,res.deleted_count)
            if res.deleted_count > 0:
                result['deleted'] = True
            else:
                result['deleted'] = False
        elif permanent == False:
            query = {"_id": {"$in": id_list}}
            print(id_list)
            set_query = {"status": "Deleted"}
            res = DbHelper.update_user_record(query, set_query)
            if res.modified_count > 0:
                result['deleted'] = True
            else:
                result['deleted'] = False
        else:
            result['deleted'] = False

        return result


    def get_user_data(self, id, status, skip, limit):

        """
        get USER from DB and prepare for response
        """
        # build query
        query = [
                {"$match":
                     {"status":status}},
                {"$lookup": {
                             "from": "standard",
                             "localField": "standard",
                             "foreignField": "_id",
                             "as": "standard_data"
                            }
                },
                {"$lookup": {
                    "from": "subjects",
                    "localField": "subjects",
                    "foreignField": "_id",
                    "as": "subjects_data"
                        }
                },
             {"$skip":skip},
            {"$limit": limit},

            {"$project":{"standard":0,"subjects":0,"_id":0}}
         ]



        if id:

            query=[{"$match":{"_id": id}},
                   {"$lookup": {
                             "from": "standard",
                             "localField": "standard",
                             "foreignField": "_id",
                             "as": "standard_data"
                            }
                },
                   {"$lookup": {
                       "from": "subjects",
                       "localField": "subjects",
                       "foreignField": "_id",
                       "as": "subjects_data"
                   }
                   }, {"$skip":skip},
            {"$limit": limit},


            {"$project":{"standard":0,"subjects":0,"_id":0}}
                   ]

            response={'data':[],'count':0}

            particular_data=DbHelper.fetch_users_by_ids(query)

            count=0
            for data in particular_data:
                print("==============================",data)
                count=count+1

                subjects_data = []
                for subject in data['subjects_data']:
                    subjects_data.append(subject['name'])
                response['data'].append({"name": data['name'] if "name" in data else "",
                "role": data['role'] if "role" in data else "",
                "address": data['address'] if "address" in data else "",
                "subjects": subjects_data,
                # "standard": data['standard_data'][0]['name'] if "standard_data" in data else "",
                "status": data['status'] if "status" in data else "",
                "kyc_doc": data['kyc_doc'] if "kyc_doc" in data else "",
                "gender": data['gender'] if "gender" in data else "",
                "date_of_birth": data['date_of_birth'] if "date_of_birth" in data else "",
                })
                response['count']=count

            return response


        # call db helper with query and pagination fields

        user_data = DbHelper.fetch_user_data(query)

        response = {"data": [], "count":0}
        count = 0
        for user in user_data:
            count = count + 1
            print(user)
            dob_str = user['date_of_birth']
            subjects_data=[]
            for subject in user['subjects_data']:
                subjects_data.append(subject['name'])


            dob = datetime.strptime(dob_str, '%m-%d-%Y').date()
            age = self.calculate_age(dob)

            response['data'].append({
                "name": user['name'] if "name" in user else "",
                "role": user['role'] if "role" in user else "",
                "address": user['address'] if "address" in user else "",

                "subjects": subjects_data ,
                # "standard": user['standard_data'][0]['name'] if "standard_data" in user else "",
                "date_of_birth": user['date_of_birth'] if "date_of_birth" in user else "",
                "gender": user['gender'] if "gender" in user else "",
                "kyc_doc": user['kyc_doc'] if "kyc_doc" in user else "",
                "status": user['status'] if "status" in user else "",
                "age": age,

                # "date_of_birth":dob_str
            })
            response['count'] = count
        return response

    def get_user_data_by_id(self, id):

        """
        get USER from DB and prepare for response
        """
        query = [{"$match": {"_id": id}},
                 {"$lookup": {
                     "from": "standard",
                     "localField": "standard",
                     "foreignField": "_id",
                     "as": "standard_data"
                 }
                 },
                 {"$lookup": {
                     "from": "subjects",
                     "localField": "subjects",
                     "foreignField": "_id",
                     "as": "subjects_data"
                 }
                 },

                 {"$project": {"standard": 0, "subjects": 0, "_id": 0}}
                 ]

        response = {'data': [], 'count': 0}
        particular_data = DbHelper.fetch_users_by_ids(query)

        count = 0
        for data in particular_data:
            print(data)

            count = count + 1
            subjects_data = []
            for subject in data['subjects_data']:
                subjects_data.append(subject['name'])
                response['data'].append({"name": data['name'] if "name" in data else "",
                                         "role": data['role'] if "role" in data else "",
                                         "address": data['address'] if "address" in data else "",
                                         "subjects": subjects_data,
                                         # "standard": data['standard_data'][0]['name'] if "standard_data" in data else "",
                                         "status": data['status'] if "status" in data else "",
                                         "kyc_doc": data['kyc_doc'] if "kyc_doc" in data else "",
                                         "gender": data['gender'] if "gender" in data else "",
                                         "date_of_birth": data['date_of_birth'] if "date_of_birth" in data else "",
                                         })
                response['count'] = count

            return response


