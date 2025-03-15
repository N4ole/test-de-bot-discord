# 🚀 Bot Discord - Python

Un bot Discord **modulaire et personnalisable** développé avec **discord.py**.  
Il inclut des commandes de **modération**, **utilitaires**, **logs**, **watchlist**, et bien plus !

---

## 📌 1. Fonctionnalités Principales  

✅ **Modération** (`!ban`, `!kick`, `!mute`, `!warn`, `!modlogs`)  
✅ **Logs** (`message_deleted`, `message_edited`, `message_sent`, `voice_logs`)  
✅ **Système de Watchlist** (`!watchlist`, `!unwatch`, suivi des activités des membres surveillés)  
✅ **Commandes d'information** (`!botinfo`, `!userinfo`, `!serverinfo`, `!avatar`)  
✅ **Système de permissions et d'accès administrateur**  
✅ **Personnalisation des salons de logs** (`!setlog`, `!setvoicelog`, `!showlogs`)  
✅ **Commandes diverses (math, roll, etc.)**  
✅ **Système de gestion vocale** (`mute`, `unmute`, `deaf`, `undeaf`, changement de salon vocal)  

---



### 🔑 2. Configuration du `.env`
Créer un fichier `.env` avec :
```ini
DISCORD_TOKEN=VOTRE_TOKEN_BOT
```

### 🚀 3. Démarrer le bot
```sh
python bot.py
```

---

## 📜 Commandes Disponibles

### 🔹 **Commandes Générales**
| Commande | Description |
|----------|------------|
| `!help` | Affiche la liste des commandes disponibles (paginé) |
| `!ping` | Vérifie la latence du bot |
| `!roll` | Génère un nombre aléatoire |
| `!math add <a> <b>` | Additionne deux nombres |
| `!math multiply <a> <b>` | Multiplie deux nombres |
| `!math divide <a> <b>` | Divise deux nombres (vérifie division par zéro) |

### 🔹 **Commandes de Modération**
| Commande | Description |
|----------|------------|
| `!botinfo` | affiche les informations du bot |
| `!userinfo @user` | affiche les informations d'un membres|
| `!serverinfo` | affiche les information du serveur |
| `!avatar @user` | affiche l'avatar d'un utilisateur |

### 🔹 **Commandes de Modération**
| Commande | Description |
|----------|------------|
| `!ban @user <raison>` | Bannit un utilisateur (admin uniquement) |
| `!kick @user <raison>` | Expulse un utilisateur (admin uniquement) |
| `!mute @user <raison>` | Rend un membre muet (admin uniquement) |
| `!unmute @user` | rétablis le son pour un membre |
| `!warn @user <raison>` | Donne un avertissement à un utilisateur |
| `!modlogs @user` | Affiche l'historique des sanctions d'un membre |

### 🔹 **Commandes de Logs**
| Commande | Description |
|----------|------------|
| `!setlog <sent/deleted/edited> #channel` | Change le salon où les logs sont envoyés |
| `!showlogs` | Affiche les salons de logs actuels |
| `!clearlogs <sent/deleted/edited>` | Vide un type de logs |
| `!setvoicelog #channel` | définit le salon des logs vocaux |
| `!showvoicelog` | affiche le salon actuel des logs vocaux |

### 🔹 **Système de Watchlist**
| Commande | Description |
|----------|------------|
| `!watchlist @user` | Ajoute un utilisateur à la watchlist et crée un salon privé |
| `!unwatch @user` | Retire un utilisateur de la watchlist et supprime son salon |
| `!watchlistlogs` | Affiche les logs des utilisateurs surveillés |

### 🔹 **Commandes Administratives**
| Commande | Description |
|----------|------------|
| `!reload <module>` | Recharge un module sans redémarrer le bot |
| `!togglelog <sent/deleted/edited>` | Active ou désactive un type de logs |
| `!adminonly` | Vérifie si l'utilisateur est admin |
| `!checkperms @user` | Vérifie les permissions d'un utilisateur |

---

## 📁 Structure du Projet
```plaintext
📂 bot/
 ├── 📂 commands/         
 │   ├── moderation.py    
 │   ├── logs_config.py   
 │   ├── watchlist.py     
 │   ├── help.py          
 │   ├── admin.py         
 │   ├── info.py          
 │   └── ...
 ├── 📂 events/           
 │   ├── message_logs.py  
 │   ├── watchlist_events.py 
 │   ├── bot_status.py  
 │   └── ...
 ├── 📂 logs/             
 │   ├── logs.py              
 │   ├── modlogs.py           
 │   ├── logs_config.py        
 │   ├── voice_logs.py        
 │   ├── logging_utils.py     
 │   └── ...
 ├── 📂 data/             
 │   ├── server_config.json  
 │   ├── logs_sent.json      
 │   ├── logs_deleted.json   
 │   ├── logs_edited.json    
 │   ├── voice_logs.json  
 │   ├── watchlist.json      
 │   └── modlogs.json      
 ├── bot.py               
 ├── requirements.txt     
 ├── .env                 
 ├── README.md            
 └── ...

```

---

## 🛠️ Dépendances
📌 Pour installer les dépendances `requirements.txt`.
```sh
pip install -r requirements.txt

```


