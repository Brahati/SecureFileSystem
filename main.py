from crypto.aes_module import AESHandler
from crypto.rsa_module import RSAHandler
from crypto.utils import read_file, write_file
import time

print("\n🚀 STARTING ENCRYPTION PROCESS...\n")

# ------------------ STEP 1: READ FILE ------------------
original_data = read_file("data/input/sample.txt")

print("📄 ORIGINAL DATA (first 100 bytes):")
print(original_data[:100])


# ------------------ STEP 2: AES ENCRYPT ------------------
start_time = time.time()

key, nonce, tag, ciphertext = AESHandler.encrypt(original_data)

end_time = time.time()

print("\n🔐 AES ENCRYPTION COMPLETE")

print("\n🔐 ENCRYPTED DATA (first 100 bytes):")
print(ciphertext[:100])

print("\n🔑 AES KEY (partial):")
print(key[:10], "... (hidden)")

print("\n🧪 NONCE:")
print(nonce)

print("\n🧪 TAG:")
print(tag)

print(f"\n⏱ AES Encryption Time: {end_time - start_time:.6f} seconds")


# ------------------ STEP 3: RSA KEY GENERATION ------------------
print("\n🔐 GENERATING RSA KEYS...")

private_key, public_key = RSAHandler.generate_keys()

print("✅ RSA KEYS GENERATED")


# ------------------ STEP 4: ENCRYPT AES KEY USING RSA ------------------
encrypted_key = RSAHandler.encrypt(public_key, key)

print("\n🔒 RSA ENCRYPTED AES KEY (first 50 bytes):")
print(encrypted_key[:50])


# ------------------ STEP 5: COMBINE PAYLOAD ------------------
payload = encrypted_key + nonce + tag + ciphertext

print("\n📦 PAYLOAD CREATED")
print("📦 Payload Size:", len(payload), "bytes")

write_file("data/output/encrypted.bin", payload)

print("\n💾 Encrypted payload saved to data/output/encrypted.bin")


# =========================================================
# =================== DECRYPTION ==========================
# =========================================================

print("\n🔓 STARTING DECRYPTION PROCESS...\n")

# ------------------ STEP 6: READ PAYLOAD ------------------
payload = read_file("data/output/encrypted.bin")

# Split components
encrypted_key = payload[:256]       # RSA 2048 → 256 bytes
nonce = payload[256:272]           # 16 bytes
tag = payload[272:288]             # 16 bytes
ciphertext = payload[288:]

print("📦 Payload extracted successfully")


# ------------------ STEP 7: RSA DECRYPT AES KEY ------------------
decrypted_key = RSAHandler.decrypt(private_key, encrypted_key)

print("\n🔓 AES KEY DECRYPTED (partial):")
print(decrypted_key[:10], "... (hidden)")


# ------------------ STEP 8: AES DECRYPT ------------------
start_time = time.time()

decrypted_data = AESHandler.decrypt(decrypted_key, nonce, tag, ciphertext)

end_time = time.time()

print("\n🔓 AES DECRYPTION COMPLETE")

print("\n🔓 DECRYPTED DATA (first 100 bytes):")
print(decrypted_data[:100])

print(f"\n⏱ AES Decryption Time: {end_time - start_time:.6f} seconds")


# ------------------ STEP 9: VERIFY ------------------
if original_data == decrypted_data:
    print("\n✅ SUCCESS: Decrypted data matches original!")
else:
    print("\n❌ ERROR: Data mismatch!")


# ------------------ STEP 10: SAVE OUTPUT ------------------
write_file("data/output/decrypted.txt", decrypted_data)

print("\n💾 Decrypted file saved to data/output/decrypted.txt")

print("\n🎉 PROCESS COMPLETED SUCCESSFULLY!\n")