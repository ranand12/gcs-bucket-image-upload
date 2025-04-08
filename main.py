import os
import tempfile
import requests
from datetime import datetime
from flask import Flask, jsonify
from google.cloud import storage

app = Flask(__name__)

# Configure this to your GCS bucket
BUCKET_NAME = os.environ.get('BUCKET_NAME', 'your-bucket-name')

# URL of the image to download
IMAGE_URL = "https://upload.wikimedia.org/wikipedia/commons/5/51/Google_Cloud_logo.svg"

@app.route('/', methods=['GET', 'POST'])
def upload_image():
    """
    Cloud Run function to download an image from a URL and upload it to Google Cloud Storage.
    This function is triggered by any HTTP request (GET or POST).
    """
    try:
        # Download the image from the URL
        response = requests.get(IMAGE_URL)
        if response.status_code != 200:
            return jsonify({
                'success': False,
                'error': f'Failed to download image from URL. Status code: {response.status_code}'
            }), 500
        
        # Create a temporary file to store the downloaded image
        with tempfile.NamedTemporaryFile(delete=False) as temp:
            temp.write(response.content)
            temp_name = temp.name
        
        # Generate a unique filename using timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"google_cloud_logo_{timestamp}.svg"
        
        # Initialize GCS client (uses Application Default Credentials)
        storage_client = storage.Client()
        bucket = storage_client.bucket(BUCKET_NAME)
        
        # Define the path in the bucket where the file will be uploaded
        destination_blob_name = f"uploads/{filename}"
        blob = bucket.blob(destination_blob_name)
        
        # Upload the file
        blob.upload_from_filename(temp_name)
        
        # Create a publicly accessible URL if the bucket permissions allow it
        # Note: This requires the bucket to have appropriate IAM permissions
        url = f"gs://{BUCKET_NAME}/{destination_blob_name}"
        
        # Clean up the temporary file
        os.unlink(temp_name)
        
        return jsonify({
            'success': True,
            'message': f'File {filename} uploaded successfully',
            'url': url,
            'timestamp': timestamp
        }), 200
    
    except Exception as e:
        # Clean up the temporary file in case of error
        if 'temp_name' in locals() and os.path.exists(temp_name):
            os.unlink(temp_name)
        
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == "__main__":
    # This is used when running locally only. When deploying to Cloud Run,
    # a webserver process such as Gunicorn will serve the app.
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
