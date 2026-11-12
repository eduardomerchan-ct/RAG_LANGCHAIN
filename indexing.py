from langchain_core.vectorstores import InMemoryVectorStore
from langchain_voyageai import VoyageAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from filereader import read_multiple_pdfs

load_dotenv()


embedding = VoyageAIEmbeddings(model="voyage-3.5")#sets the embedding model to turn the text 


vectore_store=InMemoryVectorStore(embedding) #creates an empty vectory storage that uses the previous mode;

DOC_PATHS=[ #the list of pdfs we weill search and ask questions on later
    "pdfs/syllabus_2026fall_v1.pdf",
    "pdfs/CSE3150-Syllabus-Fall-2026(1).pdf"

]

docs=read_multiple_pdfs(DOC_PATHS) #reads each pdf and creates one document per peft


#this sets up the splitter each chunk is at most 1000 characters and  each chunk repeats atleast 200 of the previous one
text_splitter= RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)


all_splits=text_splitter.split_documents(docs) #cuts every document into theri own small chunks(each chunk keeps the "source")

print(f'split documentation into {len(all_splits)} chunks') #shows how many chunks we made

vectore_store.add_documents(documents=all_splits) #sends each chunk to voyage to get the vector and then stores the chunk and the vector point

print(f'indexed {len(all_splits)} chunks') #makes sure evething is serachble