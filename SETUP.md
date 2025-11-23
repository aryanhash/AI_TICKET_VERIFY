# AI-Verified NFT Ticketing System - Setup Guide

This guide will help you set up and deploy the complete NFT ticketing system.

## 📋 Prerequisites

- MetaMask wallet extension installed
- QIE tokens for gas fees
- OpenAI API key (for AI verification)
- Pinata account (optional, for IPFS uploads)
- MongoDB instance (included in Replit)

## 🔑 Step 1: Configure Environment Variables

You need to set the following environment variables in Replit Secrets or create a `.env` file:

### Critical Variables

```env
# OpenAI API Key (Required for AI verification)
OPENAI_API_KEY=sk-your-openai-api-key-here

# QIE Blockchain (Set after contract deployment)
NFT_CONTRACT_ADDRESS=0xYourDeployedContractAddress
ORGANIZER_PRIVATE_KEY=your-wallet-private-key-here

# MongoDB (Default works for local MongoDB)
MONGO_URL=mongodb://localhost:27017/
```

### Optional Variables

```env
# IPFS (Pinata) - If not set, mock hashes will be used
PINATA_JWT=your-pinata-jwt-token
PINATA_API_KEY=your-pinata-api-key
PINATA_SECRET_API_KEY=your-pinata-secret-key

# QIE RPC (Custom endpoint)
QIE_RPC_URL=https://rpc-mainnet.qie.digital

# OpenAI Model (Default: gpt-4o)
OPENAI_MODEL=gpt-4o
```

## 🚀 Step 2: Deploy Smart Contract

### Option A: Using Remix IDE (Recommended)

1. Go to https://remix.ethereum.org

2. Create a new file `NFTTicket.sol` and copy the contract from `contracts/NFTTicket.sol`

3. Install OpenZeppelin dependencies:
   - In Remix Plugin Manager, install "OpenZeppelin"
   - Or use GitHub import: `@openzeppelin/contracts`

4. Compile the contract:
   - Select Solidity Compiler 0.8.20+
   - Click "Compile NFTTicket.sol"

5. Configure MetaMask for QIE Network:
   ```
   Network Name: QIE Blockchain
   RPC URL: https://rpc-mainnet.qie.digital
   Chain ID: 5656
   Currency Symbol: QIE
   Block Explorer: https://mainnet.qie.digital
   ```

6. Deploy:
   - Go to "Deploy & Run Transactions"
   - Environment: "Injected Provider - MetaMask"
   - Ensure MetaMask shows "QIE Blockchain"
   - Click "Deploy"
   - Confirm transaction (costs ~$0.01-1 in QIE)

7. Copy the deployed contract address

### Option B: Using Hardhat

See `contracts/DEPLOYMENT.md` for detailed Hardhat deployment instructions.

## 🔧 Step 3: Configure Application

### Backend Configuration

1. Set environment variables in Replit Secrets:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `NFT_CONTRACT_ADDRESS`: The deployed contract address
   - `ORGANIZER_PRIVATE_KEY`: Your wallet's private key (keep secure!)

2. The backend will start automatically at `http://localhost:8000`

### Frontend Configuration

1. The frontend automatically runs at `http://localhost:5000`

2. No additional configuration needed - it proxies backend requests

## 👤 Step 4: Set Up Organizer Account

After deploying, you need to make your wallet an organizer to create events:

### Method 1: Using curl

```bash
curl -X POST http://localhost:8000/auth/make-organizer/YOUR_WALLET_ADDRESS
```

### Method 2: Using the API docs

1. Go to `http://localhost:8000/docs`
2. Find `POST /auth/make-organizer/{wallet_address}`
3. Enter your wallet address
4. Click "Execute"

## 🎫 Step 5: Create Your First Event

1. Connect your wallet at `http://localhost:5000`
2. Sign the authentication message
3. Go to "Create Event" in the navigation
4. Fill in event details:
   - Title
   - Description
   - Date and time
   - Venue
   - Ticket price (in QIE)
   - Total supply
   - Event image

5. Click "Create Event"

## 🎟️ Step 6: Purchase a Ticket

1. Browse events at `/events`
2. Click on an event
3. Upload a photo of yourself (for AI verification)
4. Click "Buy Ticket"
5. The system will:
   - Upload your photo to IPFS
   - Create NFT metadata
   - Mint the NFT to your wallet
   - Generate a QR code

## ✅ Step 7: Verify a Ticket

1. Go to `/verify`
2. Scan the ticket QR code (or paste QR data manually)
3. Take a selfie or upload a photo
4. Click "Verify Ticket"
5. AI will compare the selfie to the ticket holder's image
6. Result: VERIFIED ✅ / SUSPICIOUS ⚠️ / DENIED ❌

## 🔍 Verification Process

The AI verification works by:

1. Extracting the NFT metadata URI from the QR code
2. Fetching the metadata from IPFS
3. Comparing the live selfie with the ticket holder image
4. Using GPT-4 Vision to determine if they match
5. Returning verification status with confidence level

## 🛠️ Troubleshooting

### "Contract not initialized" error

- Make sure `NFT_CONTRACT_ADDRESS` is set in environment variables
- Verify the contract is deployed on QIE Network
- Check that the address is checksummed (starts with 0x)

### "Minting failed" error

- Ensure `ORGANIZER_PRIVATE_KEY` is set
- Check you have QIE tokens for gas fees
- Verify you're on the QIE Network (Chain ID 5656)

### "OpenAI API key not configured" error

- Set `OPENAI_API_KEY` in environment variables
- Ensure the key is valid and has credits
- Check the model name in `OPENAI_MODEL` (default: gpt-4o)

### "IPFS upload failed" error

- If using Pinata: Set `PINATA_JWT` or `PINATA_API_KEY` + `PINATA_SECRET_API_KEY`
- If not set: System uses mock IPFS hashes (works for testing)

### "Invalid signature" error

- Ensure MetaMask is connected to QIE Network
- Try disconnecting and reconnecting your wallet
- Clear browser cache and localStorage

## 💡 Testing Flow

### Complete Test Scenario

1. **Setup**: Deploy contract, set env vars, make organizer
2. **Create Event**: Login as organizer, create event with image
3. **Buy Ticket**: Connect different wallet, upload selfie, purchase
4. **Verify Ticket**: Scan QR, upload same person's photo → VERIFIED
5. **Fraud Test**: Scan QR, upload different person's photo → DENIED

## 📊 Monitoring

### Check Backend Logs

```bash
# In Replit shell
tail -f /tmp/logs/Backend_*.log
```

### Check Frontend Logs

```bash
tail -f /tmp/logs/Frontend_*.log
```

### View Verification History

Go to: `http://localhost:8000/verify/logs`

## 🔐 Security Best Practices

1. **Never commit private keys** to version control
2. Store `ORGANIZER_PRIVATE_KEY` securely in Replit Secrets
3. Use a dedicated wallet for organizer operations
4. Consider using a multi-sig wallet for production
5. Regularly rotate OpenAI API keys
6. Monitor contract events on QIE explorer

## 🌐 Production Deployment

When deploying to production:

1. Use environment-specific configuration
2. Set up proper MongoDB with authentication
3. Use production RPC endpoints
4. Enable rate limiting on API
5. Add proper CORS configuration
6. Set up SSL/TLS certificates
7. Monitor transaction costs
8. Implement backup strategies

## 📈 Costs

### QIE Blockchain Costs (Approximate)

- Contract Deployment: ~$0.01-1
- Mint NFT Ticket: ~$0.001-0.01 per ticket
- Event Creation (IPFS): Free with mock, ~$0.001 with Pinata

### OpenAI Costs

- AI Verification: ~$0.01-0.05 per verification (GPT-4 Vision)
- Consider using GPT-4o-mini for lower costs

### IPFS Costs (Pinata)

- Free tier: 1 GB storage, unlimited requests
- Pro: $20/month for more storage

## 🎯 Next Steps

After basic setup:

1. Customize frontend branding and styling
2. Add event categories and filtering
3. Implement ticket resale functionality
4. Add email notifications
5. Build mobile app version
6. Implement analytics dashboard
7. Add multi-event season passes

## 📞 Support

- QIE Blockchain: https://docs.qie.digital
- OpenAI: https://platform.openai.com/docs
- Pinata IPFS: https://docs.pinata.cloud
- Project Issues: Check README.md

## 🎉 You're Ready!

Your AI-Verified NFT Ticketing System is now set up and ready to use. Create events, sell tickets, and prevent fraud with blockchain and AI technology!
