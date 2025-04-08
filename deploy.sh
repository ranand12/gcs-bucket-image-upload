#!/bin/bash
# Script to deploy the image upload function to Google Cloud Run

# Exit on error
set -e

# Check if project ID is provided
if [ -z "$1" ]; then
  echo "Usage: ./deploy.sh <project-id> [region] [service-name]"
  echo "Example: ./deploy.sh my-project-id us-central1 image-upload-service"
  exit 1
fi

# Set variables
PROJECT_ID=$1
REGION=${2:-us-central1}
SERVICE_NAME=${3:-image-upload-service}

# Confirm deployment
echo "Deploying to project: $PROJECT_ID"
echo "Region: $REGION"
echo "Service name: $SERVICE_NAME"
echo ""
read -p "Continue? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
  echo "Deployment cancelled."
  exit 1
fi

# Set project
echo "Setting project to $PROJECT_ID..."
gcloud config set project $PROJECT_ID

# Deploy to Cloud Run
echo "Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
  --source . \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --env-vars-file .env.yaml

# Get the URL
URL=$(gcloud run services describe $SERVICE_NAME --platform managed --region $REGION --format 'value(status.url)')

echo ""
echo "Deployment complete!"
echo "Your service is available at: $URL"
echo ""
echo "To test your service, run:"
echo "curl -X POST -F \"image=@/path/to/your/image.jpg\" $URL"
