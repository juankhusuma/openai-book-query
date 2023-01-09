import polars as pl
import numpy as np
import openai
from openai.embeddings_utils import get_embedding, cosine_similarity
try:
    from constants import token
except ImportError:
    print("Credential has not been set")
openai.api_key = token

def load_data():
    try:
        df = pl.read_csv("./data.csv")
        df["vector"] = df["vector"].apply(eval).apply(np.array)
    except FileNotFoundError:
        print("Previous data not found, embedding dataset...")
        df = pl.read_csv("./dump/dataset.txt", sep="|")
        df["vector"] = df["vector"].apply(lambda _: []).apply(np.array)
        df = df.dropna()
        df['vector'] = df["text"].apply(lambda x: get_embedding(x, engine='text-embedding-ada-002'))
        print(df)
        df.to_csv("./data.csv")
    finally:
        return df


def query(df, query, n=3):
    search_query_embedding = get_embedding(
        query,
        engine="text-embedding-ada-002"
    )
    df['similarities'] = df["vector"].apply(lambda x: cosine_similarity(x, search_query_embedding))
    res = df.sort_values('similarities', ascending=False)["text"].head(n)
    return list(res)

if __name__ == '__main__':
    df = load_data()
    print(query(df, "good meditation"))
    print(query(df, "lobha"))