from pinecone.grpc import PineconeGRPC as Pinecone
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from a .env file

# 1. Prepare clients
pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
index = pc.Index(host=os.environ["PINECONE_INDEX_HOST_ADDRESS"])
oai = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def search_index_gdpr(query: str):
    """Search th vector index for the given query and return the top result.
        Use this for RAG (Retrieval Augmented Generation), for GDPR Related queries."""
    # 2. Embed your query
    embed_model = os.environ.get("OPENAI_EMBED_MODEL", "text-embedding-3-small")
    query_vec = oai.embeddings.create(model=embed_model, input=[query]).data[0].embedding

    # 3. Query Pinecone
    results = index.query(
        vector=query_vec,
        top_k=1,
        namespace=os.environ.get("NAMESPACE", "__default__"),
        include_metadata=True
    )

    # 4. Print results
    for match in results.matches:
        print(f"Score: {match.score:.3f}")
        print(f"Source: {match.metadata.get('source')}")
        print(f"Text: {match.metadata.get('text')}...\n")
        return match.metadata.get('text')
    return None