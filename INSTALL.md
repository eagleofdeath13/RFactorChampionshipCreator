# Guide d'Installation - rFactor Championship Creator

## 📦 Prérequis

**Aucun !**

Cette version packagée inclut tout le nécessaire :
- ✅ Python intégré
- ✅ Interface web React intégrée
- ✅ Toutes les dépendances

**Vous avez uniquement besoin de :**
- Windows 10 ou supérieur
- Une installation fonctionnelle de **rFactor**

---

## 🚀 Installation

### Étape 1 : Extraction

Si vous avez téléchargé le fichier ZIP :
1. **Extrayez** le contenu du ZIP dans un dossier de votre choix
   - Exemple : `C:\rFactor_Tools\ChampionshipCreator\`
   - ⚠️ **Évitez** les chemins avec des espaces ou caractères spéciaux

### Étape 2 : Configuration

1. **Ouvrez** le fichier `config.json` avec un éditeur de texte (Notepad++, VSCode, ou même Bloc-notes)

2. **Modifiez** le chemin vers votre installation rFactor :

   ```json
   {
     "rfactor_path": "C:/Program Files (x86)/Steam/steamapps/common/rFactor"
   }
   ```

   **Exemples de chemins valides :**
   - Steam : `C:/Program Files (x86)/Steam/steamapps/common/rFactor`
   - Installation personnalisée : `D:/Games/rFactor`
   - Autre disque : `E:/rFactor`

   ⚠️ **Important :**
   - Utilisez des **slashes (/)** et non des backslashes (\)
   - Ou doublez les backslashes : `C:\\Program Files\\...`

3. **Sauvegardez** le fichier

### Étape 3 : Lancement

1. **Double-cliquez** sur `RUN_APP.bat`

2. Une console va s'ouvrir et afficher :
   ```
   ====================================================================
       rFactor Championship Creator
   ====================================================================

   Starting server on http://127.0.0.1:5000

   📋 Application URLs:
      Frontend:  http://localhost:5000/
      API Docs:  http://localhost:5000/api/docs

   Press Ctrl+C to stop the server
   ```

3. **Votre navigateur par défaut** s'ouvrira automatiquement (après ~3 secondes)

4. Si le navigateur ne s'ouvre pas automatiquement, ouvrez manuellement :
   **http://localhost:5000**

---

## ✅ Vérification

Une fois l'interface ouverte dans votre navigateur, vous devriez voir :
- 🏠 Page d'accueil avec les sections : Talents, Véhicules, Circuits, Championnats
- Si tout fonctionne correctement, vous pouvez naviguer dans l'interface

---

## 🛠️ Utilisation

### Créer un Championnat Personnalisé

1. Allez dans la section **"Championnats"**
2. Cliquez sur **"Créer un Championnat"**
3. Suivez les étapes :
   - **Étape 1 :** Informations de base (nom, description)
   - **Étape 2 :** Sélection des véhicules
   - **Étape 3 :** Association des pilotes aux véhicules
   - **Étape 4 :** Sélection et ordre des circuits
   - **Étape 5 :** Options et validation

4. Une fois créé, le championnat sera disponible dans **rFactor** :
   - Lancez rFactor
   - Allez dans **"Race"** → **"Select Series"**
   - Cherchez votre championnat (préfixé par `M_`)

### Gérer les Talents (Pilotes)

1. Section **"Talents"**
2. Créez, modifiez ou importez des pilotes depuis CSV
3. Les talents peuvent ensuite être assignés aux véhicules lors de la création d'un championnat

### Gérer les Véhicules

1. Section **"Véhicules"**
2. Consultez tous les véhicules disponibles
3. Recherchez et filtrez par classe ou fabricant

### Gérer les Circuits

1. Section **"Circuits"**
2. Consultez tous les circuits disponibles
3. Recherchez par nom

---

## ⚠️ Dépannage

### Le navigateur ne s'ouvre pas automatiquement

→ Ouvrez manuellement : **http://localhost:5000**

### Erreur "config.json not found"

→ Vérifiez que le fichier `config.json` existe dans le même dossier que l'exécutable

### Erreur "Port 5000 already in use"

→ Une autre application utilise le port 5000. Options :
1. Fermez l'autre application
2. Ou modifiez le port dans `src/main.py` (nécessite rebuild)

### L'application ne trouve pas mes fichiers rFactor

→ Vérifiez dans `config.json` que :
1. Le chemin est correct
2. Les slashes sont dans le bon sens (`/` et non `\`)
3. Le chemin pointe vers le **dossier racine** de rFactor (celui qui contient `GameData/`, `rFm/`, etc.)

### Les championnats créés n'apparaissent pas dans rFactor

→ Vérifiez que :
1. Le fichier `.rfm` a été créé dans `rFactor/rFm/M_*.rfm`
2. Les véhicules ont été copiés dans `rFactor/GameData/Vehicles/M_*/`
3. Relancez rFactor complètement

---

## 🔄 Mise à Jour

Pour mettre à jour vers une nouvelle version :
1. **Sauvegardez** votre `config.json`
2. **Supprimez** l'ancien dossier
3. **Extrayez** la nouvelle version
4. **Restaurez** votre `config.json`

---

## 📝 Désinstallation

Pour désinstaller :
1. **Supprimez** simplement le dossier de l'application
2. **Optionnel** : Supprimez les championnats créés dans rFactor :
   - `rFactor/rFm/M_*.rfm`
   - `rFactor/GameData/Vehicles/M_*/`

---

## 📞 Support

Pour toute question ou problème :
- Consultez la documentation complète dans `README.md`
- Vérifiez les logs dans la console qui s'est ouverte
- Ouvrez une issue sur le dépôt GitHub du projet

---

## 🎮 Bon championnats !

Profitez de vos championnats personnalisés sur rFactor ! 🏁
