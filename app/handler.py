"""Module with lambda handlers definition."""

from .container import Container


container = Container()


initialize_upload_listening_handler = container.initialize_upload_listening_handler.handle
check_uploading_handler = container.check_uploading_handler.handle
image_has_been_uploaded_handler = container.image_has_been_uploaded_handler.handle
get_labels_handler = container.get_labels_handler.handle
transform_labels_handler = container.transform_labels_handler.handle
save_labels_handler = container.save_labels_handler.handle
invoke_callback_handler = container.invoke_callback_handler.handle
get_recognition_result_handler = container.get_recognition_result_handler.handle
unexpected_error_fallback_handler = container.unexpected_error_fallback_handler.handle
