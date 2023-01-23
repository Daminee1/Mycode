import json
from django.shortcuts import render
from Stu_Teach_Details.settings import db
from rest_framework.views import APIView
from rest_framework.response import Response
from .users_response_helper import UsersResponses
from .users_operations_helper import UsersOperations
from bson import ObjectId
import json

UsersResponses = UsersResponses()
UsersOperations = UsersOperations()

def home(request):
    user=list(db.user.find())
    subjects=list(db.subjects.find())
    standard=list(db.standard.find())
    for us in user:
        us["id"] = str(us["_id"])
    for sub in subjects:
        sub["id"] = str(sub["_id"])
    for std in standard:
        std["id"] = str(std["_id"])
    # for user in user:
    #     print("----------------------------------",user)

    return render(request,'user_home.html',{'user':user,'subjects':subjects, 'standard':standard})

class User_Details(APIView):
    def post(self,request):

        try:
            print(request.data)
            #validate data
            if 'name' in request.data:
                name = request.data['name']
            else:
                error_message = {"message": "Name Required"}
                return UsersResponses.get_status_400(error_message)

            if 'role' in request.data:
                role = request.data['role']
            else:
                error_message = {"message": "role Required"}
                return UsersResponses.get_status_400(error_message)
            if 'address' in request.data:
                address = request.data['address']
            else:
                error_message = {"message": "address Required"}
                return UsersResponses.get_status_400(error_message)

            if 'subjects' in request.data:
                subjects=[]
                subject=list(request.data['subjects'])
                for subject in subject:
                    try:
                        subject= ObjectId(str(subject))
                        subjects.append(subject)

                    except:
                     error_message = {"message": "Invalid subjects Id"}
                     return UsersResponses.get_status_422(error_message)
            else:
                error_message = {"message": "subjects Required"}
                return UsersResponses.get_status_400(error_message)

            if 'standard' in request.data:
                standard = request.data['standard']

                try:
                    standard= ObjectId(str(standard))


                except:
                    error_message = {"message": "Invalid standard Id"}
                    return UsersResponses.get_status_422(error_message)
            else:
                error_message = {"message": "standard Required"}
                return UsersResponses.get_status_400(error_message)
            if 'kyc_doc' in request.data:
                kyc_doc = request.data['kyc_doc']
            else:
                error_message = {"message": "kyc_doc Required"}
                return UsersResponses.get_status_400(error_message)
            if 'date_of_birth' in request.data:
                date_of_birth = request.data['date_of_birth']
            else:
                error_message = {"message": "date_of_birth Required"}
                return UsersResponses.get_status_400(error_message)
            if 'gender' in request.data:
                gender = request.data['gender']
            else:
                error_message = {"message": "gender Required"}
                return UsersResponses.get_status_400(error_message)
            if 'status' in request.data:
                status = request.data['status']
            else:
                error_message = {"message": "status Required"}
                return UsersResponses.get_status_400(error_message)

            kwargs={"name":name,"role":role,"address" : address,"subjects":subjects,"standard":standard,"kyc_doc":kyc_doc,
                          "date_of_birth":date_of_birth,  "gender":gender,  "status":status}


            #call op helper
            result = UsersOperations.addUser(kwargs)

            #prepare response code
            if result:
                response = {"message": "User Inserted"}
                return UsersResponses.get_status_201(response)
            else:
                error_message = {"message": "User Insert Failed"}
                return UsersResponses.get_status_400(error_message)





        except Exception as e:
            print("exception -->", e)
            return UsersResponses.get_status_500()

    def patch(self,request):
        #### Check required parameter ####
        try:
            if 'id' in request.data:
                id = request.data['id']
            else:
                error_message = {"message": "id Required"}
                return UsersResponses.get_status_400(error_message)

            ### validate values ####
            try:
                id = ObjectId(str(id))
                # print(id)
            except:
                error_message = {"message": "Invalid User Id"}
                return UsersResponses.get_status_422(error_message)

            kwargs = {}

            if 'name' in request.data:
                kwargs['name'] = request.data['name']

            if 'role' in request.data:
                kwargs['role'] = request.data['role']

            if 'address' in request.data:
                kwargs['address'] = request.data['address']

            if 'subjects' in request.data:
                kwargs['subjects'] = request.data['subjects']

            if 'standard' in request.data:
                kwargs['standard'] = request.data['standard']

            if 'kyc_doc' in request.data:
                kwargs['kyc_doc'] = request.data['kyc_doc']

            if 'date_of_birth' in request.data:
                kwargs['date_of_birth'] = request.data['date_of_birth']

            if 'gender' in request.data:
                kwargs['gender'] = request.data['gender']

            if 'status' in request.data:
                kwargs['status'] = request.data['status']

            # call
            result = UsersOperations.update_user(id, **kwargs)

            # prepare response code
            if result:
                response = {"message": "User Updated"}
                return UsersResponses.get_status_201(response)
            else:
                error_message = {"message": "User Updated Failed"}
                return UsersResponses.get_status_400(error_message)

        except Exception as e:
            print("exception -->", e)
            return UsersResponses.get_status_500()



    def delete(self, request):
        """
        Delete user record API
        """
        print(request.data)

        # try:
           # Check for required parameter
        if not request.data['id']:
            error_message = {"message": "Id Required"}
            return UsersResponses.get_status_400(error_message)

        # validate values
        try:

           id=request.data['id']
           print(id)
           obj_ids = ObjectId(str(id))
           # db.user.delete({"_id":ObjectId(str(ids))})

        except:
           error_message = {"message": "Invalid User Id"}
           return UsersResponses.get_status_422(error_message)

        result = UsersOperations.remove_user(obj_ids, True)

        # prepare response code
        if result['deleted'] == True:
            response = {"message": "User Deleted"}
            return UsersResponses.get_status_202(response)
        else:
            error_message = {"message": "User Delete Failed"}
            return UsersResponses.get_status_400(error_message)
        # except:
        #     return UsersResponses.get_status_500()

    def get(self, request):
        '''
               List User API
               '''
        # try:



        #### Check for required parameter ####
        try:
            skip = int(request.GET.get('skip'))
        except:
            response = {"message": "skip required and it must be an integer value"}
            return UsersResponses.get_status_422(response)

        #### Check for required parameter ####
        try:
            limit = int(request.GET.get('limit'))
        except:
            response = {"message": "limit required and it must be an integer value"}
            return UsersResponses.get_status_422(response)

        #### Check for required parameter ####
        try:
            status = request.GET.get('status')
        except:
            response = {"message": "status required and it must be an string value"}
            return UsersResponses.get_status_422(response)


        #### check for valid id filter ####
        if request.GET.get('id'):
            id = request.GET.get('id')
            try:
                id = ObjectId(str(id))
            except:
                error_message = {"message": "Enter valid ObjectId"}
                return UsersResponses.get_status_422(error_message)
        else:
            id = None


        #### get response and preapare ####
        result = UsersOperations.get_user_data(id,status,skip,limit)

        #### init and prepare response object ####
        response = {}
        response['total_data'] = result['data']
        response['total_records'] = result['count']

        if response['total_records'] > 0:
            return UsersResponses.get_status_200(response)
        else:
            error_message = {"message": "User Not Found"}
            return UsersResponses.get_status_204(error_message)
        # except:
        #     return EventsResponses.get_status_500()


class User_Details_Get(APIView):
    def get(self, request):
        if request.GET.get('id'):
            id = request.GET.get('id')
            try:
                id = ObjectId(str(id))
            except:
                error_message = {"message": "Enter valid ObjectId"}
                return UsersResponses.get_status_422(error_message)
        else:
            id = None

        #### get response and preapare ####
        result = UsersOperations.get_user_data_by_id(id)
        # print(result)
        #### init and prepare response object ####
        response = {}
        response['total_data'] = result['data']
        response['total_records'] = result['count']

        if response['total_records'] > 0:
            return UsersResponses.get_status_200(response)
        else:
            error_message = {"message": "User Not Found"}
            return UsersResponses.get_status_204(error_message)
        # except:
        #     return EventsResponses.get_status_500()










