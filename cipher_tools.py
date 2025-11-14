"""
Cipher Tools Module
Provides encryption and decryption functionality
"""

import json
from typing import Dict, Any

class CipherTools:
    """Cipher tools for encryption and decryption"""
    
    @staticmethod
    def caesar_cipher(text: str, shift: int, encrypt: bool = True) -> str:
        """Caesar cipher encryption/decryption"""
        if not text:
            return ""
        
        result = []
        for char in text:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                if encrypt:
                    shifted = (ord(char) - base + shift) % 26
                else:
                    shifted = (ord(char) - base - shift) % 26
                result.append(chr(base + shifted))
            else:
                result.append(char)
        return ''.join(result)
    
    @staticmethod
    def reverse_cipher(text: str) -> str:
        """Reverse cipher - reverses the text"""
        return text[::-1]
    
    @staticmethod
    def atbash_cipher(text: str) -> str:
        """Atbash cipher - A=Z, B=Y, etc."""
        result = []
        for char in text:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                shifted = 25 - (ord(char) - base)
                result.append(chr(base + shifted))
            else:
                result.append(char)
        return ''.join(result)

def analyze_cipher_tools() -> Dict[str, Any]:
    """Analyze cipher tools and provide examples"""
    cipher = CipherTools()
    
    # Example texts
    original_text = "Hello World"
    
    # Caesar cipher examples
    caesar_encrypted = cipher.caesar_cipher(original_text, 3, encrypt=True)
    caesar_decrypted = cipher.caesar_cipher(caesar_encrypted, 3, encrypt=False)
    
    # Reverse cipher
    reverse_encrypted = cipher.reverse_cipher(original_text)
    reverse_decrypted = cipher.reverse_cipher(reverse_encrypted)
    
    # Atbash cipher
    atbash_encrypted = cipher.atbash_cipher(original_text)
    atbash_decrypted = cipher.atbash_cipher(atbash_encrypted)
    
    return {
        "summary": {
            "available_ciphers": ["Caesar", "Reverse", "Atbash"],
            "total_ciphers": 3
        },
        "examples": {
            "caesar_cipher": {
                "original": original_text,
                "encrypted": caesar_encrypted,
                "decrypted": caesar_decrypted,
                "shift": 3
            },
            "reverse_cipher": {
                "original": original_text,
                "encrypted": reverse_encrypted,
                "decrypted": reverse_decrypted
            },
            "atbash_cipher": {
                "original": original_text,
                "encrypted": atbash_encrypted,
                "decrypted": atbash_decrypted
            }
        },
        "cipher_descriptions": {
            "Caesar": "Shifts each letter by a fixed number of positions in the alphabet",
            "Reverse": "Reverses the entire text",
            "Atbash": "Substitutes each letter with its mirror (A=Z, B=Y, etc.)"
        }
    }

def main():
    """Main function for command-line use"""
    results = analyze_cipher_tools()
    print("\n=== Cipher Tools Analysis ===")
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
