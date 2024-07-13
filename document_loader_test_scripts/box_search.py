import bs4
import os
from langchain import hub
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv

class BoxSearch:
    def __init__(self):
        load_dotenv("../config/.openai.env")

        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.db = None
        self.compressor = None
        self.compression_retriever = None
        self.llm = ChatOpenAI(model="gpt-3.5-turbo-0125")
        self.prompt = None
        self.is_trained = False

    def format_docs(self,docs):
        return "\n\n".join(doc.page_content for doc in docs)
    
    def train_ai(self, docs):

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(docs)
        self.db = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())

        # Retrieve and generate using the relevant snippets of the blog.
        self.retriever = self.db.as_retriever(search_kwargs={"k": 1})
        self.prompt = hub.pull("rlm/rag-prompt")
        
        self.is_trained = True
        
    def box_search(self, question):

        if not self.is_trained:
            raise Exception("AI Model is not trained. Please run train_ai first.")
        
        rag_chain = (
            {"context": self.retriever | self.format_docs, "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

        answer = rag_chain.invoke(question)

        return answer