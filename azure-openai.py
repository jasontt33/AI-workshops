
from openai import AzureOpenAI
import streamlit as st
from creds import get_it


def send_to_openai(selected_model, messages, temp, p_val, max_tokens):
    ''' 
    Docstring: This function sends the messages to the OpenAI API and returns the chat text
    selected_model: The llm model you want to use
    messages: The messages you want to send to the API
    temp: The temperature value for the API which determines how random the chat is
    p_val: The p value for the API, or I think the volume of the chat that is considered in the output
    '''
    # Configure Azure OpenAI Service API
    client = AzureOpenAI(
        azure_endpoint=get_it.azure_openai_endpoint,
        api_key=get_it.azure_openai_api_key,
        api_version=get_it.azure_openai_version
    )
    
    try:
        chat = client.chat.completions.create(
            model=selected_model,
            messages=messages,
            temperature=temp,
            max_tokens=max_tokens,
            top_p=p_val,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None
        )
        
        # Assuming 'chat' is your ChatCompletion object
        completion_tokens = chat.usage.completion_tokens
        prompt_tokens = chat.usage.prompt_tokens
        total_tokens = chat.usage.total_tokens

        print(f"Completion Tokens: {completion_tokens}")
        print(f"Prompt Tokens: {prompt_tokens}")
        print(f"Total Tokens: {total_tokens}")
        
        content = chat.choices[0].message.content

        return content, completion_tokens, prompt_tokens, total_tokens
    except Exception as e:
        print(e)
        return "Error with OpenAI server, please try again later"
        


def ask_question():
    ## add a title to the page
    st.title("ChatGPT with Azure OpenAI")
    

    # Display a help menu for users to understand the benefits of each model
    st.subheader("The following models are available:")
    st.write("- GPT-4: The latest and greatest model from OpenAI but can be slow")
    st.write("- GPT-4-32K: A larger version of GPT-4 but is also slow and can be expensive in terms of tokens used")
    st.write("- GPT-35-16k: A larger version of GPT-35 but still very fast")
    st.write("- GPT-35: The fastest model available")

    
    selected_model = st.selectbox("Select Model", ["GPT-4", "GPT-4-32K", "GPT-35-16k", "GPT-35"], index=3)
    if selected_model == "GPT-4" or selected_model == "GPT-35":
        max_tokens = st.slider("Max Tokens", 0, 4000, 1200, 100)
    elif selected_model == "GPT-35-16k":
        max_tokens = st.slider("Max Tokens", 0, 8000, 2048, 100)
    elif selected_model == "GPT-4-32K":
        max_tokens = st.slider("Max Tokens", 0, 16000, 4096, 100)

    st.write("")
    st.subheader("Temperature")
    st.write("🤖 Temperature is how random the chat is. Higher scores are more random while lower scores are more predictable")
    temperature = st.slider("Temperature", 0.0, 1.0, 0.5, 0.1)
    st.write("")
    st.subheader("Top P")
    st.write("🤖 Top P is the probability of the chat that is considered in the output. Higher scores are more verbose while lower scores are more concise")
    top_p = st.slider("Top P", 0.0, 1.0, 0.9, 0.1)
    st.write("")
    st.write("Please enter your question below:")
    query = ""
    
    if selected_model in ["GPT-4-32K", "GPT-35-16k"]:
        query = st.text_area("", query, height=500)  # Use st.text_area instead of st.text_input
    else:
        query = st.text_input("", query)

    if query:  # Only run when the user has entered a question
        messages = [
            {"role": "system", "content": "You are a smart and friendly AI assistant ready to assist in finding answers to this question: \n\n"},
        ]
        messages.append({"role": "user", "content": query})

      
        with st.spinner("Waiting for API response..."):
            chat, completion_tokens, prompt_tokens, total_tokens = send_to_openai(selected_model=selected_model, messages=messages, temp=temperature, p_val=top_p, max_tokens=max_tokens)
        st.success("API response received!")

        st.write(chat)
        ## display token useage below
        st.write(f"Completion Tokens: {completion_tokens}")
        st.write(f"Prompt Tokens: {prompt_tokens}")
        st.write(f"Total Tokens: {total_tokens}")
        ## calculate the cost of the chat
        if selected_model == "GPT-35" or selected_model == "GPT-35-16k":
            cost = 0.00002 * total_tokens
        elif selected_model == "GPT-4":
            cost = 0.00006 * total_tokens
        elif selected_model == "GPT-4-32K":
            cost = 0.00012 * total_tokens
        st.write(f"Cost of chat: ${cost:.2f}")
    else:
        st.write("Please enter a question before submitting.")

if __name__ == "__main__":
    ask_question()
