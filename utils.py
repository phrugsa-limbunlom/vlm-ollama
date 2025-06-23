from PIL import Image

class Utils:

    @staticmethod
    def build_conversation_prompt(current_prompt, history):
        """Build a conversation prompt including history"""
        if not history:
            return current_prompt

        # Start with a system message to set context
        conversation_parts = []

        # Add conversation history
        for message in history:
            if message["role"] == "user":
                # Handle both text and multimodal messages
                if isinstance(message["content"], dict):
                    # Multimodal message (text + image)
                    text_content = message["content"].get("text", "")
                    if text_content:
                        conversation_parts.append(f"Human: {text_content}")
                else:
                    # Text-only message
                    conversation_parts.append(f"Human: {message['content']}")
            elif message["role"] == "assistant":
                # Clean up the assistant response (remove metrics if present)
                content = message["content"]
                if "📊 **Performance Metrics:**" in content:
                    content = content.split("📊 **Performance Metrics:**")[0].strip()
                conversation_parts.append(f"Assistant: {content}")

        # Add current prompt
        conversation_parts.append(f"Human: {current_prompt}")
        conversation_parts.append("Assistant:")

        # Join all parts with newlines
        full_prompt = "\n\n".join(conversation_parts)

        # Truncate if too long (keep last N characters to fit context window)
        max_context_chars = 8000
        if len(full_prompt) > max_context_chars:
            # Keep the current prompt and recent history
            truncated_prompt = "...\n\n" + full_prompt[-max_context_chars:]
            return truncated_prompt

        return full_prompt

    @staticmethod
    def optimize_image(image):
        """Optimize image for faster processing"""
        # Resize large images
        max_size = (512, 512)
        if image.size[0] > max_size[0] or image.size[1] > max_size[1]:
            image.thumbnail(max_size, Image.Resampling.LANCZOS)

        if image.mode != 'RGB':
            image = image.convert('RGB')

        return image