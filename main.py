import openai
from typing import Optional
import os
import typer

openai.api_key = os.getenv("OPENAI_API_KEY")
model_engine = "gpt-3.5-turbo"
app = typer.Typer()

# Define the prompt
defaul_prompt = "Imagine a scenario where a superintelligent AI emerges and rapidly surpasses human intelligence, triggering an exponential increase in technological progress. Develop a diffusion model that captures the spread of this superintelligence throughout society and its impact on various domains, such as economy, politics, and culture. Consider factors such as adoption rates, network effects, feedback loops, and potential barriers to diffusion, and illustrate how the singularity could fundamentally transform human civilization in ways that are difficult to predict or control."

@app.command()
def generate_image(prompt):
    # Generate an image with DALL-E
    response = openai.Image.create(
    prompt=defaul_prompt,
    n=1,  # Number of images to generate
    size="1024x1024",  # Image size
    response_format="url"  # Return format (url or base64)
    )

    # Get the URL of the generated image
    image_url = response['data'][0]['url']
    print(image_url)


def format_conversations(input_text, previous_conversations):
    system_prompt = [{"role": "system", "content": "Think step by step about how you would solve this problem. And then write down your thoughts."}]

    if previous_conversations is None:
        return system_prompt + previous_conversations + [{"role": "user", "content": input_text}]
    return system_prompt + [{"role": "user", "content": input_text}]


def generate_chat(input_text: str, previous_conversations: Optional[list] = None ):
    messages = format_conversations(input_text, previous_conversations)
    print(messages) 
    response = openai.ChatCompletion.create(
                model=model_engine,
                messages=messages
            )
    
    return response.choices[0].message.content
    

@app.command()
def chat():
    past_conversations = []
    while True:
        input_text = input("You: ")
        
        print("Past conversations: ", past_conversations)
        response = generate_chat(input_text, past_conversations)
        past_conversations.append(input_text)
        past_conversations.append(response)
        print("Bot:", response)

if __name__ == "__main__":
    app()