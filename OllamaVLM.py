import base64
import io
import time
import json
import requests
from PIL import Image
from utils import Utils

class OllamaVLM:
    def __init__(self, url, model_name):
        self.ollama_url = url
        self.model_name = model_name  # Adjust based on your model
        self.model_ready = False
        self.setup_model()

    def setup_model(self):
        """Setup and ensure model is ready"""
        try:
            # Check if Ollama is running
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get("models", [])
                model_exists = any(model["name"].startswith(self.model_name) for model in models)

                if not model_exists:
                    print(f"Pulling {self.model_name}...")
                    self.pull_model()
                else:
                    print(f"Model {self.model_name} is ready")
                    self.model_ready = True
            else:
                print("❌ Ollama is not running. Please start Ollama first.")
        except Exception as e:
            print(f"❌ Error connecting to Ollama: {e}")

    def pull_model(self):
        """Pull the model if not available"""
        try:
            response = requests.post(
                f"{self.ollama_url}/api/pull",
                json={"name": self.model_name},
                stream=True,
                timeout=300
            )

            if response.status_code == 200:
                for line in response.iter_lines():
                    if line:
                        data = json.loads(line)
                        if "status" in data:
                            print(f"📥 {data['status']}")
                        if data.get("status") == "success":
                            self.model_ready = True
                            break
        except Exception as e:
            print(f"❌ Error pulling model: {e}")

    def generate_response(self, prompt, image, temperature, max_tokens, history=None):
        """Generate response using Ollama with conversation history"""
        if not self.model_ready:
            return "❌ Model not ready. Please check Ollama setup.", None

        if not prompt.strip():
            return "❌ Please enter a prompt.", None

        # Build conversation context from history
        full_prompt = Utils.build_conversation_prompt(prompt, history)

        # Prepare the request
        payload = {
            "model": self.model_name,
            "prompt": full_prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
                "num_ctx": 4096  # Increased context window for conversation history
            }
        }

        if image is not None:
            image = Image.open(image[0])
            try:
                image = Utils.optimize_image(image)
                # Convert PIL Image to base64
                img_buffer = io.BytesIO()
                image.save(img_buffer, format='JPEG')
                img_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
                payload["images"] = [img_base64]
            except Exception as e:
                return f"❌ Error processing image: {e}", None

        try:
            start_time = time.time()
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json=payload,
                timeout=300
            )
            end_time = time.time()

            if response.status_code == 200:
                result = response.json()
                latency = end_time - start_time

                # Format metrics
                metrics = {
                    "Response Time": f"{latency:.2f}s",
                    "Tokens Generated": result.get("eval_count", "N/A"),
                    "Tokens/Second": f"{result.get('eval_count', 0) / latency:.1f}" if latency > 0 else "N/A",
                    "Model": self.model_name,
                    "Hardware": "RTX 3050 (Local)",
                    "Cost": "$0.00 (No API fees!)",
                    "Context Length": len(full_prompt.split()) if full_prompt else 0
                }

                return result["response"], metrics
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return f"Internal Server Error", None

        except requests.exceptions.Timeout:
            return "❌ Request timed out. Try reducing max_tokens or simplifying the prompt.", None

