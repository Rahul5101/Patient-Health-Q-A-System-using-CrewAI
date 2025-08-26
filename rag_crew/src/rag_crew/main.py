#!/usr/bin/env python
import sys
import warnings
from crew import RagCrew
from rag_crew.src.rag_crew.tools.custom_tool import BM25ChunkRetrieverTool
import os 

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

# langfuse = Langfuse(
#     public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
#     secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
#     host = "http://localhost:3000"
# )


def run(query: str) -> str:
    """
    Run the crew.
    """
    # inputs = {
    #     # 'query': 'what is the history of patient during visits?',
    #     'query': 'how to spread awareness about cancer ?',
    #     # 'query': 'what is the symptoms of typhoid ?',
    #     # 'query' : 'what are the things a woman care about during pregnency'
        
    # }
    
   
    # return RagCrew().crew().kickoff(inputs=query)

    # langfuse = get_client()

    # langfuse.update_current_trace(session_id="session_01",user_id="user_5102")

    # prompt = langfuse.get_prompt("prompt1")
    # compiled_prompt = prompt.compile(query="What is the benifits of doing yoga in morning ?")

    return RagCrew().crew().kickoff(inputs={"query": query})    
#  

# # run()




