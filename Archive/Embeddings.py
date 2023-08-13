
import argparse
from llama_index import StorageContext, load_index_from_storage, SimpleDirectoryReader, VectorStoreIndex
import fpdf
import openai 

parser = argparse.ArgumentParser(description="Embeddings creation tool",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-s", "--store", type=str, help="Which store to access for given app name. Options are play_store and app_store")
parser.add_argument("-n", "--name", help="App name")
parser.add_argument("-p", "--prompt", help="Prompt to query here")
args = parser.parse_args()
config = vars(args)
print(config)

AppName = config["name"]
Store = config["store"]
Prompt = config["prompt"]

def Embeddings(AppName, Prompt):

    openai.api_key= "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"

    try:
        print("Attempting to load index from storage")
        storage_context = StorageContext.from_defaults(persist_dir="./Storage-" + Store + "-" + AppName)
        index = load_index_from_storage(storage_context)
        print("Loaded index from storage")
    except:
        print("Failed to load index from storage, creating new index")
        documents = SimpleDirectoryReader(input_files=["Comments-" + Store + "-" +
                                                        AppName + ".pdf"]).load_data()
        index = VectorStoreIndex.from_documents(documents)
        print("Created new index")
        index.storage_context.persist(persist_dir="./Storage-" + Store + "-" + AppName)

    query_engine = index.as_query_engine()
    response = query_engine.query(Prompt)

    pdf2 = fpdf.FPDF(format='letter')
    pdf2.add_page()
    pdf2.set_font("Arial", "",  size=10)

    print(response)

    text = str(response)
    review = text.encode('latin-1', 'replace').decode('latin-1')
    pdf2.write(12, review) 
    pdf2.ln()

    pdf2.output("Analysis-" + Store + "-" + AppName + ".pdf")

    

Embeddings(AppName, Prompt)