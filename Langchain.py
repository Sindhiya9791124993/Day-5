import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda

# Set your Google Gemini API key
os.environ["GOOGLE_API_KEY"] = "AIzaSyCZ5V3tJG4Cq2RTp7PM5WQTrTXiwLngNNQ"

# Load Gemini model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.3,
    convert_system_message_to_human=True
)

# ChainLang prompt using ChatPromptTemplate
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a professional translator that translates English to French."),
    ("user", "Translate the following English sentence to French: {input}")
])

# Use ChainLang syntax to compose the chain
# This is the LCEL equivalent of `chain = prompt | llm`
chain = prompt | llm

# Streamlit UI
st.set_page_config(page_title="ChainLang Translator", page_icon="🌐")
st.title("🌐 ChainLang: English ➜ French Translator")
st.markdown("Enter an English sentence and click **Translate** to get the French translation.")

# User input
input_text = st.text_input("Enter English Sentence:")

# Translate on button click
if st.button("Translate"):
    if not input_text.strip():
        st.warning("Please enter a sentence.")
    else:
        try:
            # Invoke the chain
            result = chain.invoke({"input": input_text})
            translation = result.content if hasattr(result, "content") else str(result)
            st.success("Translation Successful ✅")
            st.text_area("French Translation:", value=translation, height=100)
        except Exception as e:
            st.error(f"Error: {e}")
