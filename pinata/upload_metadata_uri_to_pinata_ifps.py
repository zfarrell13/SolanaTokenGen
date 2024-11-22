import os
import json
import requests
from dotenv import load_dotenv
from pathlib import Path

class PinataJSONUploader:
    def __init__(self):
        """
        Initialize the uploader with the JWT from parent directory's .env file
        """
        self.load_environment()
        self.api_endpoint = "https://api.pinata.cloud/pinning/pinJSONToIPFS"

    def load_environment(self):
        """
        Load Pinata JWT from environment variables in parent directory
        """
        load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../.env"))
        self.JWT = os.getenv("YOUR_PINATA_JWT")
        
        if not self.JWT:
            raise ValueError("Pinata JWT not found in .env file")

    def pin_json_to_ipfs(self, json_path):
        """
        Upload and pin a JSON file to IPFS via Pinata
        
        Args:
            json_path (str): Path to the JSON file to upload
            
        Returns:
            dict: Response from Pinata API containing IPFS details
        """
        if not os.path.exists(json_path):
            raise FileNotFoundError(f"JSON file not found at {json_path}")

        # Get the filename from the path
        file_name = Path(json_path).name

        # Read and parse the JSON file
        try:
            with open(json_path, 'r') as file:
                json_content = json.load(file)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON file")

        payload = {
            "pinataOptions": {
                "cidVersion": 1
            },
            "pinataMetadata": {
                "name": file_name
            },
            "pinataContent": json_content
        }

        headers = {
            "Authorization": f"Bearer {self.JWT}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(
                self.api_endpoint,
                json=payload,
                headers=headers
            )
            
            response.raise_for_status()
            result = response.json()
            
            # Add gateway URLs to the response
            result['gateway_url'] = f"https://gateway.pinata.cloud/ipfs/{result['IpfsHash']}"
            result['ipfs_url'] = f"ipfs://{result['IpfsHash']}"
            
            return result

        except requests.exceptions.RequestException as e:
            print(f"Error uploading to Pinata: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response: {e.response.text}")
            raise

if __name__ == "__main__":
    try:
        # Define your JSON path directly here
        json_path = "token_metadata/sampletoken1.json"  # Replace with your actual path
        
        uploader = PinataJSONUploader()
        result = uploader.pin_json_to_ipfs(json_path)
        
        print("\nJSON successfully pinned to IPFS!")
        print(f"File name: {Path(json_path).name}")
        print(f"IPFS Hash: {result['IpfsHash']}")
        print(f"Gateway URL: {result['gateway_url']}")
        print(f"IPFS URL: {result['ipfs_url']}")
        
    except Exception as e:
        print(f"Error: {str(e)}")