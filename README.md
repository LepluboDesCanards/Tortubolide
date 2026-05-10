# 🐢 Tortubolide - La Course de Tortues 🏎️

Un projet de programmation orientée objet (POO) en Python utilisant le module graphique `turtle`. Ce jeu simule une course de tortues sur un circuit. 

Les bolides possèdent une **physique d'inertie** : ils ne peuvent changer de vitesse ou de direction que d'une case à la fois par tour. Attention aux collisions ! Percuter un mur vous stoppera net et réduira votre vitesse à zéro.

---

## ✨ Fonctionnalités

* **Physique à inertie** : Contrôlez l'accélération et la décélération de votre tortue.
* **Système de projection (Aide à la visée)** : Affiche à chaque tour vos 5 trajectoires futures possibles (Inertie + Accélération) avec un code couleur :
    * 🔵 **Point Bleu** : Trajectoire sûre.
    * 🔴 **Point Rouge** : Collision imminente (votre vitesse sera réinitialisée à 0).
* **Multijoueur & Bots** : Jouez contre plusieurs robots autonomes dotés de comportements différents (un bot prudent et un bot agressif/fou).
* **Génération dynamique de circuits** : Charge des fichiers de cartes personnalisés au format `.tmap`.

---

## 🛠️ Dépendances

Ce projet a été conçu pour être le plus léger possible. Il utilise exclusivement la **bibliothèque standard de Python 3**. Aucune installation de package tiers (comme `pip`) n'est requise !

* **Python 3.x**
* **Module `turtle`** (Inclus par défaut avec Python)
* **Module `random`** (Inclus par défaut avec Python)

---

## 🚀 Mode d'emploi

### 1. Comment lancer le jeu

Pour démarrer la partie sur la carte par défaut :
1. Téléchargez ou clonez ce dépôt.
2. Assurez-vous d'avoir un dossier nommé `maps` contenant le fichier `dev.tmap` dans le même répertoire que votre script Python.
3. Lancez le script via votre terminal :

```bash
python main.py
```

---

### 2. Comment jouer

Le jeu se joue au **tour par tour**. C'est d'abord au joueur humain de choisir son action, puis les robots jouent automatiquement après un court délai de réflexion.

#### Contrôles au clavier :
À votre tour, appuyez sur l'une des touches suivantes pour appliquer un **vecteur d'accélération** :

| Touche | Action | Vecteur d'accélération |
| :---: | :--- | :---: |
| **`z`** | Accélérer vers le Haut | `(0, -1)` |
| **`x`** | Accélérer vers le Bas | `(0, 1)` |
| **`q`** | Accélérer vers la Gauche | `(-1, 0)` |
| **`d`** | Accélérer vers la Droite | `(1, 0)` |
| **`s`** | Conserver la vitesse (Inertie) | `(0, 0)` |

*Note : Les coordonnées de la grille de jeu ont leur axe vertical inversé (le haut diminue la ligne `y`).*

#### Objectif :
Le premier joueur à franchir la ligne de départ (en rouge) et à effectuer **3 tours complets** remporte la course !

---

### 3. Comment ajouter et personnaliser des cartes

Le jeu charge les circuits à partir de fichiers texte portant l'extension `.tmap`. Vous pouvez concevoir vos propres circuits très simplement !

#### Structure d'un fichier `.tmap` :
* `#` représente un **mur** infranchissable (affiché sous forme de points noirs).
* `0` représente la **ligne de départ / arrivée** (affichée en rouge). C'est aussi là que les tortues feront leur apparition.
* Les **espaces vides** (` `) représentent la piste sur laquelle les tortues peuvent rouler.

#### Exemple de carte personnalisée (`maps/mon_circuit.tmap`) :
```text
#############
#00000000000#
#           #
#   #####   #
#   #   #   #
#   #####   #
#           #
#############
```

#### Charger votre carte dans le jeu :
Dans le code principal, modifiez simplement le chemin d'accès lors de l'instanciation de la classe `Jeu` :

```python
if __name__ == "__main__":
    jeu = Jeu("./maps/mon_circuit.tmap") # Remplacez par le nom de votre fichier
    jeu.screen.mainloop()
```

---
