import base58
import json
import os
from dotenv import load_dotenv

class SolanaKeyConverter:
    def __init__(self, env_path=None):
        """
        Initialize the converter with an optional custom .env path
        """
        if env_path is None:
            env_path = os.path.join(os.path.dirname(__file__), '../.env')
        
        self.load_environment(env_path)
        self.private_key = None
        self.private_key_array = None

    def load_environment(self, env_path):
        """
        Load environment variables from the specified .env file
        """
        if not load_dotenv(dotenv_path=env_path):
            raise ValueError(f"Could not load .env file at {env_path}")
        
        self.base58_private_key = os.getenv("WALLET_PRIVATE_KEY")
        if self.base58_private_key is None:
            raise ValueError("WALLET_PRIVATE_KEY not found in the .env file.")

    def convert_key(self):
        """
        Convert the Base58 private key to byte array
        """
        decoded_bytes = base58.b58decode(self.base58_private_key)
        self.private_key_array = list(decoded_bytes)
        return self.private_key_array

    def save_to_json(self, output_path="solana_keypair.json"):
        """
        Save the converted key array to a JSON file
        """
        if self.private_key_array is None:
            self.convert_key()
            
        with open(output_path, "w") as json_file:
            json.dump(self.private_key_array, json_file)
        return output_path

    def process_and_save(self, output_path="solana_keypair.json"):
        """
        Convenience method to convert and save in one step
        """
        self.convert_key()
        saved_path = self.save_to_json(output_path)
        return {
            "private_key_array": self.private_key_array,
            "saved_path": saved_path
        }

if __name__ == "__main__":
    try:
        converter = SolanaKeyConverter()
        result = converter.process_and_save()
        print(f"Private key in JSON format: {result['private_key_array']}")
        print(f"Saved to {result['saved_path']}")
    except Exception as e:
        print(f"Error: {str(e)}")