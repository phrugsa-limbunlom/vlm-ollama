import argparse

import gradio as gr

from OllamaVLM import OllamaVLM


def chat_interface(message, history, temperature, max_tokens):
    """Main chat interface function"""
    prompt = message["text"]
    image = message["files"] if message["files"] else None

    if not prompt.strip():
        return ""

    response, metrics = ollama_vlm.generate_response(prompt=prompt,
                                                     image=image,
                                                     temperature=temperature,
                                                     max_tokens=max_tokens,
                                                     history=history)

    if metrics:
        metrics_str = "\n\n📊 **Performance Metrics:**\n"
        for key, value in metrics.items():
            metrics_str += f"• **{key}:** {value}\n"
        response += metrics_str

    return response

if __name__ == "__main__":

    # url = "http://ollama:11434"
    url = "http://localhost:11434"

    parser = argparse.ArgumentParser()
    parser.add_argument("--model-name", type=str)
    args = parser.parse_args()

    model_name = args.model_name

    ollama_vlm = OllamaVLM(url, model_name)

    print("Starting Local VLM Demo...")
    print(f"Using model: {ollama_vlm.model_name}")

    # Create the Gradio interface
    with gr.Blocks(
            title="Local VLM Demo - Zero API Costs",
            theme=gr.themes.Soft(),
            css="""
        .gradio-container {
            max-width: 1200px !important;
        }
        .chat-container {
            height: 500px;
        }
        """
    ) as demo:
        gr.Markdown("""
        # 🚀 Local Vision-Language Model Demo

        **Experience the power of local AI inference!**
        - 🔒 **100% Private** - Your data never leaves your machine
        - 💰 **Zero API Costs** - No per-request charges
        - ⚡ **Low Latency** - Direct GPU acceleration
        - 🌐 **Offline Capable** - Works without internet

        *Powered by Ollama + Gemma3 running on RTX 3050*
        """)

        with gr.Row():
            with gr.Column(scale=3):
                # Settings at the top for easy access
                with gr.Row():
                    temperature = gr.Slider(
                        label="Temperature",
                        minimum=0.1,
                        maximum=1.0,
                        value=0.7,
                        step=0.1,
                        info="Higher = more creative"
                    )

                    max_tokens = gr.Slider(
                        label="Max Tokens",
                        minimum=50,
                        maximum=500,
                        value=200,
                        step=50,
                        info="Response length limit"
                    )

                # ChatInterface with proper additional inputs
                chatbot = gr.ChatInterface(
                    chat_interface,
                    title="💬 Chat with Local VLM",
                    type="messages",
                    multimodal=True,
                    additional_inputs=[temperature, max_tokens],
                    examples=[
                        [{"text": "Describe this image in detail", "files": ["./examples/bar-graph-example.png"]}],
                        [{"text": "What objects do you see?", "files": ["./examples/object-example.jpg"]}],
                        [{"text": "Write a story about this image", "files": ["./examples/story-example.jpg"]}],
                        [{"text": "What's the mood of this scene?", "files": ["./examples/mood-example.png"]}],
                    ],
                )

            with gr.Column(scale=1):
                gr.Markdown("### 🎯 Demo Highlights")
                gr.Markdown("""
                - **Real-time inference** on local hardware
                - **Vision + Language** understanding
                - **Cost-effective** solution
                """)

                gr.Markdown("### 💡 Usage Tips:")
                gr.Markdown("""
                - Chat with text or text with image
                - Adjust temperature for creativity (0.1 = focused, 1.0 = creative)
                - Set max tokens to control response length
                """)

                model_status = gr.Textbox(
                    label="Model Status",
                    value="✅ Ready" if ollama_vlm.model_ready else "⏳ Loading...",
                    interactive=False
                )

        # Auto-refresh model status
        def update_status():
            return "✅ Ready" if ollama_vlm.model_ready else "⏳ Loading..."

        demo.load(update_status, outputs=model_status)

    demo.launch(
        server_name="127.0.0.1",  # Only localhost access
        server_port=7862,
        share=False,  # Set to True for public link
        show_error=True,
        max_threads=4
    )