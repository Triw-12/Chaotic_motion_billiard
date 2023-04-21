


def deuxpoint(ligne):
    i = 0
    while ligne[i] != ":":
        assert ligne[i] != "\n","Mauvaise configuration ( ':' introuvable)"
        i += 1
    return i+2

def val_tupl(tpl):
    nb = tpl.split(",")
    nb1 = nb[0][1:]
    nb2 = nb[1][:-1]
    print(nb1,nb2)
    return float(nb1), float(nb2)


def recup(nom_fichier):
    fichier = open(nom_fichier,"r",encoding="utf-8")
    ligne = fichier.readline().strip()
    i = deuxpoint(ligne)
    mur = ligne[i:].split(" ")
    for r in range(len(mur)):
        try:
            mur[r] = val_tupl(mur[r])
        except :
            assert False, "Ce ne sont pas des tuples"
    print(mur)




    ligne = fichier.readline().strip()
    i = deuxpoint(ligne)
    cercle = ligne[i:].split(" ")
    for r in range(0,len(cercle),2):
        try:
            cercle[r] = [val_tupl(cercle[r]),float(cercle[r+1])]
        except:
            assert False, "Format incorrect"
    
    
    
    
    
    ligne = fichier.readline().strip()


    fichier.close()
    return mur,cercle


if __name__ == "__main__":
    recup("billiard_simple.txt")