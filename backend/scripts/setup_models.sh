#!/bin/bash

# Setup ML models for face recognition

echo "Setting up InsightFace models..."
echo "================================"

# Create models directory
mkdir -p models

# Download using Python script
python -m backend.scripts.download_models

echo "================================"
echo "Setup complete!"
echo ""
echo "Models location: models/"
echo ""
echo "Models included:"
echo "  - det_10g.onnx (SCRFD face detector)"
echo "  - w600k_r50.onnx (ArcFace recognizer)"
echo "  - 2d106det.onnx (2D landmarks)"
echo "  - 1k3d68.onnx (3D landmarks)"
echo "  - genderage.onnx (Gender/Age classifier)"