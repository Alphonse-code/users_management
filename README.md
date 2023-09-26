# users_management
 Projet RestFull API en Django Rest Framework gestion d'utilisateur 
# Gestionnaire d'Utilisateurs avec Django Rest Framework (DRF)

Ce projet est une application web qui permet la gestion des utilisateurs avec des opérations CRUD (Create, Read, Update, Delete) ainsi que les fonctionnalités de login, registration (inscription), et forgot password (mot de passe oublié) en utilisant Django Rest Framework (DRF).

## Fonctionnalités

- **CRUD d'Utilisateurs :**
    - **Create** : Permet aux administrateurs ou aux utilisateurs autorisés de créer un nouvel utilisateur en fournissant des informations telles que le nom, l'adresse e-mail et le mot de passe.
    - **Read** : Permet aux utilisateurs autorisés de lire les informations d'autres utilisateurs.
    - **Update** : Permet aux utilisateurs autorisés de mettre à jour leurs propres informations.
    - **Delete** : Permet aux administrateurs ou aux utilisateurs autorisés de supprimer des comptes utilisateur.

- **Login (Connexion) :**
    - Les utilisateurs peuvent se connecter en fournissant leur adresse e-mail et leur mot de passe.
    - Un jeton d'authentification (JWT) est généré pour l'utilisateur connecté et renvoyé au client pour les requêtes ultérieures.

- **Registration (Inscription) :**
    - Les utilisateurs non enregistrés peuvent s'inscrire en fournissant leur nom, leur adresse e-mail et leur mot de passe.
    - La vérification de l'adresse e-mail en double est gérée.
    - Un jeton d'authentification est renvoyé au nouvel utilisateur après une inscription réussie.

- **Forgot Password (Mot de passe oublié) :**
    - Les utilisateurs peuvent réinitialiser leur mot de passe s'ils l'ont oublié.
    - Un lien de réinitialisation de mot de passe est envoyé à l'adresse e-mail de l'utilisateur.
    - L'utilisateur peut saisir un nouveau mot de passe après avoir suivi le lien.

## Configuration et Exécution

1. Clonez ce référentiel sur votre machine locale.

2. Installez les dépendances en utilisant `pip` (assurez-vous d'utiliser un environnement virtuel) :
   ```shell
   pip install -r requirements.txt
