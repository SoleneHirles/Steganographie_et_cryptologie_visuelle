

from tkinter import *
fen_princ = Tk()
fen_princ.title("Projet ISN")
fen_princ.geometry("275x200")



#Fonction pour coder une image dans une image (cryptographie)
def code_image():
    import numpy, random
    from PIL import Image
    import math

    def seuil(x):
        """Fonction qui permet de séparer les pixels en deux groupes"""
        if x<128:
            return 0 #transformation en pixel noir
        else:
            return 255 #transformation en pixel blanc

    def noirblanc(r,g,b):
        """Fonction qui permet de créer des pixels noirs et des pixels blancs"""
        if r==0 and g==0 and b==0:
            return(0,0,0) #pixel noir
        else:
            return(255,255,255) #pixel blanc

    #Corps principal
    image_A= input("copier l'url de votre image secrète avec l'extention")
    image_secrete = Image.open(image_A) #On lit l'image

    #Binarisation



    a,b=image_secrete.size #on prend la taille de l'image
    imgF = Image.new(image_secrete.mode,image_secrete.size)
    for i in range(b):
        for j in range(a):
            pixel = image_secrete.getpixel((j,i)) # récupération du pixel

            p = noirblanc(seuil(pixel[0]), seuil(pixel[1]), seuil(pixel[2]))

            # composition de la nouvelle image

            imgF.putpixel((j,i), p)
    imgF.save("image secrete.png")
    liste_secrete=imgF.getdata()


    #Génération de la clé
    tableau_aleatoire = numpy.random.randint(256, size =(a,b))# une tableau de la taille de l'image avec des entier entre 0 et 256, 256 exclus.
    cle=Image.fromarray(tableau_aleatoire) #on convertit le tableau en une image, qui est la clé
    #On cherche à transformer la clé en une image en noir et blanc
    liste_cle = cle.getdata() #création de la liste des pixels


    listetrans=[seuil(x) for x in liste_cle] #on applique la fonction sur la liste

    result_cle = Image.new("L",(a,b)) #création de la nouvelle image
    result_cle.putdata(listetrans)
    result_cle.save("clé.png") #On sauvegarde la clé dans un fichier afin qu'elle puisse être envoyer pour le décodage

    liste_codee=[]
    i=0

    while i< len(liste_secrete):

        if liste_secrete[i][0] == listetrans[i]: #On compare les éléments des deux listes
           liste_codee.append(0) # On ajoute la valeur d'un pixel noir dans la liste des pixels de l'image finale
        else:
           liste_codee.append(255) # On ajoute la valeur d'un pixel blanc dans la liste des pixels de l'image finale
        i+=1
    imgcodee =  Image.new("L",(a,b))
    imgcodee.putdata(liste_codee)
    imgcodee.save("image_codee.png")


#Fonction pour coder une image dans une image (cryptographie)
def decode_image():
    import numpy, random
    from PIL import Image
    import math

    def seuil(x):
        """Fonction qui permet de séparer les pixels en deux groupes"""
        if x<128:
            return 0 #transformation en pixel noir
        else:
            return 255 #transformation en pixel blanc

    def noirblanc(r,g,b):
        """Fonction qui permet de créer des pixels noirs et des pixels blancs"""
        if r==0 and g==0 and b==0:
            return(0,0,0) #pixel noir
        else:
            return(255,255,255) #pixel blanc

    #Corps principal
    image_A= input("copier l'url de votre image codee avec l'extention")
    image_codee = Image.open(image_A) #On lit l'image
    image_cle = Image.open("clé.png")



    a,b=image_codee.size #on prend la taille de l'image


    liste_codee=image_codee.getdata()
    liste_cle=image_cle.getdata()

    listetrans=[seuil(x) for x in liste_cle] #on applique la fonction sur la liste





    liste_decodee=[]
    i=0

    while i< len(liste_codee):

        if liste_codee[i] == listetrans[i]: #On compare les éléments des deux listes
           liste_decodee.append(0) # On ajoute la valeur d'un pixel noir dans la liste des pixels de l'image finale
        else:
           liste_decodee.append(255) # On ajoute la valeur d'un pixel blanc dans la liste des pixels de l'image finale
        i+=1
    imgdecodee =  Image.new("L",(a,b))
    imgdecodee.putdata(liste_decodee)
    imgdecodee.save("image_decodee.png")

#Fonction de codage de stéganographie
def stega_codage():
    from PIL import Image

    image_A=input("copier le nom de votre image secrète ainsi que l'extention")
    image_B=input("copier le nom de votre image conteneure ainsi que l'extention ")
    image_secrete= Image.open(image_A) #On lit les images grâce au module PIL Image
    image_conteneur= Image.open(image_B)

    #Les fonctions
    def cache (n):
        """cache les bits de poids faibles pour seulement laisser les bits de poids forts visibles"""
        return n & 0b11110000 #On effectue un ET logique entre la valeur d'un octet correspondant à une composante de couleur des
        # pixels et un nombre binaire indiqué sur python par 0b qui permet de mettre à zéro les quatres bits de poids faibles

    def decalage (n,decale=4):
        """ cette fonction a pour but de faire passer des bits de poids forts en bits de poids faibles"""
        return n >> decale #On effectue un décalage de 4 bits vers la droite dans l'octet, ainsi les quatres bits de poids forts
        # deviennent quatres bits de poids faibles

    #Le corps principal du programme
    if image_secrete.size==image_conteneur.size:
        l,h=image_conteneur.size
        image_finale= Image.new('RGB', (l,h))
        for x in range (l): #On parcourt chaque ligne
            for y in range (h): # on parcourt chaque colonne
                rouge1, vert1, bleu1= image_conteneur.getpixel((x,y))

                rouge1, vert1, bleu1= cache(rouge1), cache(vert1), cache(bleu1)

                rouge2, vert2, bleu2= image_secrete.getpixel((x,y))

                rouge2, vert2, bleu2= decalage(rouge2), decalage(vert2), decalage(bleu2)

                image_finale.putpixel((x,y),(rouge1+rouge2, vert1+vert2, bleu1+bleu2))



        image_finale.save('image_finale.png') #On sauveagarde la nouvelle image créée
        image_finale.show() #On l'affiche
    else:
        print("Les images doient être de la même taille")


#Fonction de décodage de stéganographie
def stega_decodage():
    from PIL import Image

    image_B=input("copier le nom de votre image ainsi que l'extention ")
    image_conteneur= Image.open(image_B)

    #Les fonctions
    def cache (n):
        """la fonction masque sert à mettre à 0 les quatre bits de poids forts"""
        return n & 0b00001111

    def decalage (n,decale=4):
        """la fonction decalage_gauche sert à décaler les quatre bits de poids faibles vers la gauche, ils deviennent ainsi des bits de poids fort"""
        return n << decale

    #Le corps principal du programme
    l,h=image_conteneur.size # On récupère la longueur et la hauteur de l'image visible
    image_finale= Image.new('RGB', (l,h)) #On créer une nouvelle image en couleur et de la même taille que les images précédentes
    for x in range (l): #On parcourt chaque ligne
        for y in range (h): # on parcourt chaque colonne
            rouge1, vert1, bleu1= image_conteneur.getpixel((x,y)) #On récupère les trois composants de couleurs des pixel de
            # l'image qui restera visible
            rouge1, vert1, bleu1= cache(rouge1), cache(vert1), cache(bleu1) #on applique la fonction masque sur les trois composants des pixels de l'image
            rouge1, vert1, bleu1=decalage(rouge1), decalage(vert1), decalage(bleu1) #on applique la fonction decalage_gauche sur les trois composants des pixels de l'image
            image_finale.putpixel((x,y),(rouge1, vert1, bleu1)) #on modifie la couleur du pixel avec les trois composants des pixels obtenus pour avoir l'image finale

    image_finale.save('image_finale.png') #On sauveagarde la nouvelle image créée
    image_finale.show() #On l'affiche



# Création du cadre-conteneur pour les menus
zoneMenu = Frame(fen_princ, borderwidth=3, bg='#557788')
zoneMenu.pack(fill=X)
zoneMenu = Frame(fen_princ, borderwidth=3, bg='#557788')
zoneMenu.pack(fill=X)
# Création de l'onglet codage
menucrypto = Menubutton(zoneMenu, text='Cryptographie', width='20', borderwidth=2, bg='light blue', activebackground='white',relief = RAISED)
menucrypto.grid(row=0,column=1)
# Création de l'onglet decodage
menustegano = Menubutton(zoneMenu, text='Stéganographie', width='20', borderwidth=2, bg='light blue', activebackground='white',relief = RAISED)
menustegano.grid(row=0,column=2)
# Création d'un menu défilant
menuDeroulant1 = Menu(menucrypto, tearoff = 0)

menuDeroulant1.add_command(label= 'Coder une image', command= code_image)

menuDeroulant1.add_command(label= 'Decoder une image', command= decode_image)
# Attribution du menu déroulant au sous menu cliquer
menucrypto.configure(menu=menuDeroulant1)
menuDeroulant2 = Menu(menustegano, tearoff = 0)
menuDeroulant2.add_command(label='Codage', command= stega_codage )
menuDeroulant2.add_command(label='Décodage', command= stega_decodage)
# Attribution du menu déroulant au sous menu cliquer
menustegano.configure(menu=menuDeroulant2)
# Boucle principale
fen_princ.mainloop()