# 🎫 AI-Verified NFT Ticketing System

> **A revolutionary decentralized ticketing platform that combines blockchain technology, AI-powered verification, and QIE Blockchain SDK to create a fraud-proof event ticketing solution.**

[![QIE Blockchain](https://img.shields.io/badge/Blockchain-QIE-blue)](https://docs.qie.digital)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
Youtube link - https://www.youtube.com/watch?v=q2kn6yERfQg

---

<img width="1693" height="867" alt="image" src="https://github.com/user-attachments/assets/15cadf41-aa59-4856-8557-9c3d681ca253" />


## 📖 Table of Contents

- [What is This Project?](#what-is-this-project)
- [Problems It Solves](#problems-it-solves)
- [Key Features](#key-features)
- [What Makes It Unique](#what-makes-it-unique)
- [System Architecture](#system-architecture)
- [Prerequisites](#prerequisites)
- [Installation Guide](#installation-guide)
- [Configuration](#configuration)
- [How to Use](#how-to-use)
- [QIE Blockchain Features](#qie-blockchain-features)
- [API Documentation](#api-documentation)
- [Troubleshooting](#troubleshooting)
- [Support & Resources](#support--resources)

---

## 🎯 What is This Project?

This is a **complete full-stack ticketing system** that uses:

- **Blockchain (QIE Network)**: Tickets are NFTs stored on the blockchain, making them impossible to counterfeit
- **AI Verification**: Uses advanced AI to compare your face with the ticket photo to prevent fraud
- **Decentralized Storage (IPFS)**: Ticket images and data are stored on IPFS, not on a central server
- **Wallet Authentication**: No passwords needed - just connect your MetaMask wallet

### Real-World Example

Imagine you're going to a concert:
1. You buy a ticket online and upload a selfie
2. You receive an NFT ticket in your wallet
3. At the venue, you scan a QR code and take a selfie
4. AI instantly verifies you're the ticket owner
5. You're granted entry - no fraud possible!

---

## 🔥 Problems It Solves

### 1. **Ticket Fraud & Scalping** 
- **Problem**: People buy tickets and resell them at inflated prices or sell fake tickets
- **Solution**: AI verifies the person matches the ticket owner, preventing unauthorized transfers

### 2. **Counterfeit Tickets** 
- **Problem**: Fake tickets are easy to create and hard to detect
- **Solution**: Blockchain ensures every ticket is unique and verifiable

### 3. **Double-Spending** 
- **Problem**: Same ticket used multiple times or sold to multiple people
- **Solution**: Blockchain's immutable records prevent duplicate usage

### 4. **Manual Verification** 
- **Problem**: Slow, error-prone manual ticket checking at events
- **Solution**: AI-powered instant verification in seconds

### 5. **High Transaction Costs** 
- **Problem**: Ethereum gas fees can be expensive
- **Solution**: QIE Blockchain offers ultra-low fees (~$0.001 per transaction)

---

## ✨ Key Features

### 🎫 **NFT-Based Tickets**
- Each ticket is a unique NFT (Non-Fungible Token) on QIE Blockchain
- Immutable ownership records
- Cannot be duplicated or counterfeited
- Transferable between wallets

### 🤖 **AI-Powered Verification**
- Uses OpenAI GPT-4 Vision API (or Gemini/HuggingFace)
- Compares real-time selfie with original ticket photo
- Returns: ✅ VERIFIED / ⚠️ SUSPICIOUS / ❌ DENIED
- Instant results in seconds

### 🔐 **Wallet-Based Authentication**
- No passwords or accounts needed
- Connect with MetaMask wallet
- Secure signature-based login
- Your wallet = your identity

### 📱 **QR Code System**
- Each ticket has a unique QR code
- Easy scanning at event entry
- Contains all ticket information
- Works offline

### 🎪 **Event Management**
- Organizers can create events easily
- Set ticket prices, supply, dates, venues
- Upload event images
- Track sales and verifications

### 🌐 **IPFS Storage**
- Decentralized storage for images and metadata
- No single point of failure
- Permanent, immutable storage
- Fast access via IPFS gateways

### ✅ **QIE Validator Feature**
- Validate QIE network connectivity
- Check contract status
- Verify transactions
- Validate wallet addresses
- Check NFT token ownership
- Comprehensive system health monitoring

---

## 🌟 What Makes It Unique

### 1. **QIE Blockchain Integration** 🚀
- Built specifically for QIE Blockchain using **QIE Blockchain SDK**
- Uses **QIEDEX Token Creator** for contract deployment
- Ultra-low transaction fees
- Fast transaction processing (1-second finality)
- EVM-compatible (works with Ethereum tools)

### 2. **Complete QIE SDK Implementation** 💎
- **Backend**: All blockchain operations use QIE SDK (`server/services/qie_sdk.py`)
- **Frontend**: Wallet operations use QIE SDK (`client/src/lib/qie-sdk.ts`)
- **Contract**: Deployed via QIEDEX Token Creator
- **Validator**: Built-in QIE validation system

### 3. **Multi-AI Provider Support** 🤖
- Supports OpenAI GPT-4 Vision
- Supports Google Gemini
- Supports HuggingFace models
- Easy switching between providers

### 4. **Comprehensive Validation System** ✅
- Network health monitoring
- Contract state validation
- Transaction verification
- Wallet address validation
- Token ownership checks
- Real-time system diagnostics

### 5. **Developer-Friendly** 👨‍💻
- Clean, well-documented code
- TypeScript for type safety
- RESTful API design
- Comprehensive error handling
- Easy to extend and customize

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        FRONTEND                              │
│              (Next.js + TypeScript + TailwindCSS)            │
│                    Port: 5000                                │
│  • Wallet Connection (MetaMask)                              │
│  • Event Browsing                                            │
│  • Ticket Purchase                                           │
│  • QR Code Display                                           │
│  • Verification Interface                                    │
│  • QIE Validator UI                                          │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        │ HTTP/REST API
                        │
┌───────────────────────▼─────────────────────────────────────┐
│                        BACKEND                               │
│                    (FastAPI + Python)                        │
│                    Port: 8000                                │
│  • Authentication (QIE SDK)                                  │
│  • Event Management                                          │
│  • Ticket Minting (QIE SDK)                                  │
│  • AI Verification                                           │
│  • IPFS Integration                                          │
│  • QIE Validation                                            │
└───────┬──────────┬──────────┬──────────┬────────────────────┘
        │          │          │          │
    ┌───▼───┐  ┌──▼───┐  ┌───▼───┐  ┌───▼────┐
    │MongoDB│  │ QIE  │  │ IPFS  │  │  AI    │
    │       │  │Block-│  │(Pinata│  │(OpenAI │
    │       │  │chain │  │  or   │  │Gemini) │
    │       │  │      │  │Mock)  │  │        │
    └───────┘  └──────┘  └───────┘  └────────┘
```

---

## 📋 Prerequisites

Before you begin, make sure you have:

### Required Software
- **Node.js** 20+ ([Download](https://nodejs.org/))
- **Python** 3.11+ ([Download](https://www.python.org/downloads/))
- **MongoDB** ([Download](https://www.mongodb.com/try/download/community) or use MongoDB Atlas)
- **MetaMask** browser extension ([Download](https://metamask.io/))
- **Git** ([Download](https://git-scm.com/))

### Required Accounts & Keys
- **OpenAI API Key** (for AI verification) - [Get it here](https://platform.openai.com/api-keys)
  - Or use **Gemini API** - [Get it here](https://aistudio.google.com/app/apikey)
  - Or use **HuggingFace API** - [Get it here](https://huggingface.co/settings/tokens)
- **Pinata Account** (optional, for IPFS) - [Sign up here](https://www.pinata.cloud/)
- **QIE Testnet Tokens** (for gas fees) - Get from QIE faucet

---

## 🚀 Installation Guide

### Step 1: Clone the Repository

```bash
git clone <your-repo-url>
cd PerfectCleanEnd
```

### Step 2: Install Backend Dependencies

```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
cd server
pip install -r requirements.txt
cd ..
```

### Step 3: Install Frontend Dependencies

```bash
cd client
npm install
cd ..
```

### Step 4: Set Up MongoDB

#### Option A: Local MongoDB
```bash
# macOS (using Homebrew)
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community

# Or use the provided script
chmod +x start_mongodb.sh
./start_mongodb.sh
```

#### Option B: MongoDB Atlas (Cloud)
1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a free account
3. Create a free cluster
4. Get your connection string

### Step 5: Configure Environment Variables

Create a `.env` file in the `server/` directory:

```env
# MongoDB Connection
MONGO_URL=mongodb://localhost:27017/


# QIE Blockchain Configuration
QIE_RPC_URL=https://rpc1testnet.qie.digital
QIE_CONTRACT_ADDRESS=0xYourContractAddressHere
ORGANIZER_PRIVATE_KEY=your_private_key_here

# AI Verification (Choose one)
# Option 1: OpenAI
OPENAI_API_KEY=sk-your-openai-api-key
AI_PROVIDER=openai

# Option 2: Gemini
# GEMINI_API_KEY=your-gemini-api-key
# AI_PROVIDER=gemini

# Option 3: HuggingFace
# HUGGINGFACE_API_KEY=your-huggingface-api-key
# AI_PROVIDER=huggingface

# IPFS Storage (Optional - uses mock if not set)
PINATA_JWT=your-pinata-jwt-token
PINATA_API_KEY=your-pinata-api-key
PINATA_SECRET_API_KEY=your-pinata-secret-key
```

### Step 6: Deploy Smart Contract

**IMPORTANT**: This project uses **QIEDEX Token Creator** for contract deployment.

1. Go to [QIEDEX Token Creator](https://dex.qie.digital/#/token-creator)
2. Connect your MetaMask wallet
3. Ensure MetaMask is on **QIE testnet** (Chain ID: 1983)
4. Create NFT contract:
   - Token Name: `QIE NFT Ticket`
   - Token Symbol: `QNFT`
   - Enable `mint(address to, string memory uri)` function
   - Set owner-only minting
5. Deploy the contract
6. Copy the contract address
7. Update `QIE_CONTRACT_ADDRESS` in your `.env` file


### Step 7: Configure MetaMask for QIE Network

1. Open MetaMask
2. Click network dropdown → "Add Network"
3. Enter:
   - **Network Name**: QIE testnet
   - **RPC URL**: https://rpc1testnet.qie.digital
   - **Chain ID**: 1983
   - **Currency Symbol**: QIE
   - **Block Explorer**: https://testnet.qie.digital/
4. Click "Save"
5. Switch to "QIE testnet" network

### Step 8: Start the Servers

#### Start Backend (Terminal 1)
```bash
cd server
source ../venv/bin/activate  # If using virtual environment
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

#### Start Frontend (Terminal 2)
```bash
cd client
npm run dev
```

### Step 9: Verify Installation

1. **Backend**: Open http://localhost:8000/health
   - Should return: `{"status":"healthy"}`

2. **Frontend**: Open http://localhost:5000
   - Should show the homepage

3. **API Docs**: Open http://localhost:8000/docs
   - Should show FastAPI documentation

---

## ⚙️ Configuration

### Environment Variables Explained

| Variable | Required | Description |
|----------|----------|-------------|
| `MONGO_URL` | Yes | MongoDB connection string |
| `QIE_RPC_URL` | Yes | QIE testnet RPC endpoint |
| `QIE_CONTRACT_ADDRESS` | Yes | Your deployed contract address |
| `ORGANIZER_PRIVATE_KEY` | Yes | Private key for minting tickets |
| `OPENAI_API_KEY` | Yes* | OpenAI API key for verification |
| `AI_PROVIDER` | No | AI provider: `openai`, `gemini`, or `huggingface` |
| `PINATA_JWT` | No | Pinata JWT for IPFS (optional) |

*At least one AI API key is required

### Making a User an Organizer

To create events, a wallet must be set as an organizer:

```bash
curl -X POST http://localhost:8000/auth/make-organizer/0xYourWalletAddress
```

---

## 📱 How to Use

### For Event Organizers

#### 1. Connect Your Wallet
- Open the url...
- Click "Connect Wallet"
- Approve MetaMask connection
- Sign the authentication message

#### 2. Become an Organizer
- Use the API endpoint to make your wallet an organizer (see above)
- Or ask an admin to do it

#### 3. Create an Event
- Go to http://deployedlink
- Fill in event details:
  - Event title
  - Description
  - Date and time
  - Venue
  - Ticket price (in QIE)
  - Total ticket supply
  - Upload event image
- Click "Create Event"

#### 4. Monitor Sales
- View created events
- Track ticket sales
- Check verification logs

### For Ticket Buyers

#### 1. Connect Your Wallet
- Open http://localhost:5000
- Click "Connect Wallet"
- Approve MetaMask connection
- Ensure you're on QIE testnet

#### 2. Browse Events
- Browse available events
- Click on an event to see details

#### 3. Purchase a Ticket
- Click "Buy Ticket" on an event
- Upload a clear selfie photo (this will be used for verification)
- Confirm the transaction in MetaMask
- Wait for the NFT to be minted
- You'll receive a QR code

#### 4. View Your Tickets
- See all your purchased tickets
- Click "Show QR Code" to display the QR code

### For Event Staff (Verification)

#### 1. Go to Verification Page
- Open http://localhost:5000/verify

#### 2. Scan QR Code
- Click "Scan QR Code"
- Point camera at the ticket's QR code
- QR data will be captured automatically

#### 3. Verify Ticket
- Ask the attendee to take a selfie
- Upload the selfie
- Click "Verify Ticket"
- AI will compare the selfie with the original ticket photo
- Result: ✅ VERIFIED / ⚠️ SUSPICIOUS / ❌ DENIED

---

## 🔧 QIE Blockchain Features

### QIE Blockchain SDK

This project uses **QIE Blockchain SDK** for all blockchain operations:

#### Backend (`server/services/qie_sdk.py`)
- **QIEWeb3**: Connects to QIE network
- **QIEContract**: Interacts with NFT contract
- **QIESignature**: Verifies wallet signatures
- **QIENFT**: Manages NFT operations

#### Frontend (`client/src/lib/qie-sdk.ts`)
- **QIEWeb3**: Wallet connection
- **QIEContract**: Contract interactions
- **QIESignature**: Message signing
- **QIENFT**: NFT operations

### QIE Validator Feature

The built-in QIE Validator helps you monitor and validate your QIE integration:

#### Access Validator UI
- Go to http://localhost:5000/validator

#### Available Validations

1. **Network Validation**
   - Check QIE network connectivity
   - View latest block information
   - Check gas prices
   - Verify chain ID

2. **Contract Validation**
   - Verify contract is loaded
   - Check total supply
   - View available functions
   - Validate contract address

3. **Transaction Validation**
   - Verify transaction exists
   - Check confirmation status
   - View transaction details
   - Check gas usage

4. **Wallet Validation**
   - Validate address format
   - Check if address is a contract
   - View wallet balance
   - Verify checksum address

5. **Token Validation**
   - Verify token exists
   - Check token owner
   - View token URI
   - Validate token metadata

6. **Comprehensive Validation**
   - Run all validations at once
   - Get complete system health report
   - Identify any issues

#### API Endpoints

```bash
# Network validation
curl http://localhost:8000/validator/network

# Contract validation
curl http://localhost:8000/validator/contract

# Transaction validation
curl http://localhost:8000/validator/transaction/0xYourTxHash

# Wallet validation
curl http://localhost:8000/validator/wallet/0xYourAddress

# Token validation
curl http://localhost:8000/validator/token/1

# Comprehensive validation
curl http://localhost:8000/validator/comprehensive
```

### QIE Contract Deployment

The project uses **QIEDEX Token Creator** for contract deployment:

1. **Why QIEDEX Token Creator?**
   - Easy, no-code contract deployment
   - Pre-configured for QIE network
   - Generates contract address and ABI automatically
   - Required by project specifications

2. **Contract Functions**
   - `mint(address to, string memory uri)`: Mint new tickets
   - `tokenURI(uint256 tokenId)`: Get ticket metadata
   - `ownerOf(uint256 tokenId)`: Check ticket owner
   - `balanceOf(address owner)`: Get owner's ticket count
   - `totalSupply()`: Get total tickets minted

3. **Contract Address**
   - Stored in `QIE_CONTRACT_ADDRESS` environment variable
   - Used by QIE SDK to interact with contract
   - Must be deployed on QIE testnet (Chain ID: 1983)

### Wallet Validation

The system validates wallets in multiple ways:

1. **Signature Verification**
   - User signs a message with their wallet
   - Backend verifies signature using QIE SDK
   - No passwords needed - wallet is the identity

2. **Address Validation**
   - Checks address format (must start with 0x, 42 characters)
   - Converts to checksum address
   - Verifies address is valid

3. **Ownership Verification**
   - Checks if wallet owns specific NFT tickets
   - Verifies ticket ownership on blockchain
   - Prevents unauthorized access

---

## 📊 API Documentation

### Authentication

```http
POST /auth/wallet
Content-Type: application/json

{
  "wallet_address": "0x...",
  "message": "Sign this message to login",
  "signature": "0x..."
}
```

### Events

```http
GET /events                    # List all events
GET /events/{id}               # Get event details
POST /events                   # Create event (organizer only)
```

### Tickets

```http
POST /tickets/mint             # Mint NFT ticket
GET /tickets/{wallet}          # Get user's tickets
```

### Verification

```http
POST /verify                   # Verify ticket with AI
GET /verify/logs               # Get verification history
```

### Validator

```http
GET /validator/network         # Validate network
GET /validator/contract        # Validate contract
GET /validator/transaction/{tx_hash}  # Validate transaction
GET /validator/wallet/{address}       # Validate wallet
GET /validator/token/{token_id}       # Validate token
GET /validator/comprehensive          # Full validation
GET /validator/health                 # Validator health
```

📖 **Full API Documentation**: http://localhost:8000/docs

---

## 🐛 Troubleshooting

### Common Issues

#### 1. "Module not found" errors
```bash
# Backend
cd server
pip install -r requirements.txt

# Frontend
cd client
npm install
```

#### 2. MongoDB connection failed
```bash
# Check if MongoDB is running
brew services list | grep mongodb

# Start MongoDB
brew services start mongodb-community
# Or
./start_mongodb.sh
```

#### 3. "Contract not initialized" error
- Check `QIE_CONTRACT_ADDRESS` is set in `.env`
- Verify contract address is correct
- Ensure contract is deployed on QIE testnet
- Use QIE Validator to check contract status

#### 4. "Insufficient funds" error
- Get QIE testnet tokens from faucet
- Check wallet has QIE tokens for gas fees
- Verify you're on QIE testnet (not mainnet)

#### 5. MetaMask connection issues
- Ensure MetaMask is installed
- Check QIE network is added to MetaMask
- Verify you're on QIE testnet
- Try refreshing the page

#### 6. AI verification not working
- Check API key is set correctly
- Verify API key has credits/quota
- Check `AI_PROVIDER` is set correctly


#### 7. IPFS upload failed
- Check Pinata credentials (if using)
- System will use mock hashes if Pinata not configured
- Verify PINATA_JWT is valid

### Getting Help

1. **Check Logs**
   - Backend: Check terminal output
   - Frontend: Check browser console (F12)

2. **Use QIE Validator**
   - Go to http://localhost:5000/validator
   - Run comprehensive validation
   - Check for any errors

3. **Verify Configuration**
   - Check all environment variables are set
   - Verify contract address is correct
   - Ensure MongoDB is running

---

## 📚 Support & Resources

### QIE Blockchain Resources
- **QIE Documentation**: https://docs.qie.digital
- **QIEDEX Token Creator**: https://dex.qie.digital/#/token-creator
- **QIE Testnet Explorer**: https://testnet.qie.digital/
- **QIE Discord**: https://discord.com/invite/9HCNTyqkwa

### AI Provider Resources
- **OpenAI**: https://platform.openai.com/
- **Gemini**: https://aistudio.google.com/
- **HuggingFace**: https://huggingface.co/

### IPFS Resources
- **Pinata**: https://www.pinata.cloud/
- **IPFS Documentation**: https://docs.ipfs.tech/

---

## 🎓 Learning Resources

### For Beginners

1. **Blockchain Basics**
   - What is a blockchain?
   - What are NFTs?
   - How do wallets work?

2. **QIE Blockchain**
   - Why QIE is different
   - How to use QIE testnet
   - Understanding gas fees

3. **Web3 Development**
   - MetaMask integration
   - Smart contract interaction
   - Transaction signing

4. **AI Verification**
   - How face recognition works
   - AI model comparison
   - Verification accuracy

---

## 📄 License

MIT License - feel free to use this project for learning, hackathons, or commercial purposes!

---

## 🤝 Contributing

This is a hackathon project. Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

---

## ⭐ Features Summary

✅ **Blockchain-Based**: NFT tickets on QIE Blockchain  
✅ **AI-Powered**: Face verification using advanced AI  
✅ **Decentralized**: IPFS storage, no central authority  
✅ **Secure**: Wallet-based auth, no passwords  
✅ **Fast**: QIE's 1-second finality  
✅ **Cheap**: Ultra-low transaction fees  
✅ **Validated**: Built-in QIE validation system  
✅ **User-Friendly**: Clean UI, easy to use  

---

**Built with ❤️ using QIE Blockchain SDK**

For questions or support, check the documentation files or reach out to the QIE community!
