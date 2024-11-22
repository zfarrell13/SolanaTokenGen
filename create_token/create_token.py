import subprocess
import os
import glob
import time


class SolanaMainnetScriptRunner:
    def __init__(self):
        self.root_directory = os.getcwd()
        self.wallet_address = None
        self.to_file = None

    def run_command(self, command):
        try:
            result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print(result.stdout)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Error while executing command: {command}")
            print(e.stderr)
            raise

    def set_solana_config(self):
        print("Setting Solana configuration to mainnet-beta...")
        self.run_command("solana config set --url https://api.mainnet-beta.solana.com -k solana_keypair.json")

    def get_wallet_address(self):
        print("Retrieving wallet address...")
        self.wallet_address = self.run_command("solana address")
        if not self.wallet_address:
            raise ValueError("Failed to retrieve wallet address.")
        print(f"Wallet address: {self.wallet_address}")

    def generate_to_keypair(self):
        print("Generating keypair starting with To...")
        self.run_command("solana-keygen grind --starts-with To:1")

        # Find the generated file in the root directory
        json_file = glob.glob(os.path.join(self.root_directory, "To*.json"))
        if not json_file:
            raise FileNotFoundError("No JSON file found starting with 'To' in the root directory.")
        self.to_file = os.path.basename(json_file[0])
        print(f"Generated file: {self.to_file}")

    def create_spl_token(self):
        print(f"Creating SPL token with file: {os.path.splitext(self.to_file)[0]}")
        retries = 5
        for attempt in range(1, retries + 1):
            try:
                self.run_command(
                    f"spl-token --program-id TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb create-token "
                    f"--enable-metadata {self.to_file}"
                )
                print("SPL token creation succeeded!")
                break
            except subprocess.CalledProcessError as e:
                error_message = e.stderr.strip()
                if "account Address" in error_message and "already in use" in error_message:
                    print("SPL token account already exists. Proceeding with the next steps.")
                    break
                print(f"SPL token creation attempt {attempt} failed. Retrying in 5 seconds...")
                if attempt < retries:
                    time.sleep(5)
                else:
                    print("SPL token creation failed after 5 attempts.")
                    raise

    def create_token_account(self):
        print(f"Creating token account for file: {os.path.splitext(self.to_file)[0]}")
        retries = 5
        for attempt in range(1, retries + 1):
            try:
                # Attempt to create the token account
                self.run_command(f"spl-token create-account {os.path.splitext(self.to_file)[0]}")
                print("Token account creation succeeded!")
                break
            except subprocess.CalledProcessError as e:
                error_message = e.stderr.strip()  # Capture the error message
                if "Error: Account already exists:" in error_message:
                    # Extract the account number from the error message
                    account_number = error_message.split(":")[-1].strip()
                    print("Token account creation succeeded!")
                    print(f"Token Account: {account_number}")
                    break
                print(f"Token account creation attempt {attempt} failed. Retrying in 5 seconds...")
                if attempt < retries:
                    time.sleep(5)
                else:
                    print("Token account creation failed after 5 attempts.")
                    raise
                
    def run(self):
        self.set_solana_config()
        self.get_wallet_address()
        self.generate_to_keypair()
        self.create_spl_token()
        self.create_token_account()


if __name__ == "__main__":
    runner = SolanaMainnetScriptRunner()
    runner.run()
