import os
import requests
from dotenv import load_dotenv
from pathlib import Path

class PinataIPFSUploader:
    def __init__(self):
        """
        Initialize the uploader with the JWT from parent directory's .env file
        """
        self.load_environment()
        self.api_endpoint = "https://api.pinata.cloud/pinning/pinFileToIPFS"

    def load_environment(self):
        """
        Load Pinata JWT from environment variables in parent directory
        """
        load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../.env"))
        self.JWT = os.getenv("YOUR_PINATA_JWT")
        
        if not self.JWT:
            raise ValueError("Pinata JWT not found in .env file")

    def pin_file_to_ipfs(self, file_path):
        """
        Upload and pin a file to IPFS via Pinata
        
        Args:
            file_path (str): Path to the file to upload
            
        Returns:
            dict: Response from Pinata API containing IPFS details
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found at {file_path}")

        file_name = Path(file_path).name
        
        files = {
            'file': (file_name, open(file_path, 'rb'))
        }

        headers = {
            "Authorization": f"Bearer {self.JWT}"
        }

        try:
            response = requests.post(
                self.api_endpoint,
                files=files,
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
        finally:
            files['file'][1].close()

if __name__ == "__main__":
    try:
        uploader = PinataIPFSUploader()
        file_path = "token_metadata/sampletoken1_image.jpeg"
        
        result = uploader.pin_file_to_ipfs(file_path)
        
        print("\nFile successfully pinned to IPFS!")
        print(f"IPFS Hash: {result['IpfsHash']}")
        print(f"Gateway URL: {result['gateway_url']}")
        print(f"IPFS URL: {result['ipfs_url']}")
        
    except Exception as e:
        print(f"Error: {str(e)}")