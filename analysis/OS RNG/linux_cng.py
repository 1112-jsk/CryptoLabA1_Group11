import os

size = 1024 * 1024
path = "data/urandom.bin"

os.makedirs("data", exist_ok=True)

with open(path, "wb") as f:
    f.write(os.urandom(size))

print("Linux random data generated successfully!")
print("File size:", os.path.getsize(path), "bytes")