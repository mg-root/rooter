<h1 align="center">📦 rooter</h1>

<p align="center">
  Une boîte à outils Python légère pour donner un vrai look à vos scripts terminal.<br/>
  <sub>Couleurs · Panneaux · Tableaux · Menus · Invites de saisie · Base de données JSON</sub>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white"/>&nbsp;
  <img src="https://img.shields.io/badge/Licence-MIT-6d28d9?style=flat"/>&nbsp;
  <img src="https://img.shields.io/badge/Type-Librairie%20CLI-555?style=flat"/>&nbsp;
  <img src="https://img.shields.io/badge/Statut-Projet%20perso-15803d?style=flat"/>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png" width="100%"/>
</p>

## Sommaire

- [Contexte](#-contexte)
- [Pourquoi ce projet](#-pourquoi-ce-projet)
- [Aperçu des fonctionnalités](#-aperçu-des-fonctionnalités)
- [Installation](#-installation)
- [Démarrage rapide](#-démarrage-rapide)
- [Documentation par module](#-documentation-par-module)
  - [Texte stylé & couleurs](#texte-stylé--couleurs)
  - [Panel — panneaux encadrés](#panel--panneaux-encadrés)
  - [Table — tableaux](#table--tableaux)
  - [Menu — menus interactifs](#menu--menus-interactifs)
  - [Prompt — invites de saisie](#prompt--invites-de-saisie)
  - [Progress — barre de progression](#progress--barre-de-progression)
  - [Grid — grille Unicode](#grid--grille-unicode)
  - [JsonDatabase — base de données JSON](#jsondatabase--base-de-données-json)
  - [Utilitaires](#utilitaires)
- [Structure du projet](#-structure-du-projet)
- [Ce que ce projet m'a apporté](#-ce-que-ce-projet-ma-apporté)
- [Pistes d'amélioration](#-pistes-damélioration)
- [Licence](#-licence)

---

## 🎯 Contexte

**rooter** est une bibliothèque Python que j'ai développée pour répondre à un besoin récurrent dans mes projets terminal : afficher des informations de manière **lisible et esthétique**, sans réécrire à chaque fois le même code de mise en forme.

Plutôt que de manipuler directement les codes d'échappement ANSI (peu lisibles, faciles à casser), rooter propose une **syntaxe par balises** — proche du HTML — et un ensemble de composants prêts à l'emploi : panneaux, tableaux, menus, invites de saisie, barres de progression. Le tout est regroupé dans une API cohérente, pensée pour être réutilisée d'un projet à l'autre.

C'est un projet **personnel et pédagogique** : l'objectif n'était pas de concurrencer des bibliothèques établies comme `rich`, mais de **comprendre en profondeur** comment fonctionne le formatage terminal en le reconstruisant moi-même, de la gestion des couleurs jusqu'au rendu des composants.

---

## 💡 Pourquoi ce projet

- **Comprendre le formatage ANSI** de l'intérieur : couleurs, styles, réinitialisation, styles imbriqués.
- **Concevoir une API réutilisable** : passer d'un script jetable à une vraie bibliothèque installable via `pip`.
- **Structurer du code en modules** cohérents, chacun avec sa responsabilité (un composant = un fichier).
- **Résoudre des problèmes concrets** : gérer une pile de styles imbriqués, calculer la largeur d'un texte en ignorant les balises, aligner du contenu dans des cadres Unicode.

---

## ✨ Aperçu des fonctionnalités

| Composant | Rôle |
|-----------|------|
| **Texte stylé** | Coloration et style par balises (`<red>`, `<bold>`, `</>`) avec gestion des imbrications |
| **Couleurs custom** | Ajout de couleurs par nom, en hexadécimal ou RGB |
| **`Panel`** | Encadre du texte dans une boîte titrée et colorée |
| **`Table`** | Tableaux avec colonnes stylées et bordures optionnelles |
| **`Menu`** | Menus numérotés interactifs |
| **`Prompt`** | Saisie utilisateur validée (type, choix, intervalle, mot de passe) |
| **`Progress`** | Barre de progression animée avec temps restant |
| **`Grid`** | Grille de cellules en caractères Unicode |
| **`JsonDatabase`** | Mini-base de données sur fichiers JSON, typée, avec requêtes |
| **Utilitaires** | Robustesse de mot de passe, formatage de nombres, téléchargement |

---

## 📦 Installation

```bash
git clone https://github.com/mg-root/rooter.git
cd rooter
pip install .
```

**Prérequis :** Python ≥ 3.10.

---

## 🚀 Démarrage rapide

```python
from rooter import print
from rooter.panel import Panel

# Texte stylé par balises
print("<green>Installation</> <bold>terminée</> avec succès !")

# Un panneau encadré
print(Panel(title="Bienvenue", text="Premier pas avec rooter", color="cyan"))
```

Le `print` de rooter remplace celui de Python : il interprète les balises, mais colore aussi automatiquement les booléens, les nombres et `None`.

---

## 📚 Documentation par module

### Texte stylé & couleurs

Le cœur de la bibliothèque (`rooter/__init__.py`). La syntaxe par balises ouvre un style avec `<nom>` et le referme avec `</>`. Les imbrications sont gérées par une pile : à la fermeture, le style parent est restauré.

```python
from rooter import rooter, print

# Balises de style et de couleur
print("<red>Erreur :</> <yellow>fichier introuvable</>")
print("<bold><underline>Titre important</></>")

# Ajouter une couleur personnalisée
rooter.addColor("orange", hex="#FF8800")
rooter.addColor("turquoise", rgb=(64, 224, 208))
print("<orange>Couleur personnalisée</>")
```

**Balises disponibles :** couleurs (`red`, `green`, `blue`, `cyan`, `purple`, `grey`…), fonds (`bg_red`…) et styles (`bold`, `italic`, `underline`, `dim`, `reverse`, `strikethough`).

---

### `Panel` — panneaux encadrés

Encadre un texte (multi-lignes possible) dans une boîte aux coins arrondis.

```python
from rooter.panel import Panel

print(Panel(
    title="Statut",
    text="Service : actif\nUptime : 12j",
    color="green",
    border_color="grey",
    min_size=30
))
```

| Paramètre | Description |
|-----------|-------------|
| `title` | Titre affiché dans la bordure haute |
| `title_color` | Couleur du titre |
| `text` | Contenu (les `\n` créent plusieurs lignes) |
| `color` | Couleur du texte |
| `border_color` | Couleur de la bordure |
| `min_size` | Largeur minimale du panneau |

---

### `Table` — tableaux

Construit un tableau avec en-têtes stylés et bordures optionnelles entre les lignes.

```python
from rooter.table import Table

table = Table(title="Utilisateurs", border=True)
table.addColumn("ID", styles="bold cyan")
table.addColumn("Nom", styles="green")
table.addRow(["1", "Sasha"])
table.addRow(["2", "Alex"])
print(table)
```

- `addColumn(nom, styles)` — ajoute une colonne ; `styles` accepte plusieurs styles séparés par un espace.
- `addRow(...)` — ajoute une ligne (liste de valeurs ou arguments).

---

### `Menu` — menus interactifs

Un menu numéroté, construit au-dessus de `Panel` et `Prompt`.

```python
from rooter.menu import Menu

menu = Menu(
    title="Menu principal",
    color="cyan",
    color_index="yellow",
    data=["Démarrer", "Paramètres", "Quitter"]
)
menu.show()
choix = menu.ask()   # renvoie l'index (0, 1, 2…) du choix
```

- `setData(liste)` / `addData(élément, position)` — gèrent les entrées.
- `ask()` — affiche l'invite, valide la saisie et renvoie l'index choisi.

---

### `Prompt` — invites de saisie

Une invite de saisie robuste, avec validation intégrée.

```python
from rooter.prompt import Prompt

age = Prompt(text="Âge", type=int, between="0-120").ask()
mode = Prompt(text="Mode", choices=["dev", "prod"], default="dev").ask()
mdp  = Prompt(text="Mot de passe", password=True).ask()
```

| Paramètre | Description |
|-----------|-------------|
| `type` | `str`, `int` ou `float` — la saisie est revalidée jusqu'à être correcte |
| `choices` | Liste de valeurs autorisées |
| `between` | Intervalle `"min-max"` |
| `default` | Valeur renvoyée si l'utilisateur valide à vide |
| `password` | Masque la saisie |

---

### `Progress` — barre de progression

Barre animée affichant le pourcentage et le temps restant.

```python
from rooter.progress import Progress

Progress(title="Téléchargement", width=30, duration=5).start()
```

---

### `Grid` — grille Unicode

Dessine une grille de cellules ; pratique pour des plateaux, des damiers ou des visualisations simples.

```python
from rooter.grid import Grid

grid = Grid(size="3x3", frame_size=3)
grid.set(0, 0, "X", color="red")
grid.set(1, 1, "O", color="green")
grid.show()
```

- `set(y, x, valeur, color)` — remplit une cellule.
- `setLines(...)` / `setColumns(...)` / `setPoints(...)` — remplissent en lot.

---

### `JsonDatabase` — base de données JSON

Une mini-base de données persistée dans des fichiers JSON, avec modèles typés et requêtes conditionnelles.

```python
from rooter.database import Model, JsonDatabase

# 1. Définir le modèle (créé une seule fois)
Model("users", {
    "id":    {"type": "int", "auto_increment": True},
    "name":  {"type": "str"},
    "admin": {"type": "bool", "default": False},
}).create()

# 2. Manipuler les données
db = JsonDatabase("users")
db.insert(keys=["name"], values=["Sasha"])
db.insert(keys=["name", "admin"], values=["Alex", True])

db.show(where="admin = True")          # affichage en tableau
data = db.get(order_by="ASC name")     # récupération en liste
db.update("admin", True, where="id = 1")
db.delete(where="id = 2")
```

- **Modèles typés** : `str`, `int`, `float`, `bool`, `list`, `dict`, `tuple`.
- **Clés spéciales** : `primary`, `auto_increment`, `default`.
- **Opérateurs de condition** : `=`, `!=`, `>`, `<`, `>=`, `<=`.
- **Tri** : `order_by="ASC champ"` ou `"DESC champ"`.

---

### Utilitaires

```python
from rooter import GroupDigits
from rooter.password import getStrenghPassword
from rooter.download import download_file_url

GroupDigits(1000000)              # "1 000 000"
GroupDigits(1000000, ".")         # "1.000.000"

getStrenghPassword("azerty")      # 0 à 3 (faible → très fort)

download_file_url("https://.../fichier.pdf", destination="downloads")
```

---

## 🗂️ Structure du projet

```
rooter/
├── __init__.py     # Cœur : moteur couleurs/styles, print stylé, utilitaires
├── panel.py        # Panel     — boîtes encadrées
├── table.py        # Table     — tableaux
├── menu.py         # Menu      — menus interactifs
├── prompt.py       # Prompt    — invites de saisie validées
├── progress.py     # Progress  — barre de progression
├── grid.py         # Grid      — grille Unicode
├── stack.py        # Stack     — pile (gestion des styles imbriqués)
├── database.py     # JsonDatabase — base de données JSON typée
├── password.py     # Évaluation de robustesse de mot de passe
└── download.py     # Téléchargement de fichier par URL
```

Chaque fichier correspond à un composant autonome, ce qui rend la bibliothèque facile à lire et à étendre.

---

## 🎓 Ce que ce projet m'a apporté

- **Le formatage terminal en profondeur** : codes ANSI, gestion des styles imbriqués via une structure de pile, calcul de largeur en ignorant les balises pour aligner correctement le contenu.
- **La conception d'une API** claire et cohérente, réutilisable d'un projet à l'autre.
- **Le packaging Python** : passer d'un ensemble de scripts à une bibliothèque installable avec `setup.py`.
- **L'organisation modulaire** : séparer les responsabilités, un composant par fichier.

---

## 🔧 Pistes d'amélioration

Ce projet reste perfectible, et j'en assume les limites :

- Rendre `clear()` portable (Windows/Linux/macOS).
- Ajouter des tests automatisés.
- Publier des captures d'écran des composants dans ce README.

---

## 📄 Licence

Distribué sous licence **MIT**. Libre à vous de l'utiliser, le modifier et le partager.
