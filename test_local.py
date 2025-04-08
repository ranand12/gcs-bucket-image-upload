#!/usr/bin/env python3
"""
Test script for the Cloud Run function that downloads an image from a URL and uploads it to GCS.
This script triggers the function running locally.
"""

import requests
import sys

def trigger_function(url="http://localhost:8080"):
    """
    Trigger the Cloud Run function.
    
    Args:
        url (str): URL of the Cloud Run function
        
    Returns:
        dict: Response from the server
    """
    try:
        # The function accepts both GET and POST requests
        response = requests.get(url)
            
        if response.status_code == 200:
            print("Function executed successfully!")
            return response.json()
        else:
            print(f"Function execution failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"Error triggering function: {str(e)}")
        return None

if __name__ == "__main__":
    # Optional command-line argument for the URL
    url = "http://localhost:8080"
    if len(sys.argv) > 1:
        url = sys.argv[1]
    
    print(f"Triggering function at: {url}")
    result = trigger_function(url)
    
    if result:
        print("\nResponse details:")
        for key, value in result.items():
            print(f"{key}: {value}")
