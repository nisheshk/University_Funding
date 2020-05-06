from rest_framework.views       import APIView
from rest_framework.response import Response
import os
import boto3
from django.conf import settings
import datetime

class TestingView(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request, format = None):

            post_data = request.data
            print (post_data)
            AWS_SERVER_PUBLIC_KEY = settings.AWS_ACCESS_KEY_ID
            AWS_SECRET_ACCESS_KEY= settings.AWS_SECRET_ACCESS_KEY
            bucket_name = settings.AWS_STORAGE_BUCKET_NAME
            session = boto3.Session(aws_access_key_id=AWS_SERVER_PUBLIC_KEY,\
                                    aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
            s3 = session.resource('s3')


            obj = s3.Object(bucket_name, '/tmp/logs.log')
            file_content = obj.get()['Body'].read()
            file_content += ("\n" + (post_data.get("data",None)) +" " + str(datetime.datetime.now())).encode()

            print (file_content)

            s3.Object('django-static-uwinfundme', '/tmp/logs.log').put(Body=file_content)
            return Response({"Success":"Log updated"},status = 200)
