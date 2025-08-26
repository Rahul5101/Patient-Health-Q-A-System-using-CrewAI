
import os
import pickle
from typing import List, Union
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_core.documents import Document
from crewai.tools.base_tool import BaseTool
from langchain_community.retrievers import BM25Retriever
from langfuse import Langfuse
from langfuse import observe
# from langsmith import traceable
# from langsmith.wrappers import wrap_openai
# from openai import OpenAI
# openai_client = wrap_openai(OpenAI())

load_dotenv()
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

def add_ids_to_documents(docs: List[Document]) -> List[Document]:
    
    fixed_docs = []
    for i, doc in enumerate(docs):
        new_metadata = dict(doc.metadata)
        new_metadata["id"] = f"doc_{i}"
        fixed_docs.append(Document(page_content=doc.page_content, metadata=new_metadata))
    return fixed_docs


class ChunkRetrievalInput(BaseModel):
    user_query: str = Field(..., description="The query to search for relevant context.")
    chunks: List[Union[Document]] = Field(..., description="Chunks of documents to search in.")



class BM25ChunkRetrieverTool(BaseTool):
    name: str = "BM25PatientChunkTool"
    description:str = (
        "Retrieves the most relevant patient document chunks from 'Chunks/patient_chunks.pkl' "
        "using the BM25 algorithm. Takes a search query as input."
    )
    def augment_query(self, query: str, n=5) -> List[str]:
        return [f"{query} variation {i+1}" for i in range(n)]
    
    @observe()
    def _run(self, user_query: str):
       
        file_path = r"C:\Users\rahul.g\Downloads\rahul\rahul\Chunks\patient_chunks.pkl"
        with open(file_path, "rb") as f:
            chunks = pickle.load(f)

        if chunks and isinstance(chunks[0], dict):
            chunks = [
                Document(page_content=c["page_content"], metadata=c.get("metadata", {}))
                for c in chunks
            ]
        chunk = add_ids_to_documents(chunks)
        retriever = BM25Retriever.from_documents(chunk)
        retriever.k = 5
        queries = self.augment_query(user_query,n=5)

        all_docs= []
        for q in queries:
            all_docs.extend(retriever.get_relevant_documents(q))
        
        seen = set()
        unique_document = [] 
        for doc in all_docs:
            content = getattr(doc, "page_content",str(doc))
            if doc.page_content not in seen:
                unique_document.append(doc)
                seen.add(doc.page_content)
            
        return "\n\n".join([doc.page_content for doc in unique_document])


        































# import os
# import pickle
# from typing import List, Type, Union
# from dotenv import load_dotenv
# from pydantic import BaseModel, Field, model_validator, PrivateAttr
# from langchain_core.documents import Document
# from crewai.tools.base_tool import BaseTool
# from langchain_community.retrievers import BM25Retriever


# load_dotenv()
# OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# def filter_empty_chunks(chunks: list) -> list:
#     """Remove chunks with no usable content."""
#     return [
#         c for c in chunks
#         if getattr(c, "page_content", "").strip()
#     ]

# def add_ids_to_documents(docs: List[Document]) -> List[Document]:
    
#     fixed_docs = []
#     for i, doc in enumerate(docs):
#         # Copy metadata to avoid mutating originals
#         new_metadata = dict(doc.metadata)
#         new_metadata["id"] = f"doc_{i}"
#         fixed_docs.append(Document(page_content=doc.page_content, metadata=new_metadata))
#     return fixed_docs


# from langchain_core.documents import Document
# from typing import List, Union

# def convert_to_document(raw_chunks: Union[List, dict]) -> List[Document]:
    
#     documents = []

#     if isinstance(raw_chunks, dict):
#         # Single document dict
#         documents.append(
#             Document(
#                 page_content=raw_chunks.get("page_content", ""),
#                 metadata=raw_chunks.get("metadata", {})
#             )
#         )

#     elif isinstance(raw_chunks, list):
#         for index, doc in enumerate(raw_chunks):
#             if isinstance(doc, Document):
#                 documents.append(doc)
#             elif isinstance(doc, dict):
#                 documents.append(
#                     Document(
#                         page_content=doc.get("page_content", ""),
#                         metadata=doc.get("metadata", {})
#                     )
#                 )
#             elif isinstance(doc, str):
                
#                 documents.append(
#                     Document(
#                         page_content=doc,
#                         metadata={"auto_generated": True}
#                     )
#                 )
#             else:
#                 raise TypeError(f"Invalid chunk format at index {index}: {type(doc)}")

#     else:
#         raise TypeError(f"Invalid raw_chunks type: {type(raw_chunks)}")

#     return documents






# class ChunkRetrievalInput(BaseModel):
#     user_query: str = Field(..., description="The query to search for relevant context.")
#     chunks: List[Union[Document]] = Field(..., description="Chunks of documents to search in.")

#     # @model_validator(mode="before")
#     # def validate_chunks_format(cls, values):
#     #     values["chunks"] = convert_to_document(values.get("chunks", []))
#     #     return values



# class PatientChunkLoaderTool(BaseTool):
#     name: str = "PatientChunkLoader"
#     description: str = "Loads patient_chunks.pkl file and returns a list of Document chunks."

#     def _run(self, **kwargs) -> List[Document]:
#         with open("./Chunks/patient_chunks.pkl", "rb") as f:
#             raw_chunks = pickle.load(f)
#         print(f"Raw chunks type: {type(raw_chunks)}") 
#         # chunks = convert_to_document(raw_chunks)
#         print(f"Loaded {len(raw_chunks)} chunks after conversion.")
#         # print(raw_chunks)
#         return raw_chunks




# class BM25ChunkRetrieverTool(BaseTool):
#     name: str = "BM25 Chunk Retriever"
#     description: str = (
#         "Retrieves and merges relevant contexts from provided document chunks. "
#         "It first augments the user query with variations, then retrieves top-ranked contexts "
#         "for each query using BM25, deduplicates and joins the results."
#     )
#     args_schema: Type[BaseModel] = ChunkRetrievalInput
#     _chunks: list = PrivateAttr(default_factory=list)

#     def __init__(self, chunks=None):
#         self._chunks = chunks if chunks is not None else []
#         super().__init__()

#     def augment_query(self, query: str, n=5) -> List[str]:
#         return [f"{query} variation {i+1}" for i in range(n)]

#     def _run(self, user_query: str, chunks: List[Document] = None) -> str:
    
#         if chunks is not None:
#             self._chunks = convert_to_document(chunks)
        

#         queries = self.augment_query(user_query, n=5)

#         chunks_with_ids  = add_ids_to_documents(self._chunks)
#         # print("First 5 raw chunks:", chunks_with_ids[:5])
#         retriever = BM25Retriever.from_documents(chunks_with_ids)
#         retriever.k = 3
#         all_docs = []
#         for q in queries:
#             all_docs.extend(retriever.get_relevant_documents(q))

  
#         seen = set()
#         unique_docs = []
#         for doc in all_docs:
#             content = getattr(doc, "page_content", str(doc))
#             if content not in seen:
#                 unique_docs.append(doc)
#                 seen.add(content)

#         return "\n\n".join([doc.page_content for doc in unique_docs])



# class LinkClassifierInput(BaseModel):
#     answer_text: str = Field(..., description= "The output text from the agent")

# class LinkClassifierTool(BaseTool):
#     name:str = "healthcare/caregiving Classifier"
#     description: str = "classifiy text as healthcare advice or caregiving advice and append relavent links."
#     args_schema: Type[BaseModel] = LinkClassifierInput
    
#     def _run(self,answer_text:str) -> str:
#         healthcare_keywords = ["symptom", "disease", "treatment", "diagnosis", "health", "medicine"]
#         caregiving_keywords = ["caregiver", "support", "elder care", "helping", "assisting", "taking care"]

#         patient = any(word in answer_text.lower() for word in healthcare_keywords)
#         caregiving =  any(word in answer_text.lower() for word in caregiving_keywords)

#         links = ["https://www.cdc.gov/", "https://www.nia.nih.gov/"]
#         if patient:
#             links.extend([
#                 "https://www.healthinaging.org/aging-health-a-z",
#                 "https://www.healthinaging.org/tools-and-tips?type=Tip&title=&field_tip_language_value=All&keyword="
#             ])
#         elif caregiving:
#             links.extend([
#                 "https://www.caregiveraction.org/toolbox/?_resource=caregiving-basics",
#                 "https://www.caregiver.org/caregiver-resources/all-resources/"
#             ])
            
#         final_output = f"{answer_text} \n suggested links: \n" + "\n".join(links)
#         return final_output










# if __name__ == "__main__":
#     loader = PatientChunkLoaderTool()
#     chunks = loader._run()
#     print(f"Loaded {len(chunks)} chunks.")

#     # if not chunks:
#     #     print("No chunks loaded. Exiting.")
#     #     exit()

#     retriever_tool = BM25ChunkRetrieverTool()
#     result = retriever_tool._run(
#         user_query="how to spread awareness about cancer?",
#         chunks=chunks
#     )

#     print("\nRetrieved context:\n")
#     # print(result)




























