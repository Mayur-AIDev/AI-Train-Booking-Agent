import os
from dotenv import load_dotenv
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

load_dotenv()
My_Token = os.environ.get("Hugging_face_ApI")

# Switch to Qwen-2.5-7B-Instruct: No gating rules, fully public model
llm_endpoint = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen2.5-7B-Instruct",
    task="text-generation",
    temperature=0.1,
    huggingfacehub_api_token=My_Token
)

# Initialize the chat engine instance cleanly
llm = ChatHuggingFace(llm=llm_endpoint)
