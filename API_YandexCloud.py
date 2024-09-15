import boto3
from botocore.exceptions import NoCredentialsError


def delete_photo_from_s3(object_name):
    # Создание клиента S3
    bucket_name = 'flopy-folder'

    s3_client = boto3.client(
        's3',
        endpoint_url='https://storage.yandexcloud.net',
        aws_access_key_id='YCAJESYKeslrDhzmpCLJMfShP',
        aws_secret_access_key='YCMQ8fFvl0Zu1sosm15WzsAUgRvSLZIU_lAU8een',
        region_name='ru-central1'
    )

    try:
        # Удаление файла из S3
        s3_client.delete_object(Bucket=bucket_name, Key=object_name)
    except NoCredentialsError:
        print("Указаны неверные учетные данные YandexCloud.")
    except Exception as e:
        print(f"ERROR: YandexCloud, {e}")


def upload_photo_to_s3(photo_data, object_name):
    # Создание клиента S3
    bucket_name = 'flopy-folder'

    s3_client = boto3.client(
        's3',
        endpoint_url='https://storage.yandexcloud.net',
        aws_access_key_id='YCAJESYKeslrDhzmpCLJMfShP',
        aws_secret_access_key='YCMQ8fFvl0Zu1sosm15WzsAUgRvSLZIU_lAU8een',
        region_name='ru-central1'
    )

    try:
        # Преобразуем данные изображения в поток
        from io import BytesIO
        image_stream = BytesIO(photo_data)

        # Загрузка файла в S3
        s3_client.upload_fileobj(image_stream, bucket_name, object_name)

    except FileNotFoundError:
        print(f"Файл для загрузки в Yandex Cloud, {object_name}, не найден.")
    except NoCredentialsError:
        print("Указаны неверные учетные данные Yandex Cloud.")
    except Exception as e:
        print(f"ERROR: YandexCloud, {e}")


def get_photo_url(object_name):
    # Формирование URL
    url = f"https://flopy-folder.storage.yandexcloud.net/{object_name}"
    return url
