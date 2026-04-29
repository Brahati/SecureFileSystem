from crypto.aes_module import AESHandler
from crypto.rsa_module import RSAHandler
from crypto.utils import read_file
from crypto.stego_module import embed_data, extract_data

import time
import json
import os
from Crypto.PublicKey import RSA


# =========================================================
# 🔐 ENCRYPT + EMBED PIPELINE
# =========================================================

def encrypt_and_embed(input_path, sender, receiver):

    logs = []

    # STEP 1: Read file
    original_data = read_file(input_path)
    logs.append("📄 File loaded successfully")

    # 🔥 STEP 2: ADD METADATA
    filename = os.path.basename(input_path)

    metadata = {
        "filename": filename
    }

    meta_bytes = json.dumps(metadata).encode()
    combined_data = meta_bytes + b"|||" + original_data

    logs.append(f"📄 Metadata added (filename: {filename})")

    # STEP 3: AES Encryption
    start = time.time()
    key, nonce, tag, ciphertext = AESHandler.encrypt(combined_data)
    end = time.time()

    logs.append(f"🔐 AES Encryption complete ({end - start:.6f} sec)")

    # STEP 4: Generate seed
    seed = int.from_bytes(key[:4], 'big')
    logs.append("🔑 Seed generated from AES key")

    # STEP 5: RSA Key Generation
    private_key, public_key = RSAHandler.generate_keys()
    logs.append("🔐 RSA Keys generated")

    # STEP 6: Encrypt AES key
    encrypted_key = RSAHandler.encrypt(public_key, key)
    logs.append("🔒 AES key encrypted using RSA")

    # STEP 7: Combine payload
    payload = encrypted_key + nonce + tag + ciphertext
    payload_length = len(payload)

    logs.append(f"📦 Payload created ({payload_length} bytes)")

    # STEP 8: Stego embed
    output_path = f"storage/{receiver}/received/stego_{int(time.time())}.png"

    embed_data(
        image_path="data/input/cover.png",
        payload=payload,
        output_path=output_path,
        seed=seed
    )

    logs.append("🖼️ Payload embedded into image successfully")

    # STEP 9: Convert private key
    private_key_str = private_key.export_key().decode()

    return {
        "output_path": output_path,
        "payload_length": payload_length,
        "seed": seed,
        "private_key": private_key_str,
        "logs": logs
    }


# =========================================================
# 🔓 EXTRACT + DECRYPT PIPELINE
# =========================================================

def extract_and_decrypt(stego_path, payload_length, seed, private_key_str):

    logs = []

    # STEP 1: Extract payload
    payload = extract_data(
        image_path=stego_path,
        data_length=payload_length * 8,
        seed=seed
    )

    if payload is None or len(payload) != payload_length:
        logs.append("❌ ERROR: Payload corrupted during extraction")
        return None, logs

    logs.append("📦 Payload extracted successfully")

    # STEP 2: Split payload
    encrypted_key = payload[:256]
    nonce = payload[256:272]
    tag = payload[272:288]
    ciphertext = payload[288:]

    logs.append("📦 Payload components separated")

    # STEP 3: Load private key
    private_key = RSA.import_key(private_key_str)

    # STEP 4: RSA decrypt AES key
    try:
        key = RSAHandler.decrypt(private_key, encrypted_key)
        logs.append("🔓 AES key decrypted using RSA")
    except:
        logs.append("❌ RSA Decryption failed")
        return None, logs

    # STEP 5: AES decrypt
    start = time.time()
    decrypted_data = AESHandler.decrypt(key, nonce, tag, ciphertext)
    end = time.time()

    logs.append(f"🔓 AES Decryption complete ({end - start:.6f} sec)")

    # 🔥 STEP 6: Extract metadata + file
    try:
        meta_bytes, file_data = decrypted_data.split(b"|||", 1)
        metadata = json.loads(meta_bytes.decode())

        filename = metadata.get("filename", "output.bin")

        logs.append(f"📄 Metadata extracted (filename: {filename})")

    except Exception as e:
        logs.append("❌ Metadata parsing failed")
        return None, logs

    return {
        "file_data": file_data,
        "filename": filename
    }, logs