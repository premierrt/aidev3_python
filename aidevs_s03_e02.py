from aidevs3_lib_rt import *


# docker run -p 6333:6333 -v $(pwd)/qdrant_storage:/qdrant/storage qdrant/qdrant
# z tutoriala qdrant:
# https://qdrant.tech/documentation/quick-start/
#   
#
# https://qdrant.tech/documentation/embeddings/openai/
#
# https://cookbook.openai.com/examples/vector_databases/qdrant/using_qdrant_for_embeddings_search

raport_file_path="/home/rafal/Pobrane/pliki_z_fabryki_2/do-not-share"



if __name__ == "__main__":
  fileNames =  get_files_by_extension(raport_file_path, ".txt")
  slownik = load_files_to_dictionary (raport_file_path, fileNames)
  #for key, value in slownik.items():
   # print(key, value)