import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from recup_donnees import recup

liste_point,liste_point_cercle,liste_boules,rayon_boule,dt = recup("billiard_simple.txt")


x_mod = [liste_point[i][0] for i in range(len(liste_point))]
y_mod = [liste_point[i][1] for i in range(len(liste_point))]


XMAX = max([liste_point[i][0] for i in range(len(liste_point))])   +  1
YMAX = max([liste_point[i][1] for i in range(len(liste_point))])   +  1
pres = max(XMAX,YMAX)

rayon_boule  = 0.275
dt = 0.01


def scalaire (v1,v2):
    return v1.real*v2.real + v1.imag*v2.imag

def vectorielle(v1,v2) :
    return abs(v1.imag*v2.real - v2.imag*v1.real)

class Droite :
    def __init__ (self,x1,y1,x2,y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.vect = (x2-x1) + (y2-y1)*1j
        self.unit = self.vect/abs(self.vect)
    def collision(self,b):
        if vectorielle(self.vect,(b.vect.real-self.x1) + (b.vect.imag-self.y1)*1j)<=dt*pres*10 and b.vect.real <= max(self.x1,self.x2) + pres*dt and b.vect.real >= min(self.x1,self.x2) - pres*dt:
            print("Collision !")
            return True
        else :
            return False
    def re_unit(self):
        self.unit = self.vect/abs(self.vect)

class Cercle :
    def __init__(self,rayon,x0,y0):
        assert(rayon >0)
        self.r = rayon
        self.x0 = x0
        self.y0 = y0
    def vecteur(self,b):
        return Droite(b.vect.real,b.vect.imag,self.x0,self.y0)
    def tangente(self,b):
        v = self.vecteur(b)
        v.vect = v.vect*1j
        v.re_unit()
        return v
    def collision(self,b):
        v = self.vecteur(b)
        if abs(abs(v.vect)-self.r)<pres/4*dt:
            print("Collision c!")
            return True
        else :
            return False



class Boule :
    def __init__ (self,x,y,vx,vy,c) :
        self.vect = x + y*1j
        self.vvect = vx + vy*1j
        self.color = c
        self.w = 0
    def rebond_d(self,d):
        self.vvect = 2*scalaire(d.unit,self.vvect)*(d.unit) - self.vvect
        return self.vvect.real,self.vvect.imag
    def rebond_c(self,c):
        return self.rebond_d(c.tangente(self))


global liste_droite
global liste_cercle
liste_droite = [Droite(liste_point[i][0],liste_point[i][1],liste_point[i+1][0],liste_point[i+1][1]) for i in range(len(liste_point)-1)]
liste_cercle = [Cercle(liste_point_cercle[i][1],liste_point_cercle[i][0][0],liste_point_cercle[i][0][1]) for i in range(len(liste_point_cercle))]



def get_pos(t=0):
    """A generator yielding the ball's position at time t."""
    boules = [Boule(liste_boules[i][0][0],liste_boules[i][0][1],liste_boules[i][1][0],liste_boules[i][1][1],liste_boules[i][2]) for i in range(len(liste_boules))]
    while True:
        t += dt
        posx = []
        posy = []
        for boule in boules:
            for droite1 in liste_droite:
                if droite1.collision(boule):
                    boule.rebond_d(droite1)
            for cercle in liste_cercle:
                if cercle.collision(boule):
                    boule.rebond_c(cercle)
            boule.vect += boule.vvect * dt
            posx.append(boule.vect.real)
            posy.append(boule.vect.imag)
        yield posx,posy

def init():
    """Initialize the animation figure."""
    ax.set_xlim(0, XMAX)
    ax.set_ylim(0, YMAX)
    ax.set_xlabel('$x$ /m')
    ax.set_ylabel('$y$ /m')
    line.set_data(xdata, ydata)
    line2.set_data(xdata2, ydata2)
    ball1.center = liste_boules[0][0]
    ball2.center = liste_boules[1][0]
    return line,line2, ball1,ball2#height_text

def animate(pos):
    """For each frame, advance the animation to the new position, pos."""
    x, y = pos
    xdata.append(x[0])
    ydata.append(y[0])
    line.set_data(xdata, ydata)
    xdata2.append(x[1])
    ydata2.append(y[1])
    line2.set_data(xdata2, ydata2)
    ball1.center = (x[0], y[0])
    ball2.center = (x[1], y[1])
    return line,line2, ball1, ball2 #height_text ## LA VIRGULE EST SUPER MEGA IMPORTANTE (i.e sinon ça marche pas)

# Set up a new Figure, with equal aspect ratio so the ball appears round.
fig, ax = plt.subplots()
ax.set_aspect('equal')

# These are the objects we need to keep track of.
ball1 = plt.Circle(liste_boules[0][0], rayon_boule,fc=liste_boules[0][2])
ball2 = plt.Circle(liste_boules[1][0], rayon_boule,fc=liste_boules[1][2])
line, = ax.plot([], [],color=liste_boules[0][2] ,lw=2) #La virgule est importante
line2, = ax.plot([],[],color=liste_boules[1][2],lw=2)

ax.plot(x_mod,y_mod,'k-')
ax.add_patch(ball1)
ax.add_patch(ball2)
for i in range (len(liste_point_cercle)):
    ax.add_patch(plt.Circle(liste_point_cercle[i][0],liste_point_cercle[i][1],fill=False))

xdata, ydata = [], []
xdata2, ydata2 = [], []

interval = 1000*dt
ani = animation.FuncAnimation(fig, animate, get_pos, blit=True,
                      interval=interval, repeat=False, init_func=init)
plt.show()

