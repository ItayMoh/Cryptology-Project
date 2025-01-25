# Secure Audio Encryption and Verification System

## Overview

This project demonstrates a secure system for encrypting, transmitting, and verifying audio files. It combines several advanced cryptographic techniques such as CAST-256, OFB, Rabin Digital Signatures, and EC ElGamal encryption to ensure data confidentiality, integrity, and authenticity.

## Features

- **CAST-256 in OFB mode:** Used for encrypting audio data.
- **Elliptic Curve ElGamal Encryption:** Secures the keys used in encryption.
- **Rabin Digital Signatures:** Provides authenticity for the transmitted files.
- **Modular Design:** Includes separate modules for encryption, decryption, signing, and verification.

## How It Works

1. **Key Generation:**
   - Bob generates a public-private key pair using EC ElGamal.
   - The public key is shared with Alice.

2. **Encryption by Alice:**
   - Alice generates a CAST-256 key and IV (Initialization Vector).
   - The audio file is encrypted using CAST-256 in OFB mode.
   - The CAST-256 key and IV are encrypted using Bob's public EC ElGamal key.
   - A Rabin digital signature is generated for the audio file to ensure authenticity.

3. **Decryption by Bob:**
   - Bob decrypts the CAST-256 key and IV using his private EC ElGamal key.
   - The audio file is decrypted using the CAST-256 key and IV.
   - The Rabin digital signature is verified to confirm the file's authenticity.

## Prerequisites

- Python 3.8 or higher
- Libraries: `os`, `random`, `pickle`, `base64`, `hashlib`

## Usage

1. **Alice's Encryption Process:**
   Run the `alice.py` script to encrypt the audio file and generate the signature:
   ```bash
   python alice.py
   ```
   Provide the path to the audio file when prompted.

2. **Bob's Decryption Process:**
   Run the `bob.py` script to decrypt the audio file and verify the signature:
   ```bash
   python bob.py
   ```
   Provide the same path of the audio file that you provided to alice when prompted.

3. **Cleanup Temporary Files:**
   Run the `cleanup.py` script:
   ```bash
   python cleanup.py
   ```

## Example Workflow

1. Alice encrypts an audio file `audio.mp3` and sends the encrypted file, along with the signature, to Bob.
2. Bob decrypts the file, verifies its authenticity using the signature, and retrieves the original audio file.

## Security Notes

- All keys are generated using secure random number generators.
- The CAST-256 algorithm provides strong encryption when used with OFB mode.
- EC ElGamal and Rabin signatures ensure that the file cannot be tampered with.

## Possible Improvements

- Integration with a GUI for ease of use.
- Real-time audio streaming and encryption.
- In the EC ElGamal cryptography, the `p` and `q` parameters are predefined and not randomly selected, which could be optimized for additional security or flexibility.


