import sqlite3

# Connexion à la base
def connexion():
    return sqlite3.connect("Hotel.db")


# Création des tables
def creer_tables():
    db = connexion()
    cur = db.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS chambres (id INTEGER PRIMARY KEY AUTOINCREMENT,type TEXT CHECK(type IN ('suite','single','double')),prix REAL,disponibilite INTEGER NOT NULL CHECK(disponibilite IN (0,1)) DEFAULT 1)")

    cur.execute("CREATE TABLE IF NOT EXISTS clients (CIN TEXT PRIMARY KEY ,nom TEXT,telephone TEXT)")

    cur.execute("CREATE TABLE IF NOT EXISTS reservations (id INTEGER PRIMARY KEY AUTOINCREMENT,id_client INTEGER,id_chambre INTEGER,date_debut TEXT,date_fin TEXT,FOREIGN KEY(id_client) REFERENCES clients(CIN), FOREIGN KEY(id_chambre) REFERENCES chambres(id))")

    db.commit()
    db.close()


# ---------- CHAMBRES ----------
def ajouter_chambre(type_chambre, prix, dispo):
    db = connexion()
    cur = db.cursor()
    cur.execute("INSERT INTO chambres(type, prix, disponibilite) VALUES (?, ?, ?)",(type_chambre, prix, dispo))
    db.commit()
    db.close()


def afficher_chambres():
    db = connexion()
    cur = db.cursor()
    cur.execute("SELECT * FROM chambres")
    chambres = cur.fetchall()
    db.close()
    return chambres

def chambre_disponible(id_chambre, date_debut, date_fin):
    db = connexion()
    cur = db.cursor()
    query = """
        SELECT COUNT(*) 
        FROM reservations 
        WHERE id_chambre = ? 
        AND (
            (date_debut <= ? AND date_fin >= ?) OR
            (date_debut <= ? AND date_fin >= ?) OR
            (? <= date_debut AND ? >= date_fin)
        )
    """
    cur.execute(query, (id_chambre, date_debut, date_debut, date_fin, date_fin, date_debut, date_fin))
    count = cur.fetchone()[0]
    db.close()
    return count == 0  # True si aucune réservation en conflit


# ---------- CLIENTS ----------
def ajouter_client(CIN, nom, telephone):
    db = connexion()
    cur = db.cursor()
    cur.execute("INSERT INTO clients(CIN, nom, telephone) VALUES (?, ?, ?)",(CIN, nom, telephone))
    db.commit()
    db.close()


def afficher_clients():
    db = connexion()
    cur = db.cursor()
    cur.execute("SELECT * FROM clients")
    clients = cur.fetchall()
    db.close()
    return clients

def supprimer_clients(id_client):
    db = connexion()
    cur = db.cursor()
    cur.execute("DELETE FROM clients WHERE CIN=?", (id_client,))
    db.commit()
    db.close()

# ---------- RESERVATIONS ----------
def ajouter_reservation(id_client, id_chambre, date_debut, date_fin):
    db = connexion()
    cur = db.cursor()
    cur.execute("INSERT INTO reservations(id_client, id_chambre, date_debut, date_fin) VALUES (?, ?, ?, ?)",
                (id_client, id_chambre, date_debut, date_fin))
    # Mettre la chambre comme non disponible
    db.commit()
    db.close()


def afficher_reservations():
    db = connexion()
    cur = db.cursor()
    cur.execute("SELECT r.id, c.nom, ch.type, r.date_debut, r.date_fin FROM reservations r JOIN clients c ON r.id_client = c.CIN JOIN chambres ch ON r.id_chambre = ch.id")
    reservations = cur.fetchall()
    db.close()
    return reservations

def supprimer_reservations(id_res):
    db = connexion()
    cur = db.cursor()
    cur.execute("DELETE FROM reservations WHERE id=?", (id_res,))
    db.commit()
    db.close()
