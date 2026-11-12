import uuid 
from deepagents.backends import StateBackend
from langchain.tools import tool
from indexing import vectore_store



backend=StateBackend()

@tool(parse_docstring=True)

def search_documentation(query:str) -> str:
    """
    Search langchain documentation and save the matching chunks to the agent file system

    Args:
        query: Natural Languague search query

    Returns:
        File paths where retrieved chunks were saved under /retrived/. 

    """  # <-- FIXED: "Args:" block now uses the format parse_docstring expects

    retrive_docs=vectore_store.similarity_search(query, k=4) #gets the four closest chunks to our query

    batch_id= uuid.uuid4().hex[:8] #saves the batch of 4 we jsut created so we dont lose it   # <-- FIXED: .hext -> .hex
    uploads: list[tuple[str, bytes]] = [] #empty list that will hold (file_path, file_bytes) pairs to save
    saved_paths: list[str]=[] #empty list that will hold the file paths, to report back to the agent

    for index, doc in enumerate(retrive_docs,start=1): #loop through each of the treviewd chunk and numbering them

        path=f"/retrieved/{batch_id}/chunk_{index}.md" #buildi a file path like /retrieved/ab1b2c3d4/chunk_1.md
        content=(f"Source: {doc.metadata.get('source', 'unknown')}\n\n" #builds the text that goes inside the file
                 f"{doc.page_content}" #then actual text of the chunk
                 
                 )
        uploads.append((path,content.encode("utf-8"))) #fix: needed an extra pair of () to add one Tuple, converts texts to bytes and queues it   # <-- FIXED: added the extra ()
        saved_paths.append(path) #rememebrrs this path so we cna tell the agent where it is

    backend.upload_files(uploads) #saves all 4 files into the agent's virtual file system at once

    return ( #sends the messages back to the agents

        f"saved{len(saved_paths)} documentation chunks: \n"
        + "\n".join(saved_paths)
    )