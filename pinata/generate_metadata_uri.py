import os
from pathlib import Path
from pinata.resize_image import ImageResizer
from pinata.upload_image_to_pinata_ifps import PinataIPFSUploader
from pinata.generate_metadata_json import MetadataJSONGenerator
from pinata.upload_metadata_uri_to_pinata_ifps import PinataJSONUploader

class PinataUploader:
    def __init__(self, image_path, json_path):
        """
        Initialize the uploader with paths for image and JSON
        """
        self.image_path = image_path
        self.json_path = json_path
        self.resized_image_path = self._get_resized_path(image_path)

    def _get_resized_path(self, original_path):
        """Create path for resized image"""
        path = Path(original_path)
        return str(path.parent / f"resized_{path.name}")

    def process(self):
        """
        Main orchestration method to handle the entire upload process
        """
        try:
            # 1. Resize the image
            print("\nResizing image...")
            resizer = ImageResizer(self.image_path, self.resized_image_path)
            resizer.process()

            # 2. Upload resized image to IPFS
            print("\nUploading image to IPFS...")
            image_uploader = PinataIPFSUploader()
            image_result = image_uploader.pin_file_to_ipfs(self.resized_image_path)
            print(f"Image Gateway URL: {image_result['gateway_url']}")

            # 3. Update JSON with image gateway URL
            print("\nUpdating metadata JSON...")
            json_generator = MetadataJSONGenerator(self.json_path, image_result['gateway_url'])
            updated_json = json_generator.add_image_attribute()
            print("Metadata JSON updated successfully")

            # 4. Upload updated JSON to IPFS
            print("\nUploading metadata to IPFS...")
            json_uploader = PinataJSONUploader()
            metadata_result = json_uploader.pin_json_to_ipfs(self.json_path)
            
            # 5. Clean up resized image
            if os.path.exists(self.resized_image_path):
                os.remove(self.resized_image_path)

            return {
                'image_ipfs_hash': image_result['IpfsHash'],
                'image_gateway_url': image_result['gateway_url'],
                'metadata_ipfs_hash': metadata_result['IpfsHash'],
                'metadata_gateway_url': metadata_result['gateway_url'],
                'metadata_ipfs_url': metadata_result['ipfs_url']
            }

        except Exception as e:
            print(f"Error in upload process: {str(e)}")
            # Clean up resized image if it exists
            if os.path.exists(self.resized_image_path):
                os.remove(self.resized_image_path)
            raise

if __name__ == "__main__":
    # Define your paths here
    image_path = "token_metadata/sampletoken1_image.jpeg"
    json_path = "token_metadata/sampletoken1.json"

    try:
        uploader = PinataUploader(image_path, json_path)
        result = uploader.process()
        
        print("\nProcess completed successfully!")
        print(f"Image IPFS Hash: {result['image_ipfs_hash']}")
        print(f"Image Gateway URL: {result['image_gateway_url']}")
        print(f"Metadata IPFS Hash: {result['metadata_ipfs_hash']}")
        print(f"Metadata Gateway URL: {result['metadata_gateway_url']}")
        print(f"Metadata IPFS URL: {result['metadata_ipfs_url']}")
        
    except Exception as e:
        print(f"Error: {str(e)}")