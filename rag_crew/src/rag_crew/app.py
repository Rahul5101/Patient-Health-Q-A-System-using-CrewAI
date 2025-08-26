import streamlit as st
from main import run

st.set_page_config(page_title="Agentic Rag App",layout ="centered")

st.title("Query Generator using CrewAI")
st.write("Ask me anythink related to pkl file and I'll run full AI workflow to get you answer")

query = st.text_input("Enter your Query")

if st.button("Run Workflow"):
    if query.strip():
        with st.spinner("Running the agentic workflow.....please wait"):
            final_answer= run(query)
            st.success("here's the final answer")
            st.write(final_answer)
    else:
        st.warning("please enter the query first")
        