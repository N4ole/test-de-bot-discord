# 🤖 Discord Moderation Bot

Un bot Discord modulaire, sécurisé et personnalisable pour gérer un serveur   
avec un système d'owner et de logs

---

## 🚀 Fonctionnalités principales

### 🧩 Modération
- `!clear <nombre>` – Supprime des messages
- `!kick @user [raison]` – Expulse un membre
- `!ban @user [raison]` – Bannit un membre
- `!mute @user [raison]` – Mute un utilisateur
- `!unmute @user` – Unmute un utilisateur

### ⚙️ Utilitaires
- `!ping` – Vérifie la latence
- `!hello` – Petit message de bienvenue
- `!uptime` – Affiche depuis combien de temps le bot tourne
- `!status` – Donne la version, le ping, le nombre de serveurs et l'état du mode debug

### 🛡️ Système de Logs
- `!setlog #salon` – Définit le salon où sont envoyés les logs
- Logs :
  - 🔨 Bannissements
  - 👢 Kicks
  - 🔇 Mutes/Unmutes
  - 🗑️ Suppression de messages
  - ✏️ Édition de messages

### 👑 Commandes Owner (restreintes)
- `!reload [commande]` – Recharge une commande à la volée
- `!debug on/off` – Active ou désactive le mode debug
- `!addowner @user` – Ajoute un owner
- `!removeowner @user` – Supprime un owner (sauf l’ID protégé)
- `!listowners` – Liste les owners

---

## 🧠 Architecture

📁 commands/        → Toutes les commandes standard (!ping, !ban...)
📁 admin/           → Commandes réservées aux owners (!reload, !debug...)
📁 utils/           → Fonctions utilitaires (log, config, sécurité)
📁 data/            → Fichiers JSON : config, owners, log_config
📄 engine.py        → Instanciation du bot, gestion des events
📄 main.py          → Démarre le bot
📄 .env             → Contient la variable DISCORD_TOKEN

---

## 🔐 Owner System

- Owners stockés dans `data/owners.json`
- Un ID peut être **protégé** (non supprimable)
- Logs automatiques si quelqu’un tente de t’enlever ou d’ajouter un owner
- Impossible d’ajouter des bots comme owner

---

## 🐞 Mode Debug

- Active via `!debug on`
- Permet d’afficher en console des logs spécifiques
- Visible dans `!status`
- Écriture directe dans `data/config.json`

---

## 🧑‍💻 Développeur

Créé par **naole77** et **sharox_78** 🧠  
Conçu pour être **simple, fiable et évolutif**.

---
