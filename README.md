# TP MonRSA

## Auteurs
- Wissem B
- Loïs F

## Description
Ce programme permet de générer des clés RSA, de chiffrer et de déchiffrer des messages en ligne de commande. Il a été développé dans le cadre d'un TP sur le chiffrement RSA.

Le programme respecte les spécifications du TP, notamment :
- La génération de clés RSA (publique et privée).
- Le chiffrement et le déchiffrement de messages.
- L'utilisation d'un format spécifique pour les clés et les messages.

## Installation

### Prérequis
- Python 3.x installé sur votre machine.

### Étapes
1. Clonez ce dépôt :
   ```bash
   git clone https://github.com/petitwiwi/ProjetLoisFWissemB.git

# Utilisation

## Générer des clés
```bash
python monRSA.py keygen
```
Les clés sont sauvegardées dans `monRSA.pub` (clé publique) et `monRSA.priv` (clé privée).

Option `-f` pour un nom personnalisé :
```bash
python monRSA.py keygen -f ma_cle
```

## Chiffrer un message
```bash
python monRSA.py crypt monRSA.pub "Message à chiffrer"
```
Le message chiffré (en Base64) est affiché.

## Déchiffrer un message
```bash
python monRSA.py decrypt monRSA.priv "Message chiffré en Base64"
```
Le message déchiffré est affiché.

## Aide
```bash
python monRSA.py help
```

## Exemple
### Générer des clés :
```bash
python monRSA.py keygen -f ma_cle
```

### Chiffrer :
```bash
python monRSA.py crypt ma_cle.pub "Hello, World!"
```

### Déchiffrer :
```bash
python monRSA.py decrypt ma_cle.priv "Base64EncodedCiphertext"
```

## Format des clés
### Clé publique (`monRSA.pub`) :
```
---begin monRSA public key---
<Base64 encoded n and e>
---end monRSA key---
```

### Clé privée (`monRSA.priv`) :
```
---begin monRSA private key---
<Base64 encoded n and d>
---end monRSA key---
```

