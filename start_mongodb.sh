#!/bin/bash
echo "Checking MongoDB installation..."

# Check if MongoDB is installed via Homebrew
if brew list mongodb-community &>/dev/null; then
    echo "Starting MongoDB..."
    brew services start mongodb-community
    sleep 2
    echo "MongoDB should be running now!"
elif command -v docker &> /dev/null; then
    echo "MongoDB not found via Homebrew. Starting MongoDB in Docker..."
    docker run -d -p 27017:27017 --name mongodb mongo:latest 2>/dev/null || docker start mongodb
    echo "MongoDB should be running in Docker now!"
else
    echo "MongoDB not found. Please install it:"
    echo "  brew tap mongodb/brew && brew install mongodb-community"
    echo "  OR use MongoDB Atlas (cloud): https://www.mongodb.com/cloud/atlas"
fi
