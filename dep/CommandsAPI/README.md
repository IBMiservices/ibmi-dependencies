# commandsAPI

## Description
`commandsAPI` est un projet qui fournit des API pour exécuter des commandes CL et des programmes sur IBM i.

`commandsAPI` is a project that provides APIs to execute CL commands and programs on IBM i.

## Structure du projet / Project Structure
Le projet est structuré comme suit :
The project is structured as follows:

### Détails des dossiers et fichiers principaux / Main Folders and Files Details
- **core/** : Contient les fichiers source principaux pour les commandes et les programmes.
  - `commands.sqlrpgle` : Fichier source RPGLE pour les commandes.
  - `COMMANDS.BND` : Fichier de définition des exports de programme.
  - `SERVICES.BNDDIR` : Fichier de script pour créer et ajouter des entrées dans le répertoire de liaison.
  
  Contains the main source files for commands and programs.
  - `commands.sqlrpgle` : RPGLE source file for commands.
  - `COMMANDS.BND` : Program export definition file.
  - `SERVICES.BNDDIR` : Script file to create and add entries to the binding directory.

- **reference/** : 
  Contient les fichiers d'inclusion RPGLE.
  - `commands.RPGLEINC` : Fichier d'inclusion pour les prototypes de commandes.
  
  Contains RPGLE include files.
  - `commands.RPGLEINC` : Include file for command prototypes.

- **.vscode/** : Contient les configurations pour Visual Studio Code.
  - `actions.json` : Actions configurées pour la construction et la compilation.
  - `tasks.json` : Tâches configurées pour l'installation des dépendances.
  
  Contains configurations for Visual Studio Code.
  - `actions.json` : Configured actions for building and compiling.
  - `tasks.json` : Configured tasks for dependency installation.

- **dependencies.json** : Fichier de configuration des dépendances du projet.
  
  Project dependency configuration file.

- **install_deps.py** : Script Python pour installer les dépendances.
  
  Python script to install dependencies.

- **Rules.mk** : Fichier Makefile pour la construction du projet.
  
  Makefile for building the project.

- **LICENSE** : Licence du projet (GNU GPL v3).
  
  Project license (GNU GPL v3).

- **README.md** : Ce fichier.
  
  This file.

## Installation des dépendances / Installing Dependencies
Pour installer les dépendances du projet, exécutez la commande suivante :
To install the project dependencies, run the following command:
```sh
python install_deps.py
```

## Construction du projet / Building the Project
Pour construire le projet, utilisez les actions configurées dans Visual Studio Code : 
To build the project, use the configured actions in Visual Studio Code:

### Build all : 
Construit l'ensemble du projet. Builds the entire project.
### Build current : 
Construit le fichier actuellement ouvert. Builds the currently open file.

## Exécution des commandes / Executing Commands
Le projet fournit une API pour exécuter des commandes CL via la procédure execCommand définie dans commands.sqlrpgle. 
The project provides an API to execute CL commands via the execCommand procedure