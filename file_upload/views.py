from django.shortcuts import render

from Stu_Teach_Details.settings import db
from rest_framework.views import APIView
from .file_upload_response_helper import FileResponses
from .file_upload_operations_helper import FileOperations

FileOperations = FileOperations()
FileResponses = FileResponses()

class File_Upload(APIView):
    def post(self,request):
        try:
            #validate data
            if 'file_name' in request.data:
                file_name = request.data['name']
            else:
                error_message = {"message": "File Name Required"}
                return FileResponses.get_status_400(error_message)

            if 'file' in request.FILES:
                file = request.data['file']
            else:
                error_message = {"message": "file Required"}
                return FileResponses.get_status_400(error_message)

            kwargs={"file_name":file_name,"file":file}



            # call
            result = FileOperations.upload_file(kwargs)

        except Exception as e:
            print("exception -->", e)
            return FileResponses.get_status_500()


