# AI-Verified NFT Ticketing System

## Project Overview

A full-stack decentralized event ticketing platform built for QIE Blockchain with AI-powered facial verification.

**Purpose**: Eliminate ticket fraud through blockchain NFTs and AI selfie matching.

**Current State**: Complete MVP with frontend, backend, smart contract, and AI verification.

## Recent Changes (November 23, 2025)

- ✅ Initial project setup with Next.js frontend and FastAPI backend
- ✅ Smart contract (ERC721) created for NFT tickets
- ✅ Web3 integration with QIE Blockchain (Chain ID 5656)
- ✅ MongoDB models for users, events, tickets, verifications
- ✅ IPFS service for decentralized image storage
- ✅ OpenAI Vision API integration for selfie verification
- ✅ Complete frontend with wallet connection, event browsing, ticket purchasing
- ✅ QR code generation and scanning for verification

## Project Architecture

### Frontend (client/)
- **Framework**: Next.js 14 with TypeScript
- **Styling**: TailwindCSS
- **Web3**: ethers.js v6
- **Key Pages**:
  - `/` - Landing page
  - `/events` - Event listing
  - `/events/[id]` - Event details & purchase
  - `/dashboard` - User tickets
  - `/verify` - QR scan & AI verification
  - `/organizer/create` - Event creation

### Backend (server/)
- **Framework**: FastAPI (Python)
- **Database**: MongoDB
- **Blockchain**: Web3.py for QIE integration
- **AI**: OpenAI Vision API
- **Storage**: IPFS (Pinata)
- **Routes**:
  - `/auth` - Wallet authentication
  - `/events` - Event management
  - `/tickets` - NFT minting
  - `/verify` - AI verification

### Smart Contract (contracts/)
- **Type**: ERC721 NFT
- **Network**: QIE Blockchain
- **Functions**: mint, tokenURI, ownerOf, balanceOf

## User Preferences

### Development Style
- TypeScript for type safety
- Clean component structure
- Separation of concerns (lib/, components/, pages/)
- Environment-based configuration

### Deployment Notes
- Frontend must run on port 5000 (Replit requirement)
- Backend runs on port 8000
- API proxied through Next.js rewrites

## Environment Variables Required

### Critical (Must Configure)
```
NFT_CONTRACT_ADDRESS - Deployed smart contract address
ORGANIZER_PRIVATE_KEY - Wallet private key for minting
OPENAI_API_KEY - For AI verification
MONGO_URL - MongoDB connection string
```

### Optional (Enhanced Features)
```
PINATA_JWT - IPFS uploads (or use mock)
PINATA_API_KEY - Alternative IPFS auth
PINATA_SECRET_API_KEY - Alternative IPFS auth
QIE_RPC_URL - Custom RPC (default: https://rpc-mainnet.qie.digital)
```

## Dependencies

### Python
- fastapi, uvicorn - Web framework
- pymongo - MongoDB driver
- web3 - QIE blockchain SDK
- openai - AI verification
- python-jose - JWT handling
- Pillow - Image processing

### Node.js
- next, react - Frontend framework
- ethers - Web3 wallet integration
- react-qr-code - QR generation
- html5-qrcode - QR scanning
- axios - API calls
- tailwindcss - Styling

## Setup Instructions

### 1. Deploy Smart Contract
- Use Remix IDE or Hardhat
- Deploy to QIE Network (Chain ID 5656)
- Save contract address

### 2. Configure Environment
- Set NFT_CONTRACT_ADDRESS
- Set ORGANIZER_PRIVATE_KEY
- Configure OPENAI_API_KEY for verification
- Set MONGO_URL if using external MongoDB

### 3. Make User an Organizer
```bash
curl -X POST http://localhost:8000/auth/make-organizer/<wallet_address>
```

### 4. Create Events
- Connect wallet as organizer
- Go to /organizer/create
- Upload event image and details

### 5. Test Purchase Flow
- Browse events
- Upload selfie photo
- Mint NFT ticket
- View in dashboard

### 6. Test Verification
- Go to /verify
- Scan ticket QR code
- Upload selfie
- AI verifies match

## Technical Decisions

### Why QIE Blockchain?
- Ultra-low gas fees (100-1000x cheaper than Ethereum)
- EVM-compatible (reuse existing tools)
- Fast finality (1 second)
- Deflationary tokenomics

### Why NFT Tickets?
- Immutable ownership
- Transferable (optional resale)
- Verifiable on-chain
- Embedded metadata (IPFS)

### Why AI Verification?
- Prevents ticket resale fraud
- Real-time face matching
- No manual checks needed
- Scalable verification

## Troubleshooting

### "Invalid signature" error
- Ensure QIE network selected in MetaMask
- Check wallet is connected
- Try reconnecting wallet

### "Minting failed" error
- Verify contract address is set
- Check organizer private key is valid
- Ensure QIE tokens for gas fees

### "Verification failed" error
- Confirm OpenAI API key is set
- Check image format (JPEG/PNG)
- Verify IPFS metadata is accessible

## Next Steps (Post-MVP)

- [ ] Secondary marketplace for ticket resale
- [ ] Royalty tracking for organizers
- [ ] Bulk ticket minting optimization
- [ ] Mobile app with native camera
- [ ] Analytics dashboard
- [ ] Multi-event season passes
- [ ] Discord/Telegram bot integration
