
# SecureFileSystem — Cryptographically Secure File Sharing

A Python-based secure file-sharing prototype that combines **hybrid cryptography** and **image steganography** to protect files during storage and sharing.

SecureFileSystem uses AES-GCM to encrypt file contents, RSA to protect the AES encryption key, and Least Significant Bit (LSB) steganography to embed the encrypted payload inside a cover image. The application provides a Flask-based interface for managing file-sharing workflows.

## Features

- **AES-GCM Encryption:** Encrypts file contents while providing confidentiality and integrity verification.
- **RSA Key Protection:** Encrypts the AES key to protect it separately from the file contents.
- **Image Steganography:** Embeds the encrypted payload into a cover image using LSB-based techniques.
- **Secure Payload Construction:** Combines the encrypted key, nonce, authentication tag, and ciphertext into a payload for embedding.
- **Flask Web Application:** Provides an interface for file-sharing operations.
- **SQLite Database:** Stores application metadata associated with users and shared files.
- **Challenge–Response Authentication:** Implements a challenge–response authentication mechanism.

## How It Works

### Encryption and File Sharing

1. The sender selects a file to share.
2. A symmetric key is used to encrypt the file using AES-GCM.
3. The AES key is encrypted using RSA.
4. The encrypted key, nonce, authentication tag, and ciphertext are assembled into a payload.
5. The payload is embedded into a cover image using LSB steganography.
6. The resulting stego-image is used in the file-sharing workflow, and associated metadata is stored in SQLite.

### File Retrieval and Decryption

1. The recipient accesses the shared file through the application.
2. The embedded payload is extracted from the stego-image.
3. The RSA-protected AES key is recovered using the appropriate private key.
4. The original file contents are decrypted using AES-GCM.
5. The authentication tag is verified during decryption.

Successful decryption requires the correct key material and an intact authenticated ciphertext.

## Architecture

The application consists of four main components:

| Component | Responsibility |
|---|---|
| Flask | Web interface and application request handling |
| Cryptography modules | AES-GCM encryption and RSA key protection |
| Steganography module | Payload embedding and extraction |
| SQLite | User and file metadata management |

### Data Flow

**Sending:**

Original File → AES-GCM Encryption → RSA Key Protection → Payload Construction → LSB Embedding → Stego-Image

**Receiving:**

Stego-Image → Payload Extraction → RSA Key Recovery → AES-GCM Decryption → Original File

## Technology Stack

- **Language:** Python
- **Backend:** Flask
- **Cryptography:** AES-GCM, RSA
- **Steganography:** Least Significant Bit (LSB) encoding
- **Database:** SQLite
- **Version Control:** Git and GitHub

## Getting Started

### Prerequisites

- Python 3
- pip
- Git

### Installation

Clone the repository:

```bash
git clone <YOUR_REPOSITORY_URL>
cd SecureFileSystem
```

Create a virtual environment:

**Windows**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS**
```bash
python3 -m venv venv
source venv/bin/activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

### Run the Application

If `main.py` is the application's entry point, run:

```bash
python main.py
```

Open the local URL displayed in the terminal in your browser.

## Security Considerations

SecureFileSystem is an educational prototype for exploring cryptographic file protection and steganographic data hiding.

- AES-GCM provides authenticated encryption when used with appropriate key and nonce management.
- RSA key protection depends on secure key generation, appropriate padding, and private-key confidentiality.
- Steganography conceals data within an image but does not itself encrypt the data or guarantee that the hidden payload cannot be detected.
- Challenge–response authentication requires secure challenge generation, replay protection, appropriate secret handling, and secure transport.
- A complete security assessment should consider private-key storage, authorization, temporary files, metadata exposure, input validation, and deployment configuration.

The authentication mechanism should not be considered a formally verified zero-knowledge proof protocol without a separate cryptographic analysis.

**This project has not been independently security-audited and should not be treated as production-ready for sensitive files without further review and testing.**

## Future Improvements

- Add automated unit and integration tests for encryption, decryption, and payload extraction.
- Improve key management and secure key storage.
- Strengthen authentication, session management, and access control.
- Add file-size limits, input validation, and robust error handling.
- Document performance and steganographic capacity across different file and image sizes.
- Add automated testing and continuous integration.
