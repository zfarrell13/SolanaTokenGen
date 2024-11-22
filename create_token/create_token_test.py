import subprocess
import os
import glob
import time


class SolanaScriptRunner:
    def __init__(self):
        self.root_directory = os.getcwd()
        self.me_file = None
        self.to_file = None

    def run_command(self, command):
        try:
            result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print(result.stdout)
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"Error while executing command: {command}")
            print(e.stderr)
            raise

    def generate_keypair(self, prefix):
        print(f"Generating keypair starting with {prefix}...")
        self.run_command(f"solana-keygen grind --starts-with {prefix}:1")

        # Find the generated file in the root directory
        json_file = glob.glob(os.path.join(self.root_directory, f"{prefix}*.json"))
        if not json_file:
            raise FileNotFoundError(f"No JSON file found starting with {prefix} in the root directory.")
        print(f"Generated file: {json_file[0]}")
        return os.path.basename(json_file[0])

    def set_solana_config(self):
        print(f"Setting Solana configuration with file: {self.me_file}")
        self.run_command(f"solana config set --url https://api.testnet.solana.com -k {self.me_file}")

    def airdrop_tokens(self):
        print(f"Airdropping 0.01 SOL to account: {os.path.splitext(self.me_file)[0]}")
        retries = 5
        for attempt in range(1, retries + 1):
            try:
                self.run_command(f"solana airdrop 0.01 {os.path.splitext(self.me_file)[0]}")
                print("Airdrop succeeded!")
                break
            except subprocess.CalledProcessError:
                print(f"Airdrop attempt {attempt} failed. Retrying in 2 seconds...")
                if attempt < retries:
                    time.sleep(2)
                else:
                    print("Airdrop failed after 5 attempts.")
                    raise

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
            except subprocess.CalledProcessError:
                print(f"SPL token creation attempt {attempt} failed. Retrying in 2 seconds...")
                if attempt < retries:
                    time.sleep(2)
                else:
                    print("SPL token creation failed after 5 attempts.")
                    raise

    def run(self):
        self.me_file = self.generate_keypair("Me")
        self.to_file = self.generate_keypair("To")
        self.set_solana_config()
        # self.airdrop_tokens()
        self.create_spl_token()


if __name__ == "__main__":
    runner = SolanaScriptRunner()
    runner.run()
