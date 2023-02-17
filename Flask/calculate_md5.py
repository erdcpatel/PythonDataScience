import hashlib

# Open the file to be hashed
with open('<path-to-file>', 'rb') as f:
    # Create an instance of the MD5 hash object
    md5 = hashlib.md5()
    # Read the file in chunks to conserve memory and update the hash object
    for chunk in iter(lambda: f.read(4096), b""):
        md5.update(chunk)

# Get the hexadecimal digest of the hash
digest = md5.hexdigest()
print(digest)
