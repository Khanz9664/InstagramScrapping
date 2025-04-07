#!/usr/bin/env bash
set -eux

# Install system dependencies for Playwright
apt-get update && apt-get install -y \
  libgtk-4-1 \
  libgraphene-1.0-0 \
  libgstgl-1.0-0 \
  libgstcodecparsers-1.0-0 \
  libavif15 \
  libenchant-2-2 \
  libsecret-1-0 \
  libmanette-0.2-0 \
  libgles2

# Install Playwright and its browsers
pip install playwright
echo "Installing Playwright browsers..."
playwright install
echo "Playwright browsers installed successfully!"
