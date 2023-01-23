import ast

from .subjects_db_helper  import DbHelper
from .subjects_response_helper  import SubjectsResponses
from datetime import datetime,date

from bson import ObjectId
import pandas as pd
from Stu_Teach_Details.settings import db

DbHelper = DbHelper()
SubjectsResponses = SubjectsResponses()


class SubjectsOperations:
    def addSubjects(self, data):
        "add subjects"
        #prepare dict for instert in mongo
        ins_query = {
            "name": data['name']
                   }

        result = DbHelper.insert_subjects(ins_query)
        return result.inserted_id


    def update_subjects(self, id, **kwargs):
        """
        get subjects and send it to DbHelper
        """
        #### insert user data  ####
        set_query = kwargs
        query = {'_id': id}
        response = DbHelper.update_subjects_record(query, set_query)
        return response



    def remove_subjects(self, id_list, permanent):
        """
        delete subjects record
        """
        #### init result obj ####
        print(id_list)
        result = {}
        ### this will check for permanent request ####
        if permanent == True:
            query = {"_id": id_list}
            # print("hello")
            res = DbHelper.delete_subjects_by_id(query)
            if res.deleted_count > 0:
                result['deleted'] = True
            else:
                result['deleted'] = False
        elif permanent == False:
            query = {"_id": {"$in": id_list}}
            print(id_list)
            set_query = {"name": "Deleted"}
            res = DbHelper.update_subjects_record(query, set_query)
            if res.modified_count > 0:
                result['deleted'] = True
            else:
                result['deleted'] = False
        else:
            result['deleted'] = False

        return result


    def get_subjects_data(self, id,skip, limit):
        """
        get subjects from DB and prepare for response
        """

        #build query
        query={}
        #check if i have id then add id filter to my query
        if id:
            query["_id"]=id

        #call db helper with query and pagination fields
        subjects_data,count=DbHelper.fetch_subjects_data(query,skip, limit)
        response={"data":[], "count":count}


        for subject in subjects_data:
            response['data'].append({
                "name": subject['name'] if "name" in subject else "",
            })
        return response
