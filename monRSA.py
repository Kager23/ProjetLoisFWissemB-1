import random
import base64
import sys

def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

def generate_prime_candidate(length):
    return random.getrandbits(length)

def generate_prime_number(length=10):
    p = 4
    while not is_prime(p):
        p = generate_prime_candidate(length)
    return p

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

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

def generate_keys():
    p = generate_prime_number()
    q = generate_prime_number()
    while q == p:
        q = generate_prime_number()
    
    n = p * q
    phi = (p - 1) * (q - 1)
    
    e = random.randrange(1, phi)
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)
    
    d = modinv(e, phi)
    
    return ((e, n), (d, n))

def save_keys(public_key, private_key, filename="monRSA"):
    pub_key_str = "---begin monRSA public key---\n" + base64.b64encode(f"{public_key[1]:x}\n{public_key[0]:x}".encode()).decode() + "\n---end monRSA key---"
    priv_key_str = "---begin monRSA private key---\n" + base64.b64encode(f"{private_key[1]:x}\n{private_key[0]:x}".encode()).decode() + "\n---end monRSA key---"
    
    with open(f"{filename}.pub", "w", encoding="utf-8") as pub_file:
        pub_file.write(pub_key_str)
    
    with open(f"{filename}.priv", "w", encoding="utf-8") as priv_file:
        priv_file.write(priv_key_str)

def read_public_key(filename):
    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()
        if lines[0].strip() != "---begin monRSA public key---":
            raise ValueError("Invalid public key file")
        key_data = base64.b64decode(lines[1].strip()).decode()
        n, e = key_data.split('\n')
        return (int(e, 16), int(n, 16))

def read_private_key(filename):
    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()
        if lines[0].strip() != "---begin monRSA private key---":
            raise ValueError("Invalid private key file")
        key_data = base64.b64decode(lines[1].strip()).decode()
        n, d = key_data.split('\n')
        return (int(d, 16), int(n, 16))

def encrypt(public_key, plaintext):
    key, n = public_key
    cipher = [(ord(char) ** key) % n for char in plaintext]
    cipher_bytes = bytearray()
    for value in cipher:
        while value > 0:
            cipher_bytes.append(value % 256)
            value //= 256
    return base64.b64encode(cipher_bytes).decode('utf-8')

def decrypt(private_key, ciphertext):
    key, n = private_key
    # Ajout de remplissage correct pour Base64
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
    plain = [chr((char ** key) % n) for char in cipher]
    return ''.join(plain)

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
        print(f"Clés générées et sauvegardées dans {filename}.pub et {filename}.priv")

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
