import boto3
import json
import logging
from botocore.exceptions import ClientError
import base64
import io
from PIL import Image
import matplotlib.pyplot as plt
import streamlit as st

logger = logging.getLogger(__name__)

class BedrockRuntimeWrapper:
    """Encapsulates Amazon Bedrock Runtime actions."""

    def __init__(self, bedrock_runtime_client):
        """
        :param bedrock_runtime_client: A low-level client representing Amazon Bedrock Runtime.
                                       Describes the API operations for running inference using
                                       Bedrock models.
        """
        self.bedrock_runtime_client = bedrock_runtime_client

    def invoke_stable_diffusion(self, prompt, seed, cfg_scale, style_preset=None):
            """
            Invokes the Stability.ai Stable Diffusion XL model to create an image using
            the input provided in the request body.

            :param prompt: The prompt that you want Stable Diffusion  to use for image generation.
            :param seed: Random noise seed (omit this option or use 0 for a random seed)
            :param style_preset: Pass in a style preset to guide the image model towards
                                a particular style.
            :return: Base64-encoded inference response from the model.
            """
            #seed - (Optional) Random noise seed (omit this option or use 0 for a random seed)
            #cfg_scale – (Optional) Determines how much the final image portrays the prompt. Use a lower number to increase randomness in the generation.
            #Generation step determines how many times the image is sampled. More steps can result in a more accurate result.
            try:
                body = {
                    "text_prompts": [{"text": prompt}],
                    "seed": seed,
                    "cfg_scale": cfg_scale,
                    "steps": 30,
                }

                if style_preset:
                    body["style_preset"] = style_preset

                response = self.bedrock_runtime_client.invoke_model(
                    modelId="stability.stable-diffusion-xl", body=json.dumps(body)
                )

                response_body = json.loads(response["body"].read())
                base64_image_data = response_body["artifacts"][0]["base64"]

                return base64_image_data

            except Exception as e:
                logger.debug(e)
                logger.error("Couldn't invoke Stable Diffusion XL")
                raise

def main():
    # Create an instance of BedrockRuntimeWrapper
    bedrock_runtime_client = boto3.client('bedrock-runtime')
    bedrock_wrapper = BedrockRuntimeWrapper(bedrock_runtime_client)

    st.title("Stable Diffusion Image Generation")

    # Call the invoke_stable_diffusion function
    prompt = st.text_input("Enter your prompt", "Generate an image of a car")
    # desribe what a seed value is
    st.write("""Seeds play a crucial role in stable diffusion, serving as the starting point for the image 
                generation process. With different seed values, you can produce various variations of the image, 
                each influencing the quality of the final result. In fact, the seed parameter is the most important 
                factor in the diffusion algorithm, as it determines the reproducibility of the images. 
                By manipulating the seed values, you can control the outcome and create unique visualizations.""")
    
    seed = st.number_input("Enter the seed value", value=0, step=1, format="%d")
    st.write("The cfg_scale parameter determines how much the final image portrays the prompt.")
    cfg_scale = st.number_input("Enter the cfg_scale value", value=0, step=1, format="%d")
    
    st.write("Style presets are a set of predefined styles that can be applied to the image generation process.")
    # Add a select drop down menu for style_preset
    style_preset_options = [
        "3d-model", "analog-film", "anime", "cinematic", "comic-book", "digital-art",
        "enhance", "fantasy-art", "isometric", "line-art", "low-poly", "modeling-compound",
        "neon-punk", "origami", "photographic", "pixel-art", "tile-texture"
    ]
    style_preset = st.selectbox("Select a style preset", style_preset_options)

    result = bedrock_wrapper.invoke_stable_diffusion(prompt, seed, cfg_scale, style_preset)
    
    # Assuming 'result' is your base64 string
    img_bytes = base64.b64decode(result)
    img = Image.open(io.BytesIO(img_bytes))

    # Display the image
    st.image(img)

if __name__ == "__main__":
    main()
    # Generate three images based on the prompt
   