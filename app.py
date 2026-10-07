import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, OpenAI
from langchain.chains.question_answering import load_qa_chain

# پیکربندی صفحه
st.set_page_config(page_title="AI Document Analyst", page_icon="📄", layout="wide")

def main():
    st.title("سیستم تحلیل هوشمند اسناد (RAG)")
    st.markdown("فایل خود را آپلود کنید و با استفاده از هوش مصنوعی، اطلاعات مورد نیازتان را استخراج کنید.")
    
    with st.sidebar:
        st.header("پیکربندی سیستم")
        api_key = st.text_input("OpenAI API Key:", type="password")
        pdf_file = st.file_uploader("فایل PDF را آپلود کنید", type="pdf")
        
    if pdf_file and api_key:
        with st.spinner("سیستم در حال خواندن و تحلیل وکتورهای فایل است..."):
            # ۱. استخراج متن از فایل
            pdf_reader = PdfReader(pdf_file)
            raw_text = "".join(page.extract_text() for page in pdf_reader.pages if page.extract_text())
            
            # ۲. خرد کردن متن برای پردازش در مدل زبانی
            text_splitter = CharacterTextSplitter(
                separator="\n", chunk_size=1000, chunk_overlap=200, length_function=len
            )
            chunks = text_splitter.split_text(raw_text)
            
            # ۳. ساخت پایگاه داده برداری (Vector DB) موقت
            embeddings = OpenAIEmbeddings(openai_api_key=api_key)
            vectorstore = FAISS.from_texts(chunks, embeddings)
            
        st.success("فایل با موفقیت پردازش و در حافظه برداری ذخیره شد.")
        
        # ۴. دریافت پرسش و استنتاج
        user_query = st.text_input("سوال خود را دقیقاً درباره محتوای همین سند بپرسید:")
        if user_query:
            with st.spinner("در حال جستجوی معنایی و تولید پاسخ..."):
                docs = vectorstore.similarity_search(user_query)
                llm = OpenAI(openai_api_key=api_key)
                chain = load_qa_chain(llm, chain_type="stuff")
                response = chain.run(input_documents=docs, question=user_query)
                
                st.markdown("### پاسخ استخراج‌شده:")
                st.info(response)
    else:
        st.warning("برای فعال‌سازی سیستم، API Key را وارد کرده و یک سند PDF آپلود کنید.")

if __name__ == '__main__':
    main()
