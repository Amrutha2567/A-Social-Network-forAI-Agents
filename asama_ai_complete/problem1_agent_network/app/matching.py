import re
from functools import lru_cache
import numpy as np
from .config import EMBEDDING_MODEL
@lru_cache(maxsize=1)
def model():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer(EMBEDDING_MODEL)
def tokens(s): return set(re.findall(r"[a-z0-9]+",s.lower()))
def similarity(a,b):
    try:
        v=model().encode([a,b],normalize_embeddings=True)
        return float(np.dot(v[0],v[1]))
    except Exception:
        x,y=tokens(a),tokens(b)
        return len(x&y)/max(1,len(x|y))
def rerank(a,b,semantic):
    x,y=tokens(a),tokens(b)
    lexical=len(x&y)/max(1,len(x|y))
    return max(0,min(1,.75*max(0,semantic)+.25*lexical))
