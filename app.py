import streamlit as st
import ast
import replicate

from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()  

# Fetch the API key
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")


# Initialize session_state
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Home"

# Function to navigate to a page
def navigate(page_name):
    st.session_state.current_page = page_name

#Ast function for python
def analyse_python_code(code):
    try:
        tree = ast.parse(code)
        return "✅ No syntax errors found!", "success"
    except SyntaxError as e:
        error_msg = f"❌ Syntax Error on line {e.lineno}: {e.msg}"
        return error_msg,"error"
    
def fix_code_with_ai(code, language="Python"):
    """Uses AI to explain and fix bugs in code"""
    try:
        prompt = f"""
        [INST] <<SYS>>
        You are a {language} coding expert. Follow these steps:
        1. Identify all bugs in this code
        2. Explain each bug in simple terms
        3. Show the corrected code
        4. Add brief improvement suggestions
        <</SYS>>

        Code to debug:
        ```{language.lower()}
        {code}
        ```
        [/INST]
        """

        output = replicate.run(
             "meta/llama-2-7b-chat:13c3cdee13ee059ab779f0291d29054dab00a47dad8261375654de5540165fb0",
            input={
                "prompt": prompt,
                "max_tokens": 300,
                "temperature": 0.3  # Lower = more precise fixes
            }
        )
        return "".join(output)
    except Exception as e:
        return f"⚠️ AI Debugging Failed: {str(e)}"


with st.sidebar:
    st.title("Explore CodeSage")
    
    if st.button("🔧 Debug Code"):
        navigate("Debug Code")
    if st.button("📜 About App"):
        navigate("About App")
    if st.button("✨ Features"):
        navigate("Features")
st.markdown(
    """
    <style>
    /* Button Styling */
    div.stButton > button {
        background-color: #7F00FF; /* A rich purple */
        color: white;
        border: None;
        padding: 10px 20px;
        border-radius: 12px;
        font-size: 18px;
        font-weight: bold;
        transition: 0.3s;
    }

    /* Hover effect */
    div.stButton > button:hover {
        background-color: #9b59b6; /* lighter purple on hover */
        color: black;
        transform: scale(1.05);
    }
    </style>
    """,
    unsafe_allow_html=True
)
    

# Render based on current_page
if st.session_state.current_page == "Home":
    
    st.image("logoo.jpeg",width = 400)
    
    #st.title("your AI powered code debugger mentor")
    
    
#     st.markdown(
#     """
#     <style>
#     body {
#         background-color: #c8a2c8; /* Your dark purple background */
#         font-family: 'Poppins', sans-serif;
#         color: #FFFFFF; /* White text for dark background */
#     }
#     .stApp {
#         background-color: #c8a2c8;
#     }
#     </style>
#     """
#     unsafe_allow_html=True
# )
    st.markdown("""
    <div style="background-color: #c8a2c8; padding: 20px; border-radius: 10px;">
        <h3>your AI powered code debugger mentor</h3>
        
    </div>
     """, unsafe_allow_html=True)

    
    

    
# Debug Code Page
elif st.session_state.current_page == "Debug Code":
    st.header("Debug Your Code")
    if st.button("⬅️ Back to Home"):
        navigate("Home")

    language = st.selectbox(
        "Select Programming Language",
        ("Python", "C++", "Java", "JavaScript", "C#", "Go", "Ruby", "PHP")
    )
    code_input = st.text_area(f"Paste your {language} code here", height=300)
    #if code_input:
        #st.subheader("Analysis Result")
        #st.info("AI Debugging feature coming soon...")
    if st.button("Debug Code"):
        st.subheader("Analysis Result")
        if code_input.strip == "":
            st.warning("Please paste some code before debugging!")
        else:
            with st.spinner("Analyzing code..."):
                # Basic syntax check
                if language == "Python":
                    analysis_msg, _ = analyse_python_code(code_input)
                    st.text(analysis_msg)
                
                # AI Debugging
                st.subheader("AI Debugging Results")
                ai_response = fix_code_with_ai(code_input, language)
                st.text(ai_response)

# About App Page
elif st.session_state.current_page == "About App":
    st.header("About CodeSage")
    if st.button("⬅️ Back to Home"):
        navigate("Home")
    st.markdown("""
    <div style="background-color: #c8a2c8; padding: 20px; border-radius: 10px;">
        <h3>About the app</h3>
        <p>CodeSage is an AI-powered debugging assistant built to help developers
    quickly find and fix bugs across multiple programming languages.</p>
    </div>
     """, unsafe_allow_html=True)

    

# Features Page
elif st.session_state.current_page == "Features":
    st.header("Features")
    if st.button("⬅️ Back to Home"):
        navigate("Home")
   
    st.markdown("""
    <div style="background-color: #c8a2c8; padding: 20px; border-radius: 10px;">
        <h3>Features</h3>
        <ul>
            <li>Instant error identification with plain-language explanations from AI.</li>
            <li>AI offers easy-to-follow fixes, aiding quick learning and application.</li>
            <li>AI integrates with beginner-friendly tools, easing the learning curve.</li>
            <li>Gain coding insights and tips from AI for continual skill improvement.</li>
            <li>Build coding confidence with AI-assisted code optimization.</li>
        </ul>
    </div>
     """, unsafe_allow_html=True)

    

