# AI-Verified NFT Ticketing System

A full-stack decentralized ticketing platform built on QIE Blockchain with AI-powered verification to prevent fraud.

## 🚀 Features

- **Blockchain-Based Tickets**: NFT tickets minted on QIE Blockchain (Chain ID: 5656)
- **AI Verification**: OpenAI Vision API compares selfies to ticket holder images
- **MetaMask Integration**: Secure wallet-based authentication
- **IPFS Storage**: Decentralized storage for ticket images and metadata
- **Event Management**: Organizers can create and manage events
- **Real-time Verification**: Instant fraud detection at event entry

## 🛠️ Tech Stack

### Frontend
- Next.js 14 with TypeScript
- TailwindCSS for styling
- ethers.js for Web3 integration
- React QR Code components

### Backend
- Python FastAPI
- MongoDB for database
- Web3.py for QIE blockchain interaction
- OpenAI Vision API for verification
- Pinata for IPFS uploads

### Blockchain
- QIE Blockchain (EVM-compatible)
- Solidity ERC721 Smart Contract
- Ultra-low gas fees

## 📦 Installation

### Prerequisites
- Node.js 20+
- Python 3.11+
- MongoDB
- MetaMask wallet with QIE network configured

### Environment Variables

Create a `.env` file with:

```env
# MongoDB
MONGO_URL=mongodb://localhost:27017/

# QIE Blockchain
QIE_RPC_URL=https://rpc-mainnet.qie.digital
NFT_CONTRACT_ADDRESS=<your_deployed_contract_address>
ORGANIZER_PRIVATE_KEY=<your_private_key>

# IPFS (Pinata)
PINATA_JWT=<your_pinata_jwt>
PINATA_API_KEY=<your_pinata_api_key>
PINATA_SECRET_API_KEY=<your_pinata_secret_key>

# AI Verification
OPENAI_API_KEY=<your_openai_api_key>
```

### Backend Setup

```bash
cd server
pip install -r requirements.txt
python main.py
```

Backend runs on: `http://localhost:8000`

### Frontend Setup

```bash
cd client
npm install
npm run dev
```

Frontend runs on: `http://localhost:5000`

## 🔗 QIE Network Configuration

Add QIE Network to MetaMask:

```
Network Name: QIE Blockchain
RPC URL: https://rpc-mainnet.qie.digital
Chain ID: 5656
Currency Symbol: QIE
Block Explorer: https://mainnet.qie.digital
```

## 📝 Smart Contract Deployment

1. Go to [Remix IDE](https://remix.ethereum.org)
2. Copy `contracts/NFTTicket.sol`
3. Compile with Solidity 0.8.20+
4. Deploy to QIE Network using MetaMask
5. Copy contract address to `.env`

See `contracts/DEPLOYMENT.md` for detailed instructions.

## 🎫 Usage Flow

### For Users
1. Connect MetaMask wallet
2. Browse available events
3. Purchase ticket with selfie upload
4. Receive NFT ticket with QR code
5. At event: Scan QR + take selfie for AI verification

### For Organizers
1. Connect wallet and become organizer
2. Create event with details and image
3. Tickets are minted when purchased
4. View verification logs

## 🤖 AI Verification

The system uses OpenAI's GPT-4 Vision to:
1. Extract image from NFT metadata (IPFS)
2. Compare with real-time selfie
3. Return: VERIFIED / SUSPICIOUS / DENIED
4. Log all verification attempts

## 🔒 Security Features

- Wallet signature authentication (no passwords)
- Smart contract ownership controls
- AI-powered fraud detection
- Immutable blockchain records
- Encrypted IPFS storage

## 📊 API Endpoints

```
POST /auth/wallet              - Wallet login
GET /events                    - List all events
POST /events                   - Create event (organizer)
GET /events/{id}               - Event details
POST /tickets/mint             - Mint NFT ticket
GET /tickets/{wallet}          - User's tickets
POST /verify                   - Verify ticket with AI
GET /verify/logs               - Verification history
```

## 🌟 Why QIE Blockchain?

- **Ultra-low fees**: ~$0.001 per transaction
- **Fast**: 1-second finality, 25,000 TPS
- **EVM-compatible**: Use existing Ethereum tools
- **Deflationary**: 80% of gas fees burned

## 📄 License

MIT License

## 🤝 Contributing

This is a hackathon project. Feel free to fork and improve!

## 🐛 Known Issues

- Requires manual contract deployment
- IPFS credentials needed for image uploads
- MongoDB must be running locally

## 📞 Support

For QIE Blockchain support:
- Discord: https://discord.com/invite/9HCNTyqkwa
- Docs: https://docs.qie.digital
