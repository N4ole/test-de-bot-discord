# 🚀 Bot Discord - Python

Un bot Discord **modulaire et personnalisable** développé avec **discord.py**.  
Il inclut des commandes de **modération**, **utilitaires**, **logs**, **watchlist**, et bien plus !

---

## 📌 1. Fonctionnalités Principales

✅ **Modération** (`!ban`, `!kick`, `!mute`, `!warn`)  
✅ **Logs d'activité** (`message_deleted`, `message_edited`, `message_sent`)  
✅ **Système de Watchlist** (`!watchlist`, `!unwatch`, suivi des activités des membres surveillés)  
✅ **Système de permissions et d'accès administrateur**  
✅ **Personnalisation des salons de logs** (`!setlog`, `!showlogs`)  
✅ **Système de commandes paginées avec `!help`**  
✅ **Commandes diverses (math, roll, etc.)**  

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
| `!ban @user <raison>` | Bannit un utilisateur (admin uniquement) |
| `!kick @user <raison>` | Expulse un utilisateur (admin uniquement) |
| `!mute @user <raison>` | Rend un membre muet (admin uniquement) |
| `!warn @user <raison>` | Donne un avertissement à un utilisateur |
| `!modlogs @user` | Affiche l'historique des sanctions d'un membre |

### 🔹 **Commandes de Logs**
| Commande | Description |
|----------|------------|
| `!setlog <sent/deleted/edited> #channel` | Change le salon où les logs sont envoyés |
| `!showlogs` | Affiche les salons de logs actuels |
| `!clearlogs <sent/deleted/edited>` | Vide un type de logs |

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
 │   └── ...              
 ├── 📂 events/           
 │   ├── message_logs.py  
 │   ├── watchlist_events.py 
 │   └── ...
 ├── 📂 data/             
 │   ├── server_config.json  
 │   ├── logs_sent.json      
 │   ├── logs_deleted.json   
 │   ├── logs_edited.json    
 │   └── watchlist.json      
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


