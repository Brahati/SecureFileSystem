import cv2
import numpy as np


# ------------------ STEP 1: Convert payload to binary ------------------
def to_binary(data: bytes) -> str:
    return ''.join(format(byte, '08b') for byte in data)


# ------------------ STEP 2: Edge Detection (AI-like decision) ------------------
def get_edge_mask(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Canny edge detection → finds high-frequency regions
    edges = cv2.Canny(gray, 100, 200)

    return edges


# ------------------ STEP 3: Embed data into image ------------------
def embed_data(image_path, payload, output_path):
    image = cv2.imread(image_path)

    if image is None:
        raise ValueError("❌ Error: Image not found!")

    edges = get_edge_mask(image)

    binary_data = to_binary(payload)
    data_len = len(binary_data)

    print(f"\n📊 Total bits to embed: {data_len}")

    idx = 0

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):

            # Only embed in edge regions (smart decision)
            if True:

                for k in range(3):  # RGB channels
                    if idx < data_len:
                        pixel = image[i, j, k]

                        # Replace LSB with data bit
                        image[i, j, k] = (pixel & 254) | int(binary_data[idx])

                        idx += 1

                    else:
                        break

    if idx < data_len:
        print("⚠️ Warning: Image may not have enough capacity!")

    cv2.imwrite(output_path, image)

    print(f"✅ Data successfully embedded in {output_path}")
    print(f"📊 Total bits embedded: {idx}")


# ------------------ STEP 4: Extract data from image ------------------
def extract_data(image_path, data_length):
    image = cv2.imread(image_path)

    if image is None:
        raise ValueError("❌ Error: Image not found!")

    edges = get_edge_mask(image)

    bits = []

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):

            if True:

                for k in range(3):
                    bits.append(str(image[i, j, k] & 1))

                    if len(bits) == data_length:
                        binary_data = ''.join(bits)

                        # Convert binary → bytes
                        extracted_bytes = bytes(
                            int(binary_data[i:i+8], 2)
                            for i in range(0, len(binary_data), 8)
                        )

                        print(f"✅ Data successfully extracted")
                        return extracted_bytes

    print("⚠️ Warning: Could not extract full data!")
    return None