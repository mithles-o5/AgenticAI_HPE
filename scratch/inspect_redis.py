import redis
import os
import json

# Redis connection details from environment (matching store.py)
REDIS_HOST = os.getenv("MEMURAI_HOST", os.getenv("REDIS_HOST", "localhost"))
REDIS_PORT = int(os.getenv("MEMURAI_PORT", os.getenv("REDIS_PORT", "6379")))
REDIS_DB = int(os.getenv("MEMURAI_DB", os.getenv("REDIS_DB", "0")))
REDIS_PASSWORD = os.getenv("MEMURAI_PASSWORD", os.getenv("REDIS_PASSWORD"))

def inspect():
    print(f"Connecting to Redis at {REDIS_HOST}:{REDIS_PORT}/db={REDIS_DB}...")
    try:
        client = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB,
            password=REDIS_PASSWORD,
            decode_responses=True
        )
        client.ping()
        print("Connected successfully!")
        
        print("\n--- Scanning all keys in Redis ---")
        keys = sorted(client.keys("*"))
        if not keys:
            print("No keys found in Redis.")
            return
            
        for k in keys:
            type_ = client.type(k)
            print(f"Key: {k:<40} | Type: {type_}")
            if type_ == "string":
                val = client.get(k)
                print(f"  Value: {val}")
            elif type_ == "set":
                val = client.smembers(k)
                print(f"  Members: {list(val)}")
            elif type_ == "hash":
                val = client.hgetall(k)
                print(f"  Hash: {val}")
    except Exception as e:
        print(f"Error inspecting Redis: {e}")

if __name__ == "__main__":
    inspect()
