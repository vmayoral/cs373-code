colors = [['red', 'green', 'green', 'red' , 'red'],
          ['red', 'red', 'green', 'red', 'red'],
          ['red', 'red', 'green', 'green', 'red'],
          ['red', 'red', 'red', 'red', 'red']]

measurements = ['green', 'green', 'green' ,'green', 'green']

motions = [[0,0],[0,1],[1,0],[1,0],[0,1]]
sensor_right = 0.7
p_move = 0.8


def show(p):
    for i in range(len(p)):
        print p[i]

#DO NOT USE IMPORT
#ENTER CODE BELOW HERE
#ANY CODE ABOVE WILL CAUSE
#HOMEWORK TO BE GRADED
#INCORRECT

p = []
nelems = len(colors)*len(colors[1])
for c in colors:
    subp = []
    for e in c: 
        subp.append(1./nelems)
    p.append(subp)

def psum(p):
    sum = 0
    for i in p:
        for j in i:
            sum+=j
    return sum

def sense(p, Z):
    q = []
    for i in range(len(p)):
        subq = []
        for j in range(len(p[i])):
            hit = (Z == colors[i][j])
            subq.append(p[i][j] * (hit * sensor_right + (1 - hit)*(1 - sensor_right)))  # convolution
        q.append(subq)

    # normalize the p distribution
    qsum = 0
    for elem in q:
        qsum += sum(elem)
    for i in range(len(q)):
        for j in range(len(q[i])):
            q[i][j] = q[i][j] / qsum
    return q
    
'''
[0,0]   -> no move
[0,1]   -> right
[0,-1]  -> left
[1,0]   -> down
[-1,0]  -> up

'''
def move(p,U):
    q = []
    for i in range(len(p)):
        subq = []
        for j in range(len(p[i])):
            subq.append(p[(i-U[0]) % len(p)][(j-U[1]) % len(p[i])] * p_move + p[i][j] * (1 - p_move))
        q.append(subq)
    return q


for k in range(len(measurements)):
    p = move(p, motions[k])
    p = sense(p, measurements[k])

#Your probability array must be printed 
#with the following code.


show(p)
#import AfficheHistogram
#fenetre = AfficheHistogram.AfficheHistogramme ( p, colors )
#fenetre.mainloop()

