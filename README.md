# vlm-ollama

# 🚀 Local Vision-Language Model Demo

A powerful, privacy-focused Vision-Language Model (VLM) demo that runs entirely on your local machine using Ollama. Experience AI-powered image understanding and chat capabilities without any API costs or privacy concerns.

## ✨ Features

- **🔒 100% Private** - Your data never leaves your machine
- **💰 Zero API Costs** - No per-request charges or subscriptions
- **⚡ Low Latency** - Direct GPU acceleration for fast inference
- **🌐 Offline Capable** - Works without internet connection
- **🖼️ Multimodal** - Supports both text and image inputs
- **💬 Conversational** - Maintains chat history and context
- **📊 Performance Metrics** - Real-time inference statistics
- **🎛️ Customizable** - Adjustable temperature and token limits

## 🛠️ Prerequisites

### System Requirements
- **GPU**: NVIDIA RTX 3050 or better (recommended)
- **RAM**: 8GB+ (16GB recommended for larger models)
- **Storage**: 10GB+ free space for models
- **OS**: Windows, macOS, or Linux

### Software Dependencies
- Python 3.8+
- [Ollama](https://ollama.ai/) installed and running
- CUDA drivers (for GPU acceleration)

## 📦 Installation

### 1. Install Ollama
```bash
# Visit https://ollama.ai/ and download the installer for your OS
# Or use package managers:

# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.ai/install.sh | sh
```

### 2. Clone and Setup Project
```bash
git clone https://github.com/phrugsa-limbunlom/vlm-ollama.git
cd vlm-ollama
```

### 3. Install Required Python Packages
```bash
pip install -r requirements.txt
```

## 🚀 Quick Start

### 1. Start Ollama Service
```bash
# Set up flash attention for performance optimization
set OLLAMA_FLASH_ATTENTION=1 # For Windows
export OLLAMA_FLASH_ATTENTION=1 # For Linux
# Start Ollama service
ollama serve
```

### 2. Pull a Vision Model
```bash
# Example: Pull LLaVA model (adjust based on your preference)
ollama pull gemma3:4b
```

### 3. Run the Demo (Specify your own model)
```bash
python main.py --model-name gemma3:4b
```

### 4. Access the Interface
Open your browser and navigate to:
```
http://localhost:7862
```

## 📁 Project Structure

```
local-vlm-demo/
├── main.py              # Main Gradio interface
├── OllamaVLM.py         # Ollama VLM wrapper class
├── utils.py             # Utility functions
├── examples/            # Example images for testing
│   ├── bar-graph-example.png
│   ├── object-example.jpg
│   ├── story-example.jpg
│   └── mood-example.png
├── requirements.txt     # Python dependencies
└── README.md           
```

## 🔧 Configuration

### Model Selection
The demo supports any Ollama-compatible vision model. Popular options:

- **LLaVA 7B**: `llava:7b` (Recommended for RTX 3050)
- **LLaVA 13B**: `llava:13b` (Requires more VRAM)
- **Gemma2**: `gemma2:2b` (Lightweight option)

### Performance Tuning
Adjust these parameters in the interface:

- **Temperature** (0.1-1.0): Controls creativity
  - 0.1: More focused, deterministic responses
  - 1.0: More creative, varied responses

- **Max Tokens** (50-500): Response length limit
  - Lower values: Shorter, more concise responses
  - Higher values: Longer, more detailed responses

### Network Configuration
By default, the demo runs on:
- **Host**: `127.0.0.1` (accessible from other devices on network)
- **Port**: `7862`
- **Ollama URL**: `http://localhost:11434`

To change these settings, modify the values in `app.py`:
For different Ollama URL (e.g., Docker), `url = "http://ollama:11434"`  # Docker container

## 🔍 Troubleshooting

### Common Issues

#### 1. "Model not ready" Error
```bash
# Check if Ollama is running
ollama list

# If model is missing, pull it
ollama pull llava:7b
```

#### 2. CUDA/GPU Issues
```bash
# Check GPU availability
nvidia-smi

# Verify CUDA installation
nvcc --version
```

#### 3. Connection Errors
- Ensure Ollama service is running: `ollama serve`
- Check firewall settings
- Verify port 11434 is not blocked

#### 4. Out of Memory Errors
- Use smaller models (e.g., `gemma2:2b`)
- Reduce max_tokens parameter
- Close other GPU-intensive applications

### Performance Optimization

#### For RTX 3050 (4GB VRAM):
- Recommended model: `llava:7b`
- Max tokens: 200-300
- Batch size: 1

#### For Higher-End GPUs:
- Models: `llava:13b` or larger
- Max tokens: 500+
- Enable concurrent requests

## 🔐 Privacy & Security

### Data Privacy
- **No external API calls** - Everything runs locally
- **No data logging** - Conversations are not stored
- **No telemetry** - No usage data sent anywhere

### Security Considerations
- Default configuration does not allow network access (`127.0.0.1`)
- For external access, use `.0.0.0.0`
- Consider firewall rules for production use

## 📊 Performance Metrics

The demo provides real-time metrics:

- **Response Time**: End-to-end inference time
- **Tokens Generated**: Number of output tokens
- **Tokens/Second**: Generation speed
- **Model**: Current model in use
- **Context Length**: Current conversation context size

## 📄 License

This project is licensed under the MIT License. See LICENSE file for details.