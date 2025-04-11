from google.cloud import storage

def upload_to_gcs(bucket_name, source_file_path, destination_blob_name):
    """Uploads a file to Google Cloud Storage"""
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_path)

    print(f" File {source_file_path} uploaded to gs://{bucket_name}/{destination_blob_name}.")

# Example usage
if __name__ == "__main__":
    bucket_name = "your-gcs-bucket-name"
    source_file_path = "path/to/local/file.txt"
    destination_blob_name = "folder-in-bucket/file.txt"  # Or just "file.txt"

    upload_to_gcs(bucket_name, source_file_path, destination_blob_name)
