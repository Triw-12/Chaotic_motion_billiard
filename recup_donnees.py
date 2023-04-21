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
    #print(nb1,nb2)
    return float(nb1), float(nb2)


def recup(nom_fichier):
    fichier = open("modele/"+nom_fichier,"r",encoding="utf-8")
    ligne = fichier.readline().strip()
    i = deuxpoint(ligne)
    mur = ligne[i:].split(" ")
    for r in range(len(mur)):
        try:
            mur[r] = val_tupl(mur[r])
        except :
            assert False, "Ce ne sont pas des tuples"
    #print(mur)


    ligne = fichier.readline().strip()
    i = deuxpoint(ligne)
    cercle = ligne[i:].split(" ")
    cercle_f = []
    for r in range(0,len(cercle),2):
        try:
            cercle_f.append([val_tupl(cercle[r]),float(cercle[r+1])])
        except:
            assert False, "Format incorrect"
    #print(cercle_f)
    
    
    ligne = fichier.readline().strip()
    i = deuxpoint(ligne)
    boule = ligne[i:].split(" ")
    boule_f = []
    for r in range(0,len(boule),3):
        try:
            print(boule[r],boule[r+1],boule[r+2])
            boule_f.append([val_tupl(boule[r]),val_tupl(boule[r+1]),boule[r+2]])
        except:
            assert False, "Format incorrect"
    #print(boule_f)

    ligne = fichier.readline().strip()
    i = deuxpoint(ligne)
    rayon = ligne[i:]
    try:
        rayon = float(rayon)
    except:
        assert False, "Format incorrect"
    
    ligne = fichier.readline().strip()
    i = deuxpoint(ligne)
    dt = ligne[i:]
    try:
        dt = float(dt)
    except:
        assert False, "Format incorrect"

    fichier.close()
    return mur,cercle_f,boule_f,rayon,dt


if __name__ == "__main__":
    m,c,b,r,t = recup("senai.txt")
    print(m,c,b,r,t)