# -*- coding: cp1252 -*-
#Displays the matrixs p and colors given in the Homework 1.4
#
#   How to use it :
#
#   Just replace the line:
#                   show(p)
#   by those ones:
#                   #show(p)
#                   import AfficheHistogram
#                   fenetre = AfficheHistogram.AfficheHistogramme ( p, colors )
#                   fenetre.mainloop()
#
#Have fun :)

from Tkinter import *

class AfficheHistogramme(Tk):
    
    def __init__(self, p, grille):
        Tk.__init__(self)
        # p est la table de probabilités
        # grille est la grille de couleurs des cases
        self.title( 'Affichage histogramme')
        #dimensions de la grille:
        self.larg = 50          #square size
        self.ecart = 5          #square tab
        self.dimx = len(p[0])   #number of squares ( horizontally )
        self.dimy = len(p)      #number of squares ( vertically )
        self.can = Canvas( self,
                          width= self.ecart + (self.larg+self.ecart)*self.dimx,
                          height = self.ecart + (self.larg+self.ecart)*self.dimy,
                          bg ='white')
        self.can.pack(side =TOP, padx =self.ecart, pady =self.ecart)
        self.DessineGrille( p, grille )
    
    def DessineGrille(self, p, grille ):
        #find max probability value:
        maxi = 0
        for y in range(self.dimy):
            for x in range(self.dimx):
                if maxi < p[y][x]:
                    maxi = p[y][x]
        
        for y in range(self.dimy):
            for x in range(self.dimx):
                hgx = self.ecart + ( self.ecart + self.larg ) * x
                hgy = self.ecart + ( self.ecart + self.larg ) * y
                bdx = self.ecart + ( self.ecart + self.larg ) * x + self.larg
                bdy = self.ecart + ( self.ecart + self.larg ) * y + self.larg
                couleur = grille[y][x]
                proba = p[y][x]
                if maxi == proba:
                    self.can.create_rectangle ( hgx, hgy, bdx, bdy, fill = couleur, width=5 )
                else:
                    self.can.create_rectangle ( hgx, hgy, bdx, bdy, fill = couleur )
                self.can.create_text ( (hgx+bdx)/2, (hgy+bdy)/2, text = str(round(proba,3)), fill = 'black' )

if __name__ == "__main__":
    #Test code:
    p = [ [ .1, .2, .3 ],
         [ .2, .0, .2 ] ]
    colors = [ [ 'green', 'red'  , 'green' ],
              [ 'red'  , 'green',  'red'  ] ]
    
    fenetre = AfficheHistogramme ( p, colors )
    fenetre.mainloop()