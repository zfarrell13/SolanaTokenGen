import os
import json
import shutil
import argparse
from pathlib import Path
from datetime import datetime
from utils.convert_base58 import SolanaKeyConverter
from pinata.generate_metadata_uri import PinataUploader
from create_token.create_token import SolanaMainnetScriptRunner
from create_token.add_token_metadata import AddTokenMetadata


class MainScript:
    def __init__(self, image_path, name, symbol, description, mint_amount):
        self.image_path = image_path
        self.name = name
        self.symbol = symbol
        self.description = description
        self.mint_amount = mint_amount
        self.metadata_gateway_url = None
        self.json_path = self.create_metadata_json()
        self.token_metadata_path = f"./{self.json_path}"
        self.to_file_path = None
        self.artifact_dir = self.setup_artifact_directory()

    def setup_artifact_directory(self):
        """
        Create an artifact directory for this execution
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        artifact_dir = os.path.join("artifacts", f"{self.name}_{timestamp}")
        os.makedirs(artifact_dir, exist_ok=True)
        print(f"Created artifact directory: {artifact_dir}")
        return artifact_dir

    def create_metadata_json(self):
        """
        Create a metadata JSON file in the tmp directory with the provided attributes
        """
        tmp_dir = "tmp"
        os.makedirs(tmp_dir, exist_ok=True)

        metadata = {
            "name": self.name,
            "symbol": self.symbol,
            "description": self.description
        }

        json_filename = f"{self.name.lower()}_metadata.json"
        json_path = os.path.join(tmp_dir, json_filename)

        with open(json_path, 'w') as f:
            json.dump(metadata, f, indent=4)

        print(f"Created metadata JSON at: {json_path}")
        return json_path

    def check_or_generate_keypair(self):
        if not os.path.exists("solana_keypair.json"):
            print("solana_keypair.json not found. Generating keypair...")
            converter = SolanaKeyConverter()
            result = converter.process_and_save()
            print(f"Private key in JSON format: {result['private_key_array']}")
            print(f"Saved to {result['saved_path']}")
        else:
            print("solana_keypair.json found.")

    def find_to_file(self):
        """
        Find the To*.json file created by create_token script
        """
        to_files = list(Path(".").glob("To*.json"))
        if to_files:
            self.to_file_path = str(to_files[0])
            print(f"Found To file: {self.to_file_path}")
        else:
            print("Warning: No To*.json file found")

    def generate_metadata_uri(self):
        uploader = PinataUploader(self.image_path, self.json_path)
        result = uploader.process()
        self.metadata_gateway_url = result['metadata_gateway_url']
        print(f"Generated Metadata Gateway URL: {self.metadata_gateway_url}")

    def create_token_and_metadata(self):
        print("Running SolanaMainnetScriptRunner...")
        token_runner = SolanaMainnetScriptRunner()
        token_runner.run()

        self.find_to_file()

        print("Running AddTokenMetadata...")
        metadata_runner = AddTokenMetadata(
            self.token_metadata_path, 
            self.metadata_gateway_url, 
            self.mint_amount
        )
        metadata_runner.run()

    def archive_and_cleanup(self):
        """
        Move files to artifact directory and clean up
        """
        try:
            # Move contents of tmp directory
            tmp_dir = "tmp"
            if os.path.exists(tmp_dir):
                for file_name in os.listdir(tmp_dir):
                    src_path = os.path.join(tmp_dir, file_name)
                    dst_path = os.path.join(self.artifact_dir, file_name)
                    shutil.move(src_path, dst_path)
                os.rmdir(tmp_dir)
                print(f"Moved tmp directory contents to: {self.artifact_dir}")

            # Move To*.json file if it exists
            if self.to_file_path and os.path.exists(self.to_file_path):
                dst_path = os.path.join(self.artifact_dir, os.path.basename(self.to_file_path))
                shutil.move(self.to_file_path, dst_path)
                print(f"Moved {self.to_file_path} to: {self.artifact_dir}")

        except Exception as e:
            print(f"Warning: Error during cleanup: {str(e)}")

    def print_explorer_urls(self):
        """
        Print Solana explorer and Solscan URLs for the token
        """
        if self.to_file_path:
            # Get the To file name without .json extension
            token_address = Path(self.to_file_path).stem  # This gets filename without extension
            
            print("\nToken Explorer URLs:")
            print(f"Solana Explorer: https://explorer.solana.com/address/{token_address}")
            print(f"Solscan: https://solscan.io/token/{token_address}")

    def run(self):
        """
        Orchestrate all the tasks.
        """
        try:
            self.check_or_generate_keypair()
            self.generate_metadata_uri()
            self.create_token_and_metadata()
        finally:
            self.archive_and_cleanup()
            self.print_explorer_urls()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create a Solana token with metadata')
    parser.add_argument('name', type=str, help='Token name -- eg. "SPT" (in quotes, it has to be one word, no spaces)')
    parser.add_argument('symbol', type=str, help='Token symbol -- eg. "SampleToken" (in quotes, it has to be one word, no spaces)')
    parser.add_argument('image_path', type=str, help='Path to the token image -- eg. "/path/to/sampletoken_image.jpeg" (in quotes, no spaces)')
    parser.add_argument('mint_amount', type=int, help='Amount of tokens to mint -- eg. 1000000 (integer)')
    parser.add_argument('description', type=str, help='TToken description -- eg. "This is a test token" (in quotes)')

    args = parser.parse_args()

    # Instantiate and run the script with command line arguments
    script = MainScript(
        image_path=args.image_path,
        name=args.name,
        symbol=args.symbol,
        description=args.description,
        mint_amount=args.mint_amount
    )
    script.run()