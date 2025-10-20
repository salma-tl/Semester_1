adresses_ip= ["192.168.0.1","10.0.0.1","172.16.0.1","200.100.50.1","169.254.0.1"]

#Q1
print("la premiere adresse est:",adresses_ip[0])
#Q2
print("la derniere adresse est:",adresses_ip[-1])
#Q3
print("la troisieme adresse est:",adresses_ip[2])
#Q4
adresses_ip.append("172.31.0.1")
#Q5
adresses_ip.remove("200.100.50.1")
print(adresses_ip)
#Q6
print(f"le nombre d'element restants sont: {len(adresses_ip)}")
#Q7
if "192.168.0.1" in adresses_ip:
    print("l'adresse 192.168.0.1 se trouve dans la liste")
else :
    print("l'adresse 192.168.0.1 ne se trouve pas dans la liste")
#Q8
ip="10.0.0.1".split('.')
if int(ip[0])>0 and int(ip[0])<128:
    print("La classe ip de 10.0.0.1 est A")
else :
    print("10.0.0.1 n'est pas de la classe A")
#Q9
adresses_ip.sort()
print("Liste triée :", adresses_ip)
#Q10
x=0
for adresses in adresses_ip :
    premier = int(adresses.split('.')[0])
    if premier >= 192 and premier <= 223:
        x+=1
if x==len(adresses_ip):
    print("toutes les adresses sont de la classe C")
else :
    print("Toutes les adresses n'appartiennent pas à la classe C")
#Q11
occ=0
for adresses in adresses_ip :
    premier = int(adresses.split('.')[0])
    if premier == 200:
        occ+=1
print("le nombre des classes publiques est:", occ)
