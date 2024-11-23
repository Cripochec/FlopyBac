import logging

import boto3
from botocore.exceptions import NoCredentialsError


# Настройка логирования
logging.basicConfig(
    filename='LOGGING.log',
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s'
)


def log_error(route_name, error):
    logging.error(f'S3, API.py ({route_name}): {error}')


def delete_photo_from_s3(object_name):
    try:
        # Создание клиента S3
        bucket_name = 'flopy-folder'

        s3_client = boto3.client(
            's3',
            endpoint_url='https://storage.yandexcloud.net',
            aws_access_key_id='YCAJESYKeslrDhzmpCLJMfShP',
            aws_secret_access_key='YCMQ8fFvl0Zu1sosm15WzsAUgRvSLZIU_lAU8een',
            region_name='ru-central1'
        )

        # Удаление файла из S3
        s3_client.delete_object(Bucket=bucket_name, Key=object_name)

    except Exception as e:
        log_error("delete_photo_from_s3", e)


def upload_photo_to_s3(photo_data, object_name):
    try:
        # Создание клиента S3
        bucket_name = 'flopy-folder'

        s3_client = boto3.client(
            's3',
            endpoint_url='https://storage.yandexcloud.net',
            aws_access_key_id='YCAJESYKeslrDhzmpCLJMfShP',
            aws_secret_access_key='YCMQ8fFvl0Zu1sosm15WzsAUgRvSLZIU_lAU8een',
            region_name='ru-central1'
        )

        # Преобразуем данные изображения в поток
        from io import BytesIO
        image_stream = BytesIO(photo_data)

        # Загрузка файла в S3
        s3_client.upload_fileobj(image_stream, bucket_name, object_name)

    except Exception as e:
        log_error("upload_photo_to_s3", e)


def get_photo_url(object_name):
    try:
        # Формирование URL
        url = f"https://flopy-folder.storage.yandexcloud.net/{object_name}"
        return url

    except Exception as e:
        log_error(delete_photo_from_s3, e)
