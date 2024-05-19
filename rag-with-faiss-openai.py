#import Essential dependencies
import streamlit as sl
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from creds import get_it


#function to load the vectordatabase
def load_knowledgeBase():
        embeddings=OpenAIEmbeddings(api_key="sk-jasonkeygoeshere")
        DB_FAISS_PATH = './db_faiss'
        db = FAISS.load_local(DB_FAISS_PATH, embeddings, allow_dangerous_deserialization=True)
        return db
        
#function to load the OPENAI LLM
def load_llm(temperature, top_p):
        from langchain_openai import ChatOpenAI
        llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=temperature, top_p=top_p, api_key=get_it.openai_api_key)
        return llm

#creating prompt template using langchain
def load_prompt():
        prompt = """You need to answer the question in the sentence as same as in the  pdf content. . 
        Given below is the context and question of the user.
        context = {context}
        question = {question}
        if the answer is not in the pdf answer "i do not know what the hell you are asking about"
         """
        prompt = ChatPromptTemplate.from_template(prompt)
        print(prompt)
        return prompt


def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)


if __name__=='__main__':
        sl.header("welcome to the 📝text RAG bot")
        sl.write("🤖 You can chat by Entering your queries ")
        temperature = sl.selectbox('Temperature', [0.2, 0.5, 1.0, 1.5, 2.0], index=2)
        top_p = sl.selectbox('Top P', [0.2, 0.5, 0.8, 1.0], index=1)
        chatgpt_model = sl.selectbox('ChatGPT Model', ['gpt-3.5-turbo', 'gpt-4', 'gpt-4-0125-preview'], index=0)

        knowledgeBase=load_knowledgeBase()
        llm=load_llm(temperature, top_p)
        prompt=load_prompt()
        
        query=sl.text_input('Enter some text')
        

        
        if(query):
                #getting only the chunks that are similar to the query for llm to produce the output
                similar_embeddings=knowledgeBase.similarity_search(query)
                similar_embeddings=FAISS.from_documents(documents=similar_embeddings, embedding=OpenAIEmbeddings(api_key=get_it.openai_api_key))
                
                #creating the chain for integrating llm,prompt,stroutputparser
                retriever = similar_embeddings.as_retriever()
                rag_chain = (
                        {"context": retriever | format_docs, "question": RunnablePassthrough()}
                        | prompt
                        | llm
                        | StrOutputParser()
                )
                
                response=rag_chain.invoke(query)
                print(response)
                sl.write(response)
                
        
        
        
        