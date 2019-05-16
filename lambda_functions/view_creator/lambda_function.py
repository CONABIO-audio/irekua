import json
import os
import mimetypes
from urllib import parse
import boto3
import io

from views import create_view


BASE_PATH = 'media/items/'
BUCKET_NAME = 'irekua-test'


def lambda_handler(event, context):
    filename = extract_filename(event)
    database_info = extract_metadata_info(filename)

    item_file = get_file(filename)
    create_view(item_file, database_info)


def extract_filename(event):
    object = event['Records'][0]['s3']['object']

    return parse.unquote_plus(object['key'])


def extract_metadata_info(filename):
    relative_path = os.path.relpath(filename, BASE_PATH)
    collection, sampling_event, device, basename = relative_path.split('/')
    hash_string, ext = os.path.splitext(basename)

    item_type = get_item_type(filename)

    return {
        'hash': hash_string,
        'collection': collection,
        'sampling_event': sampling_event,
        'device': device,
        'item_type': item_type
    }


def get_item_type(filename):
    mimetypes.init()
    item_type, _ = mimetypes.guess_type(filename)
    return item_type


def get_file(filename):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(BUCKET_NAME)

    basename = os.path.basename(filename)
    item_file = io.BytesIO()

    bucket.download_fileobj(filename, item_file)
    return item_file
