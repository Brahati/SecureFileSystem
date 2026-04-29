import hashlib
import random

# Pre-shared secret (only user knows)
USER_SECRETS = {
    "user1": "my_secret_123",
    "user2": "team_secret_456"
}

def generate_challenge():
    return str(random.randint(10000, 99999))

def compute_response(secret, challenge):
    return hashlib.sha256((secret + challenge).encode()).hexdigest()