class Personne:
    def __init__(self,nom,adresse):
        self.nom = nom
        self.adresse = adresse
    def afficher(self):
        print("Nom:",self.nom)
        print("Adresse:",self.adresse)

class Employee(Personne):
    def __init__(self,nom,adresse,cnss):
        self.cnss = cnss
        Personne.__init__(self,nom,adresse)
    def afficher(self):
        Personne.afficher(self)
        print("Cnss: ", self.cnss)

class Enseignant(Personne):
    def __init__(self,nom,adresse,cnops):
        self.cnops = cnops
        Personne.__init__(self,nom,adresse)
    def afficher(self):
        Personne.afficher(self)
        print("Cnops: ", self.cnops)

class Etudiant(Personne):
    def __init__(self,nom,adresse,cne):
        self.cne = cne
        Personne.__init__(self,nom,adresse)
    def afficher(self):
        Personne.afficher(self)
        print("Cne: ", self.cne)

p1=Employee("John","A1555",12000)
p1.afficher()
p2=Enseignant("Hain","B2266",3224)
p2.afficher()
p3=Etudiant("Tiouli","C4885",87556)
p3.afficher()
