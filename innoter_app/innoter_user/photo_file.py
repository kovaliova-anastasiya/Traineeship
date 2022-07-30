import os
from datetime import datetime
from boto3 import Session
from innoter.settings import AWS_ACCESS_KEY_ID, \
    AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION, \
    BUCKET
from innoter_user.serializers import FileSerializer


def prepare_photo(request):
    photo_serializer = FileSerializer(data=request.FILES)
    photo_serializer.is_valid(raise_exception=True)

    file_extension = os.path.splitext(str(request.FILES['file']))[1]
    filename = datetime.now().strftime("%d-%m-%YT%H:%M:%S") + file_extension

    session = Session(aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                      region_name=AWS_DEFAULT_REGION)
    s3 = session.resource('s3')
    s3.Bucket(BUCKET).put_object(Key=filename, Body=request.FILES['file'])

    filename_data = {'image_s3_path': [filename]}
    return filename_data
