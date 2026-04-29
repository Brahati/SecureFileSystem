from crypto.pipeline import encrypt_and_embed, extract_and_decrypt

result = encrypt_and_embed("data/input/sample.txt", "user1", "user2")

data, logs = extract_and_decrypt(
    result["output_path"],
    result["payload_length"],
    result["seed"],
    result["private_key"]
)

print(data)
print(logs)