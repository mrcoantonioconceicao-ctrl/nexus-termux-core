import sys
import os
from pathlib import Path

# Adiciona o diretório core ao path
sys.path.append(str(Path(__file__).resolve().parent.parent / "core"))
from safety_guard import validate_safe_path

def test_safe_traversal_blocking():
    malicious_inputs = [
        "../../escape.rs",
        "../../../data/data/com.termux/files/home/.bashrc",
        "nested/../../../secret.txt"
    ]
    
    blocked = 0
    for payload in malicious_inputs:
        try:
            validate_safe_path(payload)
        except PermissionError:
            blocked += 1
            print(f"[GUARD BLOCKED] Successfully intercepted: {payload}")
        except Exception as e:
            print(f"[UNEXPECTED ERROR] {payload}: {e}")
            
    assert blocked == len(malicious_inputs), f"Falha de segurança! Bloqueados {blocked}/{len(malicious_inputs)}"
    print("[+] Todos os ataques de path traversal foram barrados com sucesso.")

if __name__ == "__main__":
    test_safe_traversal_blocking()

