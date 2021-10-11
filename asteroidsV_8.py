#projet 1 T NSI LVC 2021-2022


#imports
import os
import sys
import random
import time
import math
import turtle
if sys.platform == "win32":
    import winsound

#CONSTANTES
RAYON = 400
TROU_NOIR = (500,500)

turtle.setup(width=800, height=800)
turtle.speed(0)
turtle.bgcolor("black")
turtle.title("Asteroids")
turtle.ht()
turtle.setundobuffer(1)
turtle.tracer(0)

class Animation(turtle.Turtle):
    """
    classe fille de Turtle donc  hérite des attributs position
    direction et
    méthodes de la classe Turtle
    définit  une forme
    -triangle(vaisseau) rayon 11.5
    -cercle (missile) rayon 2.5
    -asteroide rayon 40,20,10

    Une animation est définie par son centre (x,y), son rayon, sa vitesse
    screen.register_shape()
    """
    def __init__(self, forme, couleur,x0,y0,vitesse,rayon):
        """
        RAYON = 400 px rayon de l'univers
        """
        turtle.Turtle.__init__(self, shape = forme)
        self.speed(0)
        self.pencolor(couleur)
        self.fd(0)
        #apparaît en (x0,y0)
        self.penup()
        self.goto(x0, y0)
        #le rayon du cercle circonscrit de l'animation
        self.rayon = rayon
        self.vitesse = vitesse

    def avancer(self):
        #l'univers est un tore
        if self.xcor() > RAYON - self.rayon:
            self.setx(-RAYON + self.rayon)
        elif self.xcor() < -RAYON + self.rayon:
            self.setx(RAYON - self.rayon)
        if self.ycor() >  RAYON - self.rayon:
            self.sety(-RAYON + self.rayon)
        elif self.ycor() < -RAYON + self.rayon:
            self.sety(RAYON - self.rayon)

        self.fd(self.vitesse)

    def toucher(self,other):
        return  self.distance(other.pos()) <= self.rayon +\
         other.rayon

class Vaisseau(Animation):
    """
    Vaisseau hérite de Animation qui hérite de Turtle donc Vaisseau a les attributs
    de Turtle , position ,direction etc...
    """
    #attributs de classe
    rayon = 11.5
    angle = 20


    def __init__(self):

        Animation.__init__(self, "triangle", 'white',
         0, 0,0,Vaisseau.rayon)
        self.shapesize(0.9, 1,outline=None)
        self.vitesse = 0
        self.tirs = []
        self.nb_vies = 3
        self.niveau = 1
        self.score = 0

    def tourner_a_droite(self):
        self.right(Vaisseau.angle)

    def tourner_a_gauche(self):
        self.left(Vaisseau.angle)

    def accelerer(self):
        self.vitesse += 1

    def ralentir(self):
        if self.vitesse < 1:
            self.vitesse = 0
        elif self.vitesse > 0:
            self.vitesse -= 1

    def kill(self):
        self.nb_vies = 0

    def devier(self,direction,vitesse_a):
        """
        Si un astéroide touche le vaisseau
        ce dernier est dévié de sa trajectoire
        en prenant la direction de l'asteroide
        """
        if self.vitesse == 0:
            self.setheading(direction)
            self.vitesse = vitesse_a
            self.fd(20)
        else:
            self.setheading(self.heading()-180)
            self.fd(20)


    def tirer(self):
        nom_os = sys.platform
        if nom_os == 'Darwin':
            os.system("afplay tir.wav&")

        elif nom_os == 'Linux':
            os.system("aplay tir.wav &")

        elif nom_os == 'win32':
            winsound.PlaySound("tir.wav", winsound.SND_ASYNC)

        self.tirs.append(Missile(self.xcor(),self.ycor(),
        self.heading(),self.vitesse+ 5))

class Asteroide(Animation):

    def __init__(self,taille, x0, y0,vitesse):

        """
        taille = 1 gros astéroide
        taille = 0.5 moyen
        taille = 0.25 petit
        """
        Animation.__init__(self,'asteroide','white', x0, y0, vitesse, taille*40)
        self.shapesize(stretch_wid=taille, stretch_len=taille,
        outline=None)
        self.vitesse = vitesse
        self.taille = taille
        self.setheading(random.randint(0,360))
        self.rayon = taille*40

    def exploser(self,asteroides,vaisseau):
        if self.taille != 0.25:
            self.taille /=2
            self.rayon //=2
            #réduction de moitié
            self.shapesize(self.taille, self.taille,outline=None)
            #augmentation de la vitesse
            self.vitesse += 0.5
            #apparition d'un autre astéroïde de même taille
            #et de même vitesse
            asteroides.append(Asteroide(self.taille,self.xcor()+self.rayon,
                                        self.ycor(),self.vitesse))

            #évolution du score en fonction de la taille
            if self.taille == 1:
                vaisseau.score += 20
            elif self.taille == 0.5:
                vaisseau.score += 50

        else:
            vaisseau.score += 100
            self.goto(TROU_NOIR)
            asteroides.remove(self)

class Missile(Animation):
    rayon = 2.5

    def __init__(self,x0, y0,direction,vitesse):

        Animation.__init__(self, "triangle", "yellow",
         x0, y0,vitesse,Missile.rayon)
        self.shapesize(0.15, 0.25,outline=None)
        self.setheading(direction)

    def avancer(self):
        """
        On surcharge la méthode car une missile
        qui sort de l'univers (l'écran) va dans un trou noir
        """

        if abs(self.xcor()) > RAYON or abs(self.ycor()) > RAYON:
            self.vitesse = 0
            self.goto(TROU_NOIR)

        else:
            self.fd(self.vitesse)

class Soucoupe(Animation):
    pass

class Jeu:

    def __init__(self):

        #le terrain de jeu
        self.ecran = turtle.Screen()
        #on définit la forme asteroide
        asteroide =( (-34.6,20), (-34.6,-20), (0,-40),
        (34.6,-20),(34.6,20),(20,20),(0,40))
        #on l'enregistre
        self.ecran.register_shape('asteroide', asteroide)
        #définir et enregistrer la soucoupe volante

        #le marqueur du score
        self.stylo = turtle.Turtle()
        self.stylo.ht()
        self.stylo.speed(0)
        self.stylo.color("white")
        self.stylo.pensize(3)

        #commencer une partie
        self.commencer_une_partie = False
        #écouteur
        turtle.onkeypress(self.commencer, "Up")
        turtle.listen()
        #ouvrir le fichier texte des scores en lecture
##        with open("scores.txt",'r',encoding='utf-8') as fichier:
##            self.liste_scores = fichier.read().splitlines()

    def commencer(self):
        self.commencer_une_partie = True
        #un attribut  asteroides de type list

        self.asteroides = [Asteroide(1,random.randint(-300,300),
        random.randint(-300,300),0.2) for i in range(3)]

        #un attribut de type Vaisseau
        self.vaisseau = Vaisseau()
        #des écouteurs d'évènements
        turtle.onkeypress(self.vaisseau .tourner_a_gauche, "Left")
        turtle.onkeypress(self.vaisseau .tourner_a_droite, "Right")
        turtle.onkeypress(self.vaisseau .accelerer, "Up")
        turtle.onkeypress(self.vaisseau .ralentir, "Down")

        turtle.onkeypress(self.vaisseau.tirer, "space")

        turtle.onkeypress(self.vaisseau .kill, "k")

        turtle.listen()

    def passer_au_niveau_superieur(self,niveau):
        self.asteroides = [Asteroide(1,
                                     random.randint(-300,300),
        random.randint(-300,300),0.2) for i in range(niveau+2)]

    def partie_est_en_cours(self):
        return self.vaisseau.nb_vies != 0

    def jouer(self):
        #changer de niveau
        if len(self.asteroides) == 0:
            self.vaisseau.niveau += 1
            self.passer_au_niveau_superieur(self.vaisseau.niveau)

        #faire bouger les animations
        self.vaisseau.avancer()

        for missile in self.vaisseau.tirs:
            missile.avancer()
        for asteroide in self.asteroides:
            asteroide.avancer()

        #tenir compte des interactions entre
        #les animations
            if self.vaisseau.toucher(asteroide):
                self.vaisseau.devier(asteroide.heading(),
                                     asteroide.vitesse)
                self.vaisseau.nb_vies += 1

            for tir in self.vaisseau.tirs:
                if tir.toucher(asteroide):

                    nom_os = sys.platform
                    if nom_os == 'Darwin':
                        os.system("afplay explosion.wav&")

                    elif nom_os == 'Linux':
                        os.system("aplay explosion.wav &")

                    elif nom_os == 'win32':
                        winsound.PlaySound("explosion.wav", winsound.SND_ASYNC)
                    asteroide.exploser(self.asteroides,self.vaisseau)
                    tir.goto(TROU_NOIR)
                    self.vaisseau.tirs.remove(tir)
                elif tir.xcor() == TROU_NOIR[0]:
                    self.vaisseau.tirs.remove(tir)

    def ecran_accueil(self):
        self.stylo.undo()
        msg = "APPUYEZ SUR UP POUR COMMENCER"
        self.stylo.penup()
        self.stylo.goto(-180, 150)
        self.stylo.write(msg, font=("Arial", 16, "normal"))

    def afficher(self):

        msg = "NIVEAU : {}  NB_VIES : {} SCORE: {}   ".format(self.vaisseau.niveau,
                                                              self.vaisseau.nb_vies,
                                                              self.vaisseau.score)
        self.stylo.undo()
        self.stylo.penup()
        self.stylo.goto(-360, 350)
        self.stylo.write(msg, font=("Arial", 16, "normal"))

    def aquisition_valeur(self,path):
        """
        Retourne un dictionnaire avec 'Score' la clé d'une liste des scores
                                      'Auteur' la clé d'une liste des auteurs des scores

        Paramètre:
        ----------
        path:
            str:le chemin pour accéder au fichier score.

                /!\ la syntaxe du fichier des scores doit être comme suit:
                |score|:|auteur|;

        Exemple d'utilisation:
        ----------------------
        >>d = aquisition_valeur("scores.txt")
        >>d['Auteur'][0]

        retourne le premier auteur du document scores.txt qui se trouve dan sle repertoire courant

        ####

        >>d= aquisition_valeur("scores.txt")
        >>d['Score'][1]

        retourne le deuxième score du document scores.txt qui se trouve dans le repertoire courant
        """
        f = open(path,'r')
        s = f.read()
        q,t = 0,0
        score_pred = {'Score':[],'Auteur':[]}
        for i in s:
            q += 1
            if i==":":
                score_pred['Score'].append(s[t:q-1])
                t = q
            elif i == ";":
                score_pred['Auteur'].append(s[t:q-1])
                t = q + 1
        return score_pred

    def bilan_partie(self,path):
        msg = "TON SCORE EST: {} ".format(self.vaisseau.score)
        self.stylo.penup()
        self.stylo.goto(-80, 10)
        self.stylo.write( msg,
            font=("Arial", 22, "normal"))
        # si le score du joueur est strictement supérieur
        # au plus petit des dix meilleurs scores, insérer le score et
        # le pseudo du joueur dans le fichier scores.txt à sa place
        d_score = self.aquisition_valeur(path)#['Score']
        k = 0
        print(d_score)
        for score in d_score['Score']:
            if int(score) < self.vaisseau.score:
                nom = str(self.ecran.textinput("Asteroids", "Quel est ton pseudo ?"))
                if len(d_score['Score']) == 10:
                    d_score['Score'].pop()
                    d_score['Auteur'].pop()
                d_score['Score'].insert(k,self.vaisseau.score)
                d_score['Auteur'].insert(k,nom)
                break
            k += 1
        self.rentrer_score(d_score,path)
        print(d_score)

    def rentrer_score(self,dico,path):
        #f = open(path,'a')
        pass


    def boucle_principale(self,path):
        while True:
            #écran d'accueil
            while not self.commencer_une_partie:
                self.ecran_accueil()
            #une partie en cours
            while self.partie_est_en_cours():
                turtle.update()
                self.jouer()
                self.afficher()
            #on efface les dessins des tortues
            self.ecran.getcanvas().delete('all')
            #bilan de la partie
            self.bilan_partie(path)
            #arrêt du jeu ou nouvelle partie pour un nouveau joueur
            choix = self.ecran.textinput("Asteroids", "Une nouvelle partie ?(O/N)")
            if choix == 'N' or choix == 'n':
                break
            elif choix == 'O' or choix == 'o':
                #on retourne vers l'écran d'accueil pour une nouvelle
                #partie
                self.commencer_une_partie = False
                self.vaisseau.nb_vies = 3
                turtle.onkeypress(self.commencer, "Up")
                turtle.listen()
        #self.ecran.ondestroy()
#------------MAIN------------
if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose = False)
    jeu = Jeu()
    jeu.boucle_principale("scores.txt")
    turtle.bye()
