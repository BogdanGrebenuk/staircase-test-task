from collections import namedtuple
from functools import wraps
from http import HTTPStatus
from json import dumps, loads
from uuid import uuid4

from .exception import CallbackUrlIsNotValid


Response = namedtuple('Response', ['body', 'status_code'])


def with_http_api_response_format(function):
    @wraps(function)
    def inner(*args, **kwargs):
        response = function(*args, **kwargs)
        return {
            'isBase64Encoded': False,
            'statusCode': response.status_code,
            'headers': {'Content-Type': 'application/json'},
            'body': dumps(response.body)
        }
    return inner


@with_http_api_response_format
def initialize_upload_listening_handler(
        event, context, initialize_upload_listening
        ):
    blob_id = str(uuid4())
    callback_url = get_callback_url_from_event(event)
    try:
        upload_url = initialize_upload_listening(blob_id, callback_url)
    except CallbackUrlIsNotValid as exception:
        return Response(
            body={
                'description': str(exception),
                'payload': exception.payload
            },
            status_code=HTTPStatus.BAD_REQUEST.value
        )
    return Response(
        body={
            'blob_id': blob_id,
            'callback_url': callback_url,
            'upload_url': upload_url
        },
        status_code=HTTPStatus.CREATED.value
    )


def get_callback_url_from_event(event):
    body = loads(event.get('body'))
    return body.get('callback_url', '').strip()


def check_uploading_handler(event, context, check_uploading):
    blob_id = event.get('blob_id')
    check_uploading(blob_id)


def image_has_been_uploaded_handler(event, context, start_recognition):
    blob_id = get_blob_id_from_event(event)
    start_recognition(blob_id)


def get_blob_id_from_event(event):
    return event.get('Records')[0].get('s3').get('object').get('key')


def get_labels_handler(event, context, get_labels):
    blob_id = event.get('blob_id')
    return get_labels(blob_id)


def transform_labels_handler(event, context, transform_labels):
    blob_id = event.get('blob_id')
    labels = event.get('labels')
    return transform_labels(blob_id, labels)


def save_labels_handler(event, context, save_labels):
    blob_id = event.get('blob_id')
    labels = event.get('labels')
    return save_labels(blob_id, labels)


def invoke_callback_handler(event, context, invoke_callback):
    blob_id = event.get('blob_id')
    labels = event.get('labels')
    return invoke_callback(blob_id, labels)
