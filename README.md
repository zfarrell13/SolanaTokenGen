# SOLTOKENGEN

### Effortlessly Create Your Own Solana Tokens 🌟

**SOLTOKENGEN** makes creating tokens on the Solana mainnet easier than ever. Whether you're building a new project, minting tokens for an NFT series, or experimenting with Solana, this tool helps you generate tokens with custom names, symbols, images, descriptions, and mint amounts. No prior blockchain development experience is required!

With **SOLTOKENGEN**, you can:
- Quickly launch your own Solana token for personal or commercial projects.
- Assign metadata like an image and description to make your token stand out.
- Mint any desired amount of tokens directly to your wallet.

---

## 🛠️ SETUP

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/zfarrell13/SolanaTokenGen.git
   ```
   
2. **Set Up the Python Environment**:
   - Create a Conda environment:
     ```bash
     conda create -n solana python=3.13
     ```
   - Activate the environment:
     ```bash
     conda activate solana
     ```
   - Install dependencies:
     ```bash
     cd SolanaTokenGen
     pip install -r requirements.txt
     ```

3. **Prepare the Environment Variables**:
   - Rename `.env_template` to `.env`:
     ```bash
     mv .env_template .env
     ```
   - **Create a Solana Wallet** if you don’t already have one:
     - Use a Solana wallet provider (e.g., Phantom or Sollet).
   - **Fund Your Wallet** with a small amount of SOL for transaction fees.
   - Get the **private key** of your wallet and place it in `.env` under `WALLET_PRIVATE_KEY`.

4. **Set Up Pinata for Metadata Hosting**:
   - Sign up for a free [Pinata](https://www.pinata.cloud/) account.
   - Generate an API key and place it in `.env` under `YOUR_PINATA_JWT`.

---

## 🚀 USAGE

Run the script to create your token on the Solana mainnet. The command syntax is as follows:

```bash
python main.py --help
```

### Command Options:
```text
usage: main.py [-h] name symbol image_path mint_amount description

Create a Solana token with metadata

positional arguments:
  name         Token name -- eg. "SPT" (in quotes, it has to be one word, no spaces)
  symbol       Token symbol -- eg. "SampleToken" (in quotes, it has to be one word, no spaces)
  image_path   Path to the token image -- eg. "/path/to/sampletoken_image.jpeg" (in quotes, no spaces)
  mint_amount  Amount of tokens to mint -- eg. 1000000 (integer)
  description  Token description -- eg. "This is a test token" (in quotes)

options:
  -h, --help   show this help message and exit
```

### Example:
To create a token named **Sampletoken1** with the symbol **S1**, a specified image, a mint amount of 1,000,000, and a description:

```bash
python main.py "Sampletoken1" "S1" "path/to/sampletoken1_image.jpeg" 1000000 "This is a test token"
```

---

## 🎉 What’s Next?

Now that you’ve created your token, here are a few things you can do:
- **List Your Token** on Solana marketplaces or use it within decentralized applications (DApps).
- **Build Applications** that interact with your token, such as reward systems, voting mechanisms, or in-game assets.
- **Create NFTs** or use the token as part of your NFT collections.
- **Experiment and Learn** about Solana and tokenomics while developing your blockchain expertise!

Let **SOLTOKENGEN** help bring your ideas to life on the Solana blockchain! 🚀✨
