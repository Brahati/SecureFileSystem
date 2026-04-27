from crypto.aes_module import AESHandler
from crypto.rsa_module import RSAHandler
from crypto.utils import read_file, write_file
from crypto.stego_module import embed_data, extract_data
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
payload_length = len(payload)

print("\n📦 PAYLOAD CREATED")
print("📦 Payload Size:", payload_length, "bytes")

write_file("data/output/encrypted.bin", payload)

print("\n💾 Encrypted payload saved to data/output/encrypted.bin")


# ------------------ STEP 6: HIDE PAYLOAD IN IMAGE ------------------
embed_data(
    image_path="data/input/cover.png",
    payload=payload,
    output_path="data/output/stego.png"
)

print("\n🖼️ Payload hidden inside image: data/output/stego.png")


# =========================================================
# =================== DECRYPTION ==========================
# =========================================================

print("\n🔓 STARTING DECRYPTION PROCESS...\n")


# ------------------ STEP 7: EXTRACT PAYLOAD ------------------
payload_extracted = extract_data(
    image_path="data/output/stego.png",
    data_length=payload_length * 8
)

# 🔥 DEBUG CHECK (CRUCIAL)
print("\n🔍 DEBUG CHECK:")
print("Original payload length:", payload_length)
print("Extracted payload length:", len(payload_extracted) if payload_extracted else 0)

# ❗ STOP if corrupted
if payload_extracted is None or len(payload_extracted) != payload_length:
    print("\n❌ ERROR: Payload corrupted during steganography!")
    print("👉 Fix stego_module.py (embedding issue)")
    exit()

payload = payload_extracted

print("📦 Payload extracted successfully from image")


# ------------------ STEP 8: SPLIT PAYLOAD ------------------
encrypted_key = payload[:256]
nonce = payload[256:272]
tag = payload[272:288]
ciphertext = payload[288:]


# ------------------ STEP 9: RSA DECRYPT AES KEY ------------------
try:
    decrypted_key = RSAHandler.decrypt(private_key, encrypted_key)
except Exception as e:
    print("\n❌ RSA DECRYPTION FAILED")
    print("👉 Reason: Payload corrupted (wrong bits extracted)")
    exit()

print("\n🔓 AES KEY DECRYPTED (partial):")
print(decrypted_key[:10], "... (hidden)")


# ------------------ STEP 10: AES DECRYPT ------------------
start_time = time.time()

decrypted_data = AESHandler.decrypt(decrypted_key, nonce, tag, ciphertext)

end_time = time.time()

print("\n🔓 AES DECRYPTION COMPLETE")

print("\n🔓 DECRYPTED DATA (first 100 bytes):")
print(decrypted_data[:100])

print(f"\n⏱ AES Decryption Time: {end_time - start_time:.6f} seconds")


# ------------------ STEP 11: VERIFY ------------------
if original_data == decrypted_data:
    print("\n✅ SUCCESS: Decrypted data matches original!")
else:
    print("\n❌ ERROR: Data mismatch!")


# ------------------ STEP 12: SAVE OUTPUT ------------------
write_file("data/output/decrypted.txt", decrypted_data)

print("\n💾 Decrypted file saved to data/output/decrypted.txt")

print("\n🎉 PROCESS COMPLETED SUCCESSFULLY!\n")