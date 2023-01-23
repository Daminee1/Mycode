import ast

from .standard_db_helper  import DbHelper
from .standard_response_helper  import StandardResponses
from datetime import datetime,date

from bson import ObjectId
import pandas as pd
from Stu_Teach_Details.settings import db

DbHelper = DbHelper()
StandardResponses = StandardResponses()


class StandardOperations:
    def addStandard(self, data):
        "add standard"
        #prepare dict for instert in mongo
        ins_query = {
            "name": data['name']
                   }

        result = DbHelper.insert_standard(ins_query)
        return result.inserted_id


    def update_subjects(self, id, **kwargs):
        """
        get standard  and send it to DbHelper
        """
        #### insert user data  ####
        set_query = kwargs
        query = {'_id': id}
        response = DbHelper.update_standard_record(query, set_query)
        return response



    def remove_standard(self, id_list, permanent):
        """
        delete standard record
        """
        #### init result obj ####
        print(id_list)
        result = {}
        ### this will check for permanent request ####
        if permanent == True:
            query = {"_id": id_list}
            # print("hello")
            res = DbHelper.delete_standard_by_id(query)
            if res.deleted_count > 0:
                result['deleted'] = True
            else:
                result['deleted'] = False
        elif permanent == False:
            query = {"_id": {"$in": id_list}}
            print(id_list)
            set_query = {"name": "Deleted"}
            res = DbHelper.update_standard_record(query, set_query)
            if res.modified_count > 0:
                result['deleted'] = True
            else:
                result['deleted'] = False
        else:
            result['deleted'] = False

        return result


    def get_standard_data(self, id,skip, limit):
        """
        get standard from DB and prepare for response
        """

        #build query
        query={}
        #check if i have id then add id filter to my query
        if id:
            query["_id"]=id

        #call db helper with query and pagination fields
        standard_data,count=DbHelper.fetch_standard_data(query,skip, limit)
        # perpare resp


        response={"data":[], "count":count}

        for standard in standard_data:


            response['data'].append({
                "name": standard['name'] if "name" in standard else "",
            })
        return response
