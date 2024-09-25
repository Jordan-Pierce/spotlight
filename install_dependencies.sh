#!/bin/bash

# Install Python dependencies using poetry
poetry install

# Install JavaScript dependencies using pnpm
pnpm install

# Build the frontend
make build-frontend
