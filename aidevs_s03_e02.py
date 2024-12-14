from aidevs3_lib_rt import *
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from qdrant_client.models import VectorParams, Distance




# docker run -p 6333:6333 -v $(pwd)/qdrant_storage:/qdrant/storage qdrant/qdrant
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


def populateQdrantDB(client, embedning_results_dict, oryginal_texts, collection_name):
    points = []
    for idx, ((file_name_embedding, value1), (file_name_oryginal_text, value2)) in enumerate(zip(embedning_results_dict.items(), oryginal_texts.items())):
        points.append(
            PointStruct(
                id=idx,
                vector=value1['embedding'],
                payload={"text": value2, "data_raportu": remove_extension (file_name_oryginal_text)}
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
        embeddings[filename] = embedding_result  # Przechowywanie wyników w nowym słowniku
    return embeddings


if __name__ == "__main__":
    client = QdrantClient(url="http://localhost:6333")
    fileNames = get_files_by_extension(raport_file_path, ".txt")
    slownik = load_files_to_dictionary(raport_file_path, fileNames)
    embeddings = embed_all_texts(slownik)  # Wywołanie funkcji do embeddingu
    collection_name="aidev3_s03e02"
    populateQdrantDB(client, embeddings, slownik, collection_name)  # Przekazywanie wyników do funkcji populateQdrantDB