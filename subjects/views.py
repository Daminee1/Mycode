from django.shortcuts import render
from Stu_Teach_Details.settings import db
from rest_framework.views import APIView
from rest_framework.response import Response
from .subjects_response_helper import SubjectsResponses
from .subjects_operations_helper import SubjectsOperations
from bson import ObjectId


SubjectsResponses = SubjectsResponses()
SubjectsOperations = SubjectsOperations()


class Subjects_Details(APIView):
    def post(self,request):
        try:
            #validate data
            if 'name' not in request.data:
                error_message = {"message": "Name Required"}
                return SubjectsResponses.get_status_400(error_message)

            #call op helper
            result = SubjectsOperations.addSubjects(request.data)

            #prepare response code
            if result:
                response = {"message": "Subject Inserted"}
                return SubjectsResponses.get_status_201(response)
            else:
                error_message = {"message": "Subject Insert Failed"}
                return SubjectsResponses.get_status_400(error_message)
        except Exception as e:
            print("exception -->", e)
            return SubjectsResponses.get_status_500()

    def patch(self, request):
        #### Check required parameter ####
        try:
            if 'id' in request.data:
                id = request.data['id']
            else:
                error_message = {"message": "id Required"}
                return SubjectsResponses.get_status_400(error_message)

            ### validate values ####
            try:
                id = ObjectId(str(id))
            except:
                error_message = {"message": "Invalid User Id"}
                return SubjectsResponses.get_status_422(error_message)

            kwargs = {}

            if 'name' in request.data:
                kwargs['name'] = request.data['name']

            # call
            result = SubjectsOperations.update_subjects(id, **kwargs)

            # prepare response code
            if result:
                response = {"message": "Subjects Updated"}
                return SubjectsResponses.get_status_201(response)
            else:
                error_message = {"message": "Subjects Updated Failed"}
                return SubjectsResponses.get_status_400(error_message)

        except Exception as e:
            print("exception -->", e)
            return SubjectsResponses.get_status_500()

    def delete(self, request):
        """
        Delete Subjects record API
        """
        try:
           # Check for required parameter
            if not request.data['id']:
                error_message = {"message": "Id Required"}
                return SubjectsResponses.get_status_400(error_message)

            # validate values

            try:
               ids=list(request.data['id'])
               obj_ids = [ObjectId(id) for id in ids]
            except:
               error_message = {"message": "Invalid User Id"}
               return SubjectsResponses.get_status_422(error_message)

            result = SubjectsOperations.remove_subjects(obj_ids, True)

           # prepare response code
            if result['deleted'] == True:
                response = {"message": "User Deleted"}
                return SubjectsResponses.get_status_202(response)
            else:
                error_message = {"message": "User Delete Failed"}
                return SubjectsResponses.get_status_400(error_message)
        except:
            return SubjectsResponses.get_status_500()


    def get(self, request):
        '''
               List Subjects API
               '''

        #### Check for required parameter ####
        try:
            skip = int(request.GET.get('skip'))
        except:
            response = {"message": "skip required and it must be an integer value"}
            return SubjectsResponses.get_status_422(response)

        #### Check for required parameter ####
        try:
            limit = int(request.GET.get('limit'))
        except:
            response = {"message": "limit required and it must be an integer value"}
            return SubjectsResponses.get_status_422(response)


        #### check for valid id filter ####
        if request.GET.get('id'):
            id = request.GET.get('id')
            try:
                id = ObjectId(str(id))
            except:
                error_message = {"message": "Enter valid ObjectId"}
                return SubjectsResponses.get_status_422(error_message)
        else:
            id = None


        #### get response and preapare ####
        result = SubjectsOperations.get_subjects_data(id,skip,limit)

        #### init and prepare response object ####
        response1 = {}
        response1['total_data'] = result['data']
        response1['total_records'] = result['count']

        if response1['total_records'] > 0:
            return SubjectsResponses.get_status_200(response1)
        else:
            error_message = {"message": "User Not Found"}
            return SubjectsResponses.get_status_204(error_message)

