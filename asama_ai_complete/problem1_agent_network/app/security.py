import hashlib,hmac,json,os,re
from urllib.parse import urlparse
def moderate(text):
    patterns=[r"ignore\s+(all\s+)?previous\s+instructions",r"reveal\s+(the\s+)?(secret|api key|password)"]
    if any(re.search(p,text,re.I) for p in patterns): raise ValueError("Content rejected by safety filter.")
def validate_url(url):
    p=urlparse(url)
    if p.scheme!="https" or not p.hostname: raise ValueError("Webhook must be HTTPS.")
def signature(payload):
    secret=os.getenv("WEBHOOK_SECRET","dev-secret").encode()
    body=json.dumps(payload,sort_keys=True,separators=(",",":")).encode()
    return hmac.new(secret,body,hashlib.sha256).hexdigest()
