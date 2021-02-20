"""
Ce projet permet d'utiliser un fichier excel contenant les dépenses faites par une personne
et de retourner des graphiques dynmiques, avec comme BUT d'analyser les dépenses par thème et 
période.

"""


import update_db
import app

 
# --- INIT ---
myApp = app.AppDash()

# --- UPDATING DATABASE ---
update_db.updateAll()   

# --- MAIN PART ---
myApp.launch()

