file=open("Table_de_multiplication.txt","w")
for i in range(1,11):
    file.write(f"La table de multiplication de {i} \n")
    for j in range(1,11):
        prod = i*j
        file.write(f"{i}x{j}={prod}\n")
        file.write("\n")
