from aidevs3_lib_rt import *
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from qdrant_client.models import VectorParams, Distance




# docker run -p 6333:6333 -v $(pwd)/qdrant_storage:/qdrant/storage qdrant/qdrant
#
# http://localhost:6333/dashboard#/
# z tutoriala qdrant:
# https://qdrant.tech/documentation/quick-start/
#   
#
# !!! https://qdrant.tech/documentation/embeddings/openai/
#
# https://cookbook.openai.com/examples/vector_databases/qdrant/getting_started_with_qdrant_and_openai
#
# https://cookbook.openai.com/examples/vector_databases/qdrant/using_qdrant_for_embeddings_search

raport_file_path="/home/rafal/Pobrane/pliki_z_fabryki_2/do-not-share"
question = "W raporcie, z którego dnia znajduje się wzmianka o kradzieży prototypu broni?"


def populateQdrantDB(client, embedning_results_dict, oryginal_texts, collection_name):
    points = []
    for idx, ((file_name_embedding, value1), (file_name_oryginal_text, value2)) in enumerate(zip(embedning_results_dict.items(), oryginal_texts.items())):
        vector_data = value1  # Upewnij się, że to jest poprawne
        print(vector_data)
        points.append(
            PointStruct(
                id=idx,
                vector=vector_data,  # Użyj wektora jako listy float
                payload={"text": value2, "data_raportu": remove_extension(file_name_oryginal_text, ".txt")}
            )
        )

    client.create_collection(
       collection_name,
       vectors_config=VectorParams(
       size=1536,
       distance=Distance.COSINE,
       ),
    )
    client.upsert(collection_name, points)


def embed_all_texts(slownik: dict):
    embeddings = {}
    for filename, text in slownik.items():
        embedding_result = do_embedding(text)  # Wywołanie metody do_embedding dla każdej wartości
        embeddings[filename] = embedding_result
 # Przechowywanie wyników w nowym słowniku
    return embeddings


def populateData():
    client = QdrantClient(url="http://localhost:6333")
    fileNames = get_files_by_extension(raport_file_path, ".txt")
    slownik = load_files_to_dictionary(raport_file_path, fileNames)
    embeddings = embed_all_texts(slownik)  # Wywołanie funkcji do embeddingu
    collection_name="aidev3_s03e02"
    populateQdrantDB(client, embeddings, slownik, collection_name)  # Przekazywanie wyników do funkcji populateQdrantDB


def queryData():
   embedded_question = do_embedding(question)
   client = QdrantClient(url="http://localhost:6333")
   search_result = client.query_points(
        collection_name="aidev3_s03e02",
        query=embedded_question,
        with_payload=True,
        limit=2
    ).points
   print(search_result)


def check_points_exist(collection_name):
    client = QdrantClient(url="http://localhost:6333")
    
    # Sprawdzenie, czy kolekcja istnieje
    try:
        collection_info = client.get_collection(collection_name)
        print(f"Kolekcja '{collection_name}' istnieje.")
        
        # Zapytanie o punkty w kolekcji
        search_result = client.query_points(
            collection_name=collection_name,
            query=[0.0] * 1536,  # Przykładowe zapytanie z wektorem zerowym
            limit=1  # Ograniczenie do 1 punktu
        )
        
        if search_result.points:
            print("Punkty istnieją w kolekcji.")
        else:
            print("Kolekcja jest pusta.")
    
    except Exception as e:
        print(f"Wystąpił błąd: {e}")






if __name__ == "__main__":
   #check_points_exist("aidev3_s03e02")
 #  queryData()
 send_answer("2024-02-21", "wektory")
    
  