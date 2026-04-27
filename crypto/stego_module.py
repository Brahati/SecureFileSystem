import cv2
import numpy as np


# Convert payload → binary
def to_binary(data: bytes) -> str:
    return ''.join(format(byte, '08b') for byte in data)


# Generate random pixel positions
def generate_positions(image_shape, total_bits, seed):
    h, w, c = image_shape
    total_pixels = h * w * c

    if total_bits > total_pixels:
        raise ValueError("❌ Not enough space in image!")

    np.random.seed(seed)

    indices = np.random.choice(total_pixels, total_bits, replace=False)

    return indices


# ------------------ EMBED ------------------
def embed_data(image_path, payload, output_path, seed=42):
    image = cv2.imread(image_path)

    if image is None:
        raise ValueError("❌ Image not found!")

    binary_data = to_binary(payload)
    data_len = len(binary_data)

    print(f"\n📊 Total bits to embed: {data_len}")

    flat_image = image.flatten()

    # Generate random positions
    positions = generate_positions(image.shape, data_len, seed)

    for i, pos in enumerate(positions):
        pixel = flat_image[pos]
        flat_image[pos] = (pixel & 254) | int(binary_data[i])

    stego_image = flat_image.reshape(image.shape)

    cv2.imwrite(output_path, stego_image)

    print("✅ Data embedded using RANDOM positions")
    print(f"📊 Total bits embedded: {data_len}")


# ------------------ EXTRACT ------------------
def extract_data(image_path, data_length, seed=42):
    image = cv2.imread(image_path)

    if image is None:
        raise ValueError("❌ Image not found!")

    flat_image = image.flatten()

    # SAME positions using SAME seed
    positions = generate_positions(image.shape, data_length, seed)

    bits = []

    for pos in positions:
        bits.append(str(flat_image[pos] & 1))

    binary_data = ''.join(bits)

    extracted_bytes = bytes(
        int(binary_data[i:i+8], 2)
        for i in range(0, len(binary_data), 8)
    )

    print("✅ Data extracted using SAME random positions")

    return extracted_bytes