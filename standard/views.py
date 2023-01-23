from django.shortcuts import render
from Stu_Teach_Details.settings import db
from rest_framework.views import APIView
from rest_framework.response import Response
from .standard_response_helper import StandardResponses
from .standard_operations_helper import StandardOperations
from bson import ObjectId


StandardResponses = StandardResponses()
StandardOperations = StandardOperations()


class Standard_Details(APIView):
    def post(self,request):
        try:
            #validate data
            if 'name' not in request.data:
                error_message = {"message": "Name Required"}
                return StandardResponses.get_status_400(error_message)

            #call op helper
            result = StandardOperations.addStandard(request.data)

            #prepare response code
            if result:
                response = {"message": "Standard Inserted"}
                return StandardResponses.get_status_201(response)
            else:
                error_message = {"message": "Standard Insert Failed"}
                return StandardResponses.get_status_400(error_message)
        except Exception as e:
            print("exception -->", e)
            return StandardResponses.get_status_500()

    def patch(self, request):
        #### Check required parameter ####
        try:
            if 'id' in request.data:
                id = request.data['id']
            else:
                error_message = {"message": "id Required"}
                return StandardResponses.get_status_400(error_message)

            ### validate values ####
            try:
                id = ObjectId(str(id))
            except:
                error_message = {"message": "Invalid User Id"}
                return StandardResponses.get_status_422(error_message)

            kwargs = {}

            if 'name' in request.data:
                kwargs['name'] = request.data['name']

            # call
            result = StandardOperations.update_subjects(id, **kwargs)

            # prepare response code
            if result:
                response = {"message": "Standard Updated"}
                return StandardResponses.get_status_201(response)
            else:
                error_message = {"message": "Standard Updated Failed"}
                return StandardResponses.get_status_400(error_message)

        except Exception as e:
            print("exception -->", e)
            return StandardResponses.get_status_500()

    def delete(self, request):
        """
        Delete Standard record API
        """
        try:
           # Check for required parameter
            if not request.data['id']:
                error_message = {"message": "Id Required"}
                return StandardResponses.get_status_400(error_message)

            # validate values

            try:
               ids=list(request.data['id'])
               obj_ids = [ObjectId(id) for id in ids]
            except:
               error_message = {"message": "Invalid User Id"}
               return StandardResponses.get_status_422(error_message)

            result = StandardOperations.remove_standard(obj_ids, False)

           # prepare response code
            if result['deleted'] == True:
                response = {"message": "Standard Deleted"}
                return StandardResponses.get_status_202(response)
            else:
                error_message = {"message": "Standard Delete Failed"}
                return StandardResponses.get_status_400(error_message)
        except:
            return StandardResponses.get_status_500()


    def get(self, request):
        '''
               List Subjects API
               '''

        #### Check for required parameter ####
        try:
            skip = int(request.GET.get('skip'))
        except:
            response = {"message": "skip required and it must be an integer value"}
            return StandardResponses.get_status_422(response)

        #### Check for required parameter ####
        try:
            limit = int(request.GET.get('limit'))
        except:
            response = {"message": "limit required and it must be an integer value"}
            return StandardResponses.get_status_422(response)


        #### check for valid id filter ####
        if request.GET.get('id'):
            id = request.GET.get('id')
            try:
                id = ObjectId(str(id))
            except:
                error_message = {"message": "Enter valid ObjectId"}
                return StandardResponses.get_status_422(error_message)
        else:
            id = None


        #### get response and preapare ####
        result = StandardOperations.get_standard_data(id,skip, limit)

        #### init and prepare response object ####
        response1 = {}
        response1['total_data'] = result['data']
        response1['total_records'] = result['count']

        if response1['total_records'] > 0:
            return StandardResponses.get_status_200(response1)
        else:
            error_message = {"message": "Standard Not Found"}
            return StandardResponses.get_status_204(error_message)

