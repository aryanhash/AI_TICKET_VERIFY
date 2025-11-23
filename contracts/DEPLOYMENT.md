# NFT Ticket Contract Deployment Guide

## Prerequisites

1. **MetaMask** installed with QIE Network configured
2. **QIE tokens** for gas fees
3. **Remix IDE** or **Hardhat** for deployment

## QIE Network Configuration

### Add QIE Network to MetaMask:

```
Network Name: QIE Mainnet
RPC URL: https://rpc-mainnet.qie.digital
Chain ID: 5656
Currency Symbol: QIE
Block Explorer: https://mainnet.qie.digital
```

## Deployment Options

### Option 1: Using Remix IDE (Recommended for Beginners)

1. Go to [Remix IDE](https://remix.ethereum.org)

2. Create a new file `NFTTicket.sol` and paste the contract code

3. Install OpenZeppelin contracts:
   - In Remix, use the Plugin Manager to install "OpenZeppelin"
   - Or manually import via GitHub

4. Compile:
   - Select Solidity Compiler 0.8.20+
   - Click "Compile NFTTicket.sol"

5. Deploy:
   - Go to "Deploy & Run Transactions"
   - Environment: "Injected Provider - MetaMask"
   - Ensure MetaMask is on QIE Network (Chain ID 5656)
   - Click "Deploy"
   - Confirm transaction in MetaMask

6. Copy the deployed contract address

### Option 2: Using Hardhat

1. Install dependencies:
```bash
npm install --save-dev hardhat @openzeppelin/contracts
npx hardhat init
```

2. Configure `hardhat.config.js`:
```javascript
require("@nomicfoundation/hardhat-toolbox");

const PRIVATE_KEY = "YOUR_PRIVATE_KEY_HERE";

module.exports = {
  solidity: "0.8.20",
  networks: {
    qie: {
      url: "https://rpc-mainnet.qie.digital",
      chainId: 5656,
      accounts: [PRIVATE_KEY]
    }
  }
};
```

3. Create deployment script `scripts/deploy.js`:
```javascript
const hre = require("hardhat");

async function main() {
  const NFTTicket = await hre.ethers.getContractFactory("NFTTicket");
  const nftTicket = await NFTTicket.deploy();
  
  await nftTicket.waitForDeployment();
  
  const address = await nftTicket.getAddress();
  console.log("NFTTicket deployed to:", address);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
```

4. Deploy:
```bash
npx hardhat run scripts/deploy.js --network qie
```

## After Deployment

1. **Copy the contract address**

2. **Set environment variable** in your backend:
```
NFT_CONTRACT_ADDRESS=0xYourContractAddress
ORGANIZER_PRIVATE_KEY=YourPrivateKey
```

3. **Verify contract** (optional but recommended):
   - Use QIE block explorer verification tool
   - Or Hardhat verify plugin

## Contract ABI

The ABI is automatically generated during compilation. Key functions:

```javascript
// Mint NFT ticket
mint(address to, string memory uri) returns (uint256)

// Get token URI
tokenURI(uint256 tokenId) returns (string memory)

// Get owner of token
ownerOf(uint256 tokenId) returns (address)

// Get token balance
balanceOf(address owner) returns (uint256)

// Get total supply
totalSupply() returns (uint256)
```

## Security Notes

1. **NEVER** commit private keys to version control
2. Store `ORGANIZER_PRIVATE_KEY` as a secret in Replit
3. Only the contract owner (deployer) can mint tickets
4. Consider using a multi-sig wallet for production

## Testing

Before mainnet deployment, test on:
- QIE Testnet (if available)
- Local Hardhat network
- Fork of QIE mainnet

## Cost Estimation

Deployment on QIE is significantly cheaper than Ethereum:
- Contract Deployment: ~$0.01-1
- Mint per NFT: ~$0.001-0.01

Compare to Ethereum: 100-1000x more expensive!
