import streamlit as st
import requests

PROMPT_TEMPLATE = """[INST] <<SYS>>
You are a code quality assistant. Analyze this Python code and provide specific feedback:
1. Identify 3 potential improvements
2. Note any style violations (PEP8)
3. Suggest performance optimizations
4. Mention line numbers for each suggestion
<</SYS>>

{code}[/INST]"""

def get_code_review(code, model_name):
    API_URL = f"https://api-inference.huggingface.co/models/{model_name}"
    headers = {"Authorization": "Bearer hf_anonymous"}

    payload = {
        "inputs": PROMPT_TEMPLATE.format(code=code),
        "parameters": {
            "max_new_tokens": 1024,
            "temperature": 0.2,
            "return_full_text": False
        }
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()[0]['generated_text']
        return f"Error: {response.text}"
    except Exception as e:
        return f"API Error: {str(e)}"

def main():
    st.set_page_config(page_title="Cloud Code Review", page_icon="☁️")
    st.title("☁️ Cloud Code Reviewer")
    
    model_name = st.selectbox(
        "Select Model",
        options=[
            "bigcode/starcoder2-3b",
            "codellama/CodeLlama-7b-instruct-hf",
            "HuggingFaceH4/zephyr-7b-beta"
        ]
    )
    
    uploaded_file = st.file_uploader("Upload Python File", type=["py"])
    
    if uploaded_file:
        code = uploaded_file.read().decode()
        
        with st.expander("View Uploaded Code"):
            st.code(code, language='python')
            
        if st.button("Analyze Code"):
            with st.spinner("Analyzing with cloud model..."):
                review = get_code_review(code, model_name)
                st.subheader("Code Review Results")
                st.markdown(review)

if __name__ == "__main__":
    main()
