import subprocess
import os
import glob
import json
import time


class AddTokenMetadata:
    def __init__(self, token_metadata_path, metadata_gateway_url, mint_amount):
        self.root_directory = os.getcwd()
        self.to_file = None
        self.token_metadata_path = token_metadata_path
        self.metadata_gateway_url = metadata_gateway_url
        self.mint_amount = mint_amount
        self.name = None
        self.symbol = None
        self.uri = metadata_gateway_url

    def run_command(self, command):
        try:
            result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print(result.stdout)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Error while executing command: {command}")
            print(e.stderr)
            raise

    def find_to_file(self):
        print("Finding JSON file starting with 'To'...")
        json_file = glob.glob(os.path.join(self.root_directory, "To*.json"))
        if not json_file:
            raise FileNotFoundError("No JSON file found starting with 'To' in the root directory.")
        self.to_file = os.path.splitext(os.path.basename(json_file[0]))[0]
        print(f"Found file: {self.to_file}")

    def load_metadata(self):
        print(f"Loading metadata from: {self.token_metadata_path}")
        if not os.path.exists(self.token_metadata_path):
            raise FileNotFoundError(f"Token metadata file not found at {self.token_metadata_path}")
        with open(self.token_metadata_path, 'r') as file:
            metadata = json.load(file)
        self.name = metadata["name"]
        self.symbol = metadata["symbol"]
        print(f"Loaded metadata: name={self.name}, symbol={self.symbol}")

    def initialize_metadata(self):
        print(f"Initializing metadata for token: {self.to_file}")
        retries = 10
        for attempt in range(1, retries + 1):
            try:
                self.run_command(
                    f"spl-token initialize-metadata {self.to_file} {self.name} {self.symbol} {self.uri}"
                )
                print("Metadata initialization succeeded!")
                break
            except subprocess.CalledProcessError as e:
                error_message = e.stderr.strip()
                if "Error: Extension already initialized on this account" in error_message:
                    print("Metadata already initialized. Proceeding with the next steps.")
                    break
                print(f"Metadata initialization attempt {attempt} failed. Retrying in 5 seconds...")
                if attempt < retries:
                    time.sleep(5)
                else:
                    print("Metadata initialization failed after 5 attempts.")
                    raise


    def update_metadata_name(self):
        print(f"Updating metadata field: name with value: {self.name}")
        retries = 5
        for attempt in range(1, retries + 1):
            try:
                self.run_command(
                    f"spl-token update-metadata {self.to_file} name {self.name}"
                )
                print("Metadata field 'name' updated successfully!")
                break
            except subprocess.CalledProcessError:
                print(f"Updating metadata field 'name' attempt {attempt} failed. Retrying in 2 seconds...")
                if attempt < retries:
                    time.sleep(2)
                else:
                    print("Updating metadata field 'name' failed after 5 attempts.")
                    raise

    def update_metadata_symbol(self):
        print(f"Updating metadata field: symbol with value: {self.symbol}")
        retries = 5
        for attempt in range(1, retries + 1):
            try:
                self.run_command(
                    f"spl-token update-metadata {self.to_file} symbol {self.symbol}"
                )
                print("Metadata field 'symbol' updated successfully!")
                break
            except subprocess.CalledProcessError:
                print(f"Updating metadata field 'symbol' attempt {attempt} failed. Retrying in 2 seconds...")
                if attempt < retries:
                    time.sleep(2)
                else:
                    print("Updating metadata field 'symbol' failed after 5 attempts.")
                    raise

    def update_metadata_uri(self):
        print(f"Updating metadata field: uri with value: {self.uri}")
        retries = 5
        for attempt in range(1, retries + 1):
            try:
                self.run_command(
                    f"spl-token update-metadata {self.to_file} uri {self.uri}"
                )
                print("Metadata field 'uri' updated successfully!")
                break
            except subprocess.CalledProcessError:
                print(f"Updating metadata field 'uri' attempt {attempt} failed. Retrying in 2 seconds...")
                if attempt < retries:
                    time.sleep(2)
                else:
                    print("Updating metadata field 'uri' failed after 5 attempts.")
                    raise

    def mint_tokens(self):
        print(f"Minting {self.mint_amount} tokens for: {self.to_file}")
        retries = 10
        for attempt in range(1, retries + 1):
            try:
                self.run_command(
                    f"spl-token mint {self.to_file} {self.mint_amount}"
                )
                print(f"Minted {self.mint_amount} tokens successfully!")
                break
            except subprocess.CalledProcessError:
                print(f"Minting attempt {attempt} failed. Retrying in 5 seconds...")
                if attempt < retries:
                    time.sleep(5)
                else:
                    print("Minting failed after 5 attempts.")
                    raise



    def run(self):
        self.find_to_file()
        self.load_metadata()
        self.initialize_metadata()
        self.update_metadata_name()
        self.update_metadata_symbol()
        self.update_metadata_uri()
        self.mint_tokens()


if __name__ == "__main__":
    # Define paths and parameters here
    token_metadata_path = "./token_metadata/sampletoken1.json"
    metadata_gateway_url = "https://gateway.pinata.cloud/ipfs/bafkreicbaacs5bal2zhtv7t4t73mbyw2bevq4evb55fxtcepftj7pv7asi"
    mint_amount = 1000000

    runner = AddTokenMetadata(token_metadata_path, metadata_gateway_url, mint_amount)
    runner.run()
