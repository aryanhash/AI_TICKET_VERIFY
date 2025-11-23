// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

contract NFTTicket is ERC721URIStorage, Ownable {
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIds;
    
    mapping(uint256 => string) private _tokenURIs;
    
    event TicketMinted(address indexed to, uint256 indexed tokenId, string tokenURI);
    
    constructor() ERC721("QIE NFT Ticket", "QNFT") Ownable(msg.sender) {}
    
    function mint(address to, string memory uri) public onlyOwner returns (uint256) {
        uint256 tokenId = _tokenIds.current();
        _tokenIds.increment();
        
        _safeMint(to, tokenId);
        _setTokenURI(tokenId, uri);
        
        emit TicketMinted(to, tokenId, uri);
        
        return tokenId;
    }
    
    function totalSupply() public view returns (uint256) {
        return _tokenIds.current();
    }
    
    function tokenURI(uint256 tokenId) public view override returns (string memory) {
        return super.tokenURI(tokenId);
    }
    
    function burn(uint256 tokenId) public {
        require(ownerOf(tokenId) == msg.sender, "Only token owner can burn");
        _burn(tokenId);
    }
}
