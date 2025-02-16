import random
import base64
import sys
import math

# Fonction pour vérifier si un nombre est premier
def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(math.isqrt(num)) + 1):
        if num % i == 0:
            return False
    return True

# Génère un nombre premier de longueur donnée (par défaut 10 chiffres)
def generate_prime_number(length=10):
    while True:
        p = random.getrandbits(length)
        if is_prime(p):
            return p

# Calcul du PGCD (Plus Grand Commun Diviseur)
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

# Calcul de l'inverse modulaire (e^-1 mod phi)
def modinv(a, m):
    m0, x0, x1 = m, 0, 1
    if m == 1:
        return 0
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += m0
    return x1

# Génère une paire de clés RSA (publique et privée)
def generate_keys():
    p = generate_prime_number()
    q = generate_prime_number()
    while q == p:  # Assure que p et q sont différents
        q = generate_prime_number()
    
    n = p * q
    phi = (p - 1) * (q - 1)
    
    # Choix de e (premier avec phi)
    e = random.randrange(1, phi)
    while gcd(e, phi) != 1:
        e = random.randrange(1, phi)
    
    # Calcul de d (inverse de e modulo phi)
    d = modinv(e, phi)
    
    return ((e, n), (d, n))

# Sauvegarde les clés dans des fichiers au format spécifié
def save_keys(public_key, private_key, filename="monRSA"):
    # Clé publique
    pub_key_str = f"{public_key[1]:x}\n{public_key[0]:x}"
    pub_key_encoded = base64.b64encode(pub_key_str.encode()).decode()
    pub_key_file = f"{filename}.pub"
    with open(pub_key_file, "w", encoding="utf-8") as f:
        f.write(f"---begin monRSA public key---\n{pub_key_encoded}\n---end monRSA key---")
    
    # Clé privée
    priv_key_str = f"{private_key[1]:x}\n{private_key[0]:x}"
    priv_key_encoded = base64.b64encode(priv_key_str.encode()).decode()
    priv_key_file = f"{filename}.priv"
    with open(priv_key_file, "w", encoding="utf-8") as f:
        f.write(f"---begin monRSA private key---\n{priv_key_encoded}\n---end monRSA key---")
    
    print(f"Clés sauvegardées dans {pub_key_file} et {priv_key_file}")

# Lit une clé publique depuis un fichier
def read_public_key(filename):
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()
        if lines[0].strip() != "---begin monRSA public key---":
            raise ValueError("Format de clé publique invalide")
        key_data = base64.b64decode(lines[1].strip()).decode()
        n_hex, e_hex = key_data.split('\n')
        return (int(e_hex, 16), int(n_hex, 16))

# Lit une clé privée depuis un fichier
def read_private_key(filename):
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()
        if lines[0].strip() != "---begin monRSA private key---":
            raise ValueError("Format de clé privée invalide")
        key_data = base64.b64decode(lines[1].strip()).decode()
        n_hex, d_hex = key_data.split('\n')
        return (int(d_hex, 16), int(n_hex, 16))

# Chiffre un message avec la clé publique
def encrypt(public_key, plaintext):
    e, n = public_key
    cipher = [pow(ord(char), e, n) for char in plaintext]  # Chiffrement RSA
    cipher_bytes = bytearray()
    for value in cipher:
        while value > 0:
            cipher_bytes.append(value % 256)
            value //= 256
    return base64.b64encode(cipher_bytes).decode('utf-8')

# Déchiffre un message avec la clé privée
def decrypt(private_key, ciphertext):
    d, n = private_key
    # Ajout de padding pour Base64 si nécessaire
    padding = len(ciphertext) % 4
    if padding != 0:
        ciphertext += "=" * (4 - padding)
    cipher_bytes = base64.b64decode(ciphertext.encode('utf-8'))
    cipher = []
    for i in range(0, len(cipher_bytes), 2):
        value = cipher_bytes[i]
        if i + 1 < len(cipher_bytes):
            value += cipher_bytes[i + 1] * 256
        cipher.append(value)
    plain = [chr(pow(char, d, n)) for char in cipher]  # Déchiffrement RSA
    return ''.join(plain)

# Fonction principale pour gérer les arguments en ligne de commande
def main(args):
    if len(args) < 1 or args[0] == "help":
        print("Script monRSA par Nug")
        print("Syntaxe :")
        print("monRSA <commande> [<clé>] [<texte>] [switchs]")
        print("Commande :")
        print("keygen : Génère une paire de clé")
        print("crypt : Chiffre <texte> pour le clé publique <clé>")
        print("decrypt: Déchiffre <texte> pour le clé privée <clé>")
        print("help : Affiche ce manuel")
        return

    command = args[0]

    if command == "keygen":
        public_key, private_key = generate_keys()
        filename = "monRSA"
        if "-f" in args:
            filename = args[args.index("-f") + 1]
        save_keys(public_key, private_key, filename)

    elif command == "crypt":
        if len(args) < 3:
            print("Usage: monRSA crypt <clé publique> <texte>")
            return
        public_key = read_public_key(args[1])
        plaintext = args[2]
        ciphertext = encrypt(public_key, plaintext)
        print("Encrypted:", ciphertext)

    elif command == "decrypt":
        if len(args) < 3:
            print("Usage: monRSA decrypt <clé privée> <texte>")
            return
        private_key = read_private_key(args[1])
        ciphertext = args[2]
        plaintext = decrypt(private_key, ciphertext)
        print("Decrypted:", plaintext)

if __name__ == "__main__":
    main(sys.argv[1:])