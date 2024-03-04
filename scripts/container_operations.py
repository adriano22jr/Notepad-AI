import azure.storage.blob as az_blob
import os, app_config

sa_name = app_config.STORAGE_ACCOUNT_NAME
sa_key = app_config.STORAGE_ACCOUNT_KEY
container_name = app_config.CONTAINER_NAME
CONNECTION_STRING = f"DefaultEndpointsProtocol=https;AccountName={sa_name};AccountKey={sa_key};EndpointSuffix=core.windows.net"


def upload_new_text_blob(filename, content):
    blob_service_client = az_blob.BlobServiceClient.from_connection_string(CONNECTION_STRING)
    blob_client = blob_service_client.get_blob_client(container = container_name, blob = filename)
    
    text_file = open(filename + ".txt", "w")
    text_file.write(content)
    text_file.close()
    
    text_blob = open(filename + ".txt", "rb")
    blob_client.upload_blob(text_blob)
    text_blob.close()
    os.remove(filename + ".txt")
    
def delete_text_blob(filename):
    blob_service_client = az_blob.BlobServiceClient.from_connection_string(CONNECTION_STRING)
    blob_client = blob_service_client.get_blob_client(container = container_name, blob = filename)
    blob_client.delete_blob(delete_snapshots = "include")
    
def update_text_blob(filename, content):
    blob_service_client = az_blob.BlobServiceClient.from_connection_string(CONNECTION_STRING)
    blob_client = blob_service_client.get_blob_client(container = container_name, blob = filename)
    blob_client.upload_blob(content, overwrite = True)