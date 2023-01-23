from rest_framework.response import Response
from rest_framework import status

class UsersResponses:

    #### Status 2xx responses ####
    def get_status_200_micro(self, data):
        return Response(data, status=status.HTTP_200_OK)

    #### Status 2xx responses ####
    def get_status_200(self,data):
        response = {"message": "success"}
        response['recordsTotal'] = data['total_records']
        response['result'] = data['total_data']
        return Response(response, status=status.HTTP_200_OK)

    def get_status_201(self,data):
        response = {"message": "success"}
        response['result'] = data
        return Response(response, status=status.HTTP_201_CREATED)

    def get_status_202(self,response):
        return Response(response, status=status.HTTP_202_ACCEPTED)

    def get_status_204(self,response):
        return Response(response, status=status.HTTP_204_NO_CONTENT)

    #### Status 3xx responses ####
    def get_status_304(self, error_message):
        return Response(error_message, status=status.HTTP_304_NOT_MODIFIED)

    #### Status 4xx responses ####
    def get_status_400(self, error_message):
        return Response(error_message, status=status.HTTP_400_BAD_REQUEST)

    def get_status_401(self, error_message):
        return Response(error_message, status=status.HTTP_401_UNAUTHORIZED)

        def get_status_404(self, error_message):
            return Response(error_message, status=status.HTTP_404_NOT_FOUND)

    def get_status_409(self, error_message):
        return Response(error_message, status=status.HTTP_409_CONFLICT)

    def get_status_422(self, error_message):
        return Response(error_message, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
    #### Status 5xx responses ####
    def get_status_500(self):
        error_message = {"message": "internal server error"}
        return Response(error_message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
