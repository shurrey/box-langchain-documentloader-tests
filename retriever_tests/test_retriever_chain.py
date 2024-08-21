import os
from dotenv import load_dotenv

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

from langchain_box.retrievers import BoxRetriever
from langchain_openai import ChatOpenAI

load_dotenv("../config/.token.env")
load_dotenv("../config/.openai.env")

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

box_developer_token=os.getenv("BOX_DEVELOPER_TOKEN")

llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)

retriever = BoxRetriever(box_developer_token=box_developer_token, character_limit=10000)

context="You are an actor reading scripts and looking for all of your lines."
question="describe the character Victor"

prompt = ChatPromptTemplate.from_template(
    """Answer the question based only on the context provided.

    Context: {context}

    Question: {question}"""
)


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

answer = chain.invoke("victor")

print(f"answer {answer}")