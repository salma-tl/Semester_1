import tkinter as tk
from tkinter import ttk, messagebox
from database import *

# ---------- Fenêtre principale ----------
root = tk.Tk()
root.title("Hôtel Manager")
root.geometry("850x600")


# ---------- Styles ----------
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview",
                background="#ffffff",
                foreground="#000000",
                rowheight=25,
                fieldbackground="#ffffff")
style.map("Treeview", background=[('selected', '#4CAF50')])

btn_style = {"font": ("Arial", 10, "bold"), "fg": "white", "width": 15}

# ---------- Onglets ----------
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

from PIL import Image, ImageTk  # pip install pillow

tab_accueil = tk.Frame(notebook)
notebook.add(tab_accueil, text="Accueil")

# Charger l'image et la redimensionner pour tout l'onglet
img = Image.open("hotel.jpg")
img = img.resize((850, 600), Image.Resampling.LANCZOS)  # adapter à la taille de la fenêtre
photo = ImageTk.PhotoImage(img)

# Label pour afficher l'image
bg_label = tk.Label(tab_accueil, image=photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # image occupe tout l'onglet

# Texte centré sur l'image
lbl_welcome = tk.Label(tab_accueil, text="Bienvenue sur la plateforme de gestion de l'hôtel",
                       font=("Arial", 24, "bold"), bg="#000000", fg="white")
lbl_welcome.place(relx=0.5, rely=0.5, anchor="center")

lbl_soustitre = tk.Label(tab_accueil, text="Gérez facilement vos clients, chambres et réservations",
                         font=("Arial", 16), bg="#000000", fg="white")
lbl_soustitre.place(relx=0.5, rely=0.6, anchor="center")


creer_tables()
# ---------- Onglet Clients ----------
tab_clients = tk.Frame(notebook)
notebook.add(tab_clients, text="Clients")

frame_add_client = tk.LabelFrame(tab_clients, text="Ajouter un client", font=("Arial", 12, "bold"))
frame_add_client.pack(padx=10, pady=10, fill="x")

tk.Label(frame_add_client, text="CIN:").grid(row=0, column=0)
tk.Label(frame_add_client, text="Nom:").grid(row=0, column=1)
tk.Label(frame_add_client, text="Téléphone:").grid(row=0, column=2)

entry_cin = tk.Entry(frame_add_client)
entry_nom = tk.Entry(frame_add_client)
entry_tel = tk.Entry(frame_add_client)

entry_cin.grid(row=1, column=0, padx=5, pady=5)
entry_nom.grid(row=1, column=1, padx=5, pady=5)
entry_tel.grid(row=1, column=2, padx=5, pady=5)

def action_ajouter_client():
    cin = entry_cin.get()
    nom = entry_nom.get()
    tel = entry_tel.get()
    if not cin or not nom:
        messagebox.showwarning("Attention", "CIN et Nom sont obligatoires !")
        return
    try:
        ajouter_client(cin, nom, tel)
        messagebox.showinfo("Succès", "Client ajouté avec succès ")
        entry_cin.delete(0, tk.END)
        entry_nom.delete(0, tk.END)
        entry_tel.delete(0, tk.END)
        charger_clients()
        entry_client['values'] = [c[0] + " - " + c[1] for c in afficher_clients()]

    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible d'ajouter le client : {e}")

btn_add_client = tk.Button(frame_add_client, text="Ajouter", command=action_ajouter_client, bg="#4CAF50", **btn_style)
btn_add_client.grid(row=1, column=3, padx=10, pady=5)

# Treeview Clients
frame_table_client = tk.LabelFrame(tab_clients, text="Liste des clients", font=("Arial", 12, "bold"))
frame_table_client.pack(padx=10, pady=10, fill="both", expand=True)

cols_client = ("CIN", "Nom", "Téléphone")
tree_client = ttk.Treeview(frame_table_client, columns=cols_client, show="headings")
for col in cols_client:
    tree_client.heading(col, text=col)
    tree_client.column(col, width=200, anchor="center")
tree_client.pack(fill="both", expand=True, padx=10, pady=10)

def charger_clients():
    for i in tree_client.get_children():  #sert a ne pas repeter toutes les lignes une autre fois lors de lajout dune info
        tree_client.delete(i)
    for c in afficher_clients():
        tree_client.insert("", "end", values=c)

# Supprimer client
def action_supprimer_clients():
    selected = tree_client.selection()
    if not selected:
        messagebox.showwarning("Attention", "Sélectionnez un client à supprimer !")
        return
    id_cl = tree_client.item(selected[0])["values"][0]
    confirmer = messagebox.askyesno("Confirmer", f"Supprimer le client {id_cl} ?")
    if confirmer:
        supprimer_clients(id_cl)
        charger_clients()

btn_supprimer_clients = tk.Button(tab_clients, text="Supprimer client sélectionné", command=action_supprimer_clients, bg="#f44336", **btn_style)
btn_supprimer_clients.pack(pady=5)


charger_clients()

# ---------- Onglet Chambres ----------
tab_chambres = tk.Frame(notebook)
notebook.add(tab_chambres, text="Chambres")

frame_add_chambre = tk.LabelFrame(tab_chambres, text="Ajouter une chambre", font=("Arial", 12, "bold"))
frame_add_chambre.pack(padx=10, pady=10, fill="x")

tk.Label(frame_add_chambre, text="Type:").grid(row=0, column=0, padx=5, pady=5)
tk.Label(frame_add_chambre, text="Prix:").grid(row=0, column=1, padx=5, pady=5)
tk.Label(frame_add_chambre, text="Disponibilité:").grid(row=0, column=2, padx=5, pady=5)

entry_type = ttk.Combobox(frame_add_chambre, values=["single", "double", "suite"])
entry_type.grid(row=1, column=0, padx=5, pady=5)
entry_prix = tk.Entry(frame_add_chambre)
entry_prix.grid(row=1, column=1, padx=5, pady=5)
entry_dispo = ttk.Combobox(frame_add_chambre, values=[1, 0])
entry_dispo.grid(row=1, column=2, padx=5, pady=5)
entry_dispo.set(1)

def action_ajouter_chambre():
    type_ch = entry_type.get()
    prix = entry_prix.get()
    dispo = entry_dispo.get()
    if not type_ch or not prix:
        messagebox.showwarning("Attention", "Type et prix obligatoires !")
        return
    try:
        prix = float(prix)
        dispo = int(dispo)
        ajouter_chambre(type_ch, prix, dispo)
        messagebox.showinfo("Succès", "Chambre ajoutée ")
        entry_type.set('')
        entry_prix.delete(0, tk.END)
        entry_dispo.set(1)
        charger_chambres()
        entry_chambre['values'] = chambres_disponibles()
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible d'ajouter la chambre : {e}")

btn_add_chambre = tk.Button(frame_add_chambre, text="Ajouter", command=action_ajouter_chambre, bg="#4CAF50", **btn_style)
btn_add_chambre.grid(row=1, column=3, padx=10, pady=5)

# Treeview Chambres
frame_table_chambre = tk.LabelFrame(tab_chambres, text="Liste des chambres", font=("Arial", 12, "bold"))
frame_table_chambre.pack(padx=10, pady=10, fill="both", expand=True)

cols_chambre = ("ID", "Type", "Prix", "Disponibilité")
tree_chambre = ttk.Treeview(frame_table_chambre, columns=cols_chambre, show="headings", height=10)
for col in cols_chambre:
    tree_chambre.heading(col, text=col)
    tree_chambre.column(col, width=150, anchor="center")
tree_chambre.pack(fill="both", expand=True, padx=10, pady=10)

def charger_chambres():
    for i in tree_chambre.get_children():
        tree_chambre.delete(i)
    for c in afficher_chambres():
        tree_chambre.insert("", "end", values=c)



charger_chambres()

# ---------- Onglet Réservations ----------
tab_reservations = tk.Frame(notebook)
notebook.add(tab_reservations, text="Réservations")

frame_add_res = tk.LabelFrame(tab_reservations, text="Ajouter une réservation", font=("Arial", 12, "bold"))
frame_add_res.pack(padx=10, pady=10, fill="x")

tk.Label(frame_add_res, text="Client:").grid(row=0, column=0, padx=5, pady=5)
tk.Label(frame_add_res, text="Chambre:").grid(row=0, column=1, padx=5, pady=5)
tk.Label(frame_add_res, text="Date début (YYYY-MM-DD):").grid(row=0, column=2, padx=5, pady=5)
tk.Label(frame_add_res, text="Date fin (YYYY-MM-DD):").grid(row=0, column=3, padx=5, pady=5)

# Combobox pour clients et chambres
client_values = [c[0] + " - " + c[1] for c in afficher_clients()]
entry_client = ttk.Combobox(frame_add_res, values=client_values, width=20)
entry_client.grid(row=1, column=0, padx=5, pady=5)

# Chambres disponibles
def chambres_disponibles():
    return [str(c[0]) + " - " + c[1] for c in afficher_chambres() if c[3] == 1]

entry_chambre = ttk.Combobox(frame_add_res, values=chambres_disponibles(), width=20)
entry_chambre.grid(row=1, column=1, padx=5, pady=5)

entry_date_debut = tk.Entry(frame_add_res)
entry_date_debut.grid(row=1, column=2, padx=5, pady=5)
entry_date_fin = tk.Entry(frame_add_res)
entry_date_fin.grid(row=1, column=3, padx=5, pady=5)

def action_ajouter_reservation():
    client_sel = entry_client.get()
    chambre_sel = entry_chambre.get()
    date_debut = entry_date_debut.get()
    date_fin = entry_date_fin.get()

    if not client_sel or not chambre_sel or not date_debut or not date_fin:
        messagebox.showwarning("Attention", "Tous les champs sont obligatoires !")
        return

    id_client = client_sel.split(" - ")[0]
    id_chambre = int(chambre_sel.split(" - ")[0])
    if not chambre_disponible(id_chambre, date_debut, date_fin):
        messagebox.showwarning("Attention", "Cette chambre est déjà réservée pour cette période !")
        return

    try:
        ajouter_reservation(id_client, id_chambre, date_debut, date_fin)
        messagebox.showinfo("Succès", "Réservation ajoutée ")
        entry_client.set('')
        entry_chambre.set('')
        entry_date_debut.delete(0, tk.END)
        entry_date_fin.delete(0, tk.END)
        charger_reservations()
        # Actualiser la liste des chambres disponibles
        entry_chambre['values'] = chambres_disponibles()
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible d'ajouter la réservation : {e}")

btn_add_res = tk.Button(frame_add_res, text="Ajouter", command=action_ajouter_reservation, bg="#4CAF50", **btn_style)
btn_add_res.grid(row=1, column=4, padx=10, pady=5)

# Treeview Réservations
frame_table_res = tk.LabelFrame(tab_reservations, text="Liste des réservations", font=("Arial", 12, "bold"))
frame_table_res.pack(padx=10, pady=10, fill="both", expand=True)

cols_res = ("ID", "Client", "Chambre", "Date début", "Date fin")
tree_res = ttk.Treeview(frame_table_res, columns=cols_res, show="headings", height=10)
for col in cols_res:
    tree_res.heading(col, text=col)
    tree_res.column(col, width=150, anchor="center")
tree_res.pack(fill="both", expand=True, padx=10, pady=10)

def charger_reservations():
    for i in tree_res.get_children():
        tree_res.delete(i)
    for r in afficher_reservations():
        tree_res.insert("", "end", values=r)


def action_supprimer_reservation():
    selected = tree_res.selection()
    if not selected:
        messagebox.showwarning("Attention", "Sélectionnez une reservation à supprimer !")
        return
    id_res = tree_res.item(selected[0])["values"][0]
    confirmer = messagebox.askyesno("Confirmer", f"Supprimer la reservation {id_res} ?")
    if confirmer:
        supprimer_reservations(id_res)
        charger_reservations()

btn_refresh_res = tk.Button(tab_reservations, text=" Supprimer une reservation", command=action_supprimer_reservation, bg="#f44336", **btn_style)
btn_refresh_res.pack(pady=5)

charger_reservations()

root.mainloop()
