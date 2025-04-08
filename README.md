# Google Cloud Run Image Download and Upload Function

This Cloud Run function downloads an image from a specified URL and uploads it to a Google Cloud Storage bucket using Application Default Credentials for authentication. Each time the function is triggered, it downloads the same image and uploads it with a unique timestamp-based filename.

## Prerequisites

- Google Cloud account with billing enabled
- Google Cloud CLI (`gcloud`) installed
- Python 3.7 or higher
- A Google Cloud Storage bucket

## Setup Instructions

### 1. Set Up Application Default Credentials (ADC)

Application Default Credentials provide a way to authenticate to Google Cloud services without explicitly including credentials in your code.

#### Local Development

For local development and testing:

```bash
# Login with your Google account
gcloud auth login

# Set up application default credentials
gcloud auth application-default login
```

This creates a credentials file at:
- Linux/macOS: `~/.config/gcloud/application_default_credentials.json`
- Windows: `%APPDATA%\gcloud\application_default_credentials.json`

#### Production Deployment

When deployed to Cloud Run, the service automatically uses the service account assigned to it. Make sure this service account has the necessary permissions:

- `roles/storage.objectAdmin` for the target bucket

You can set this with:

```bash
# Replace with your service account and bucket name
gcloud storage buckets add-iam-policy-binding gs://YOUR_BUCKET_NAME \
  --member=serviceAccount:YOUR_SERVICE_ACCOUNT@YOUR_PROJECT.iam.gserviceaccount.com \
  --role=roles/storage.objectAdmin
```

### 2. Configure Your Project

1. Update the `.env.yaml` file with your bucket name:

```yaml
BUCKET_NAME: "your-actual-bucket-name"
```

2. Make sure your bucket exists:

```bash
# Create a bucket if it doesn't exist
gcloud storage buckets create gs://your-bucket-name --location=us-central1
```

### 3. Deploy to Cloud Run

You can deploy the function using the provided `deploy.sh` script, which simplifies the deployment process:

```bash
# Make sure the script is executable
chmod +x deploy.sh

# Deploy with default settings (us-central1 region and image-upload-service name)
./deploy.sh YOUR_PROJECT_ID

# Or specify a different region
./deploy.sh YOUR_PROJECT_ID us-east1

# Or specify both region and service name
./deploy.sh YOUR_PROJECT_ID us-east1 my-custom-service-name
```

The script accepts the following parameters:
1. **Project ID** (required): Your Google Cloud project ID
2. **Region** (optional, defaults to us-central1): The region to deploy to
3. **Service Name** (optional, defaults to image-upload-service): The name for your Cloud Run service

The script will:
1. Confirm your deployment settings
2. Set the active Google Cloud project
3. Deploy the service to Cloud Run
4. Display the service URL and a sample command to test it

If you prefer to deploy manually, you can use the standard gcloud command:

```bash
# Set your project ID
gcloud config set project YOUR_PROJECT_ID

# Deploy the function
gcloud run deploy image-upload-service \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --env-vars-file .env.yaml
```

If you want to require authentication for the service, remove the `--allow-unauthenticated` flag.

### 4. Test the Function

You can test the deployed function using a simple HTTP request:

```bash
# Replace with your actual Cloud Run URL
CLOUD_RUN_URL=$(gcloud run services describe image-upload-service --platform managed --region us-central1 --format 'value(status.url)')

# Trigger the function (works with either GET or POST)
curl $CLOUD_RUN_URL
```

Or using Python:

```python
import requests

# Replace with your actual Cloud Run URL
url = "https://your-cloud-run-url"

response = requests.get(url)
print(response.json())
```

## Local Development

To run the service locally:

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Set environment variables:

```bash
export BUCKET_NAME="your-bucket-name"
```

3. Run the application:

```bash
python main.py
```

The service will be available at http://localhost:8080

4. Test it with a simple request:

```bash
curl http://localhost:8080
```

## Understanding the Code

- `main.py`: Contains the Cloud Run function that downloads an image from a URL and uploads it to GCS
- `requirements.txt`: Lists the Python dependencies
- `.env.yaml`: Contains environment variables for the Cloud Run service

## Troubleshooting

### Authentication Issues

If you encounter authentication errors:

1. Verify your Application Default Credentials are set up correctly:
   ```bash
   gcloud auth application-default print-access-token
   ```

2. Check that your service account has the correct permissions on the bucket.

3. For local testing, make sure you've run `gcloud auth application-default login`.

### Upload Issues

If uploads fail:

1. Check that your bucket exists and is accessible.
2. Verify that the image URL is accessible and the image can be downloaded.
3. Check the Cloud Run logs for detailed error messages:
   ```bash
   gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=image-upload-service" --limit 10
