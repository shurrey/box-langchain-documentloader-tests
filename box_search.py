import os

from langchain_community.llms import OpenAI

from langchain_community.vectorstores import Chroma
from langchain_community.vectorstores import utils as chromautils

from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings

from dotenv import load_dotenv

class BoxSearch:
    def __init__(self):
        load_dotenv("config/.openai.env")

        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.db = None
        self.compressor = None
        self.compression_retriever = None
        self.is_trained = False

    def train_ai(self, documents):

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
        text_chunks = text_splitter.split_documents(documents)

        embeddings = OpenAIEmbeddings(openai_api_key=self.openai_key)

        filter_chunks = chromautils.filter_complex_metadata(text_chunks)
        self.db = Chroma.from_documents(filter_chunks, embeddings, persist_directory='./chroma_db')

        llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key=self.openai_key)
        self.compressor = LLMChainExtractor.from_llm(llm)
        self.compression_retriever = ContextualCompressionRetriever(base_compressor=self.compressor,
                                                                    base_retriever=self.db.as_retriever())
        
        self.is_trained = True
        
    def box_search(self, question):

        if not self.is_trained:
            raise Exception("AI Model is not trained. Please run train_ai first.")
        
        compressed_docs = self.compression_retriever.invoke(question)

        if compressed_docs:
            return compressed_docs[0].page_content
        else:
            return f"No relevant documents found for {question}"