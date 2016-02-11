#!/usr/bin/python3.4

def check_borders(fig, size_x, size_y):
    for i in range(fig.nbp):
        pt = fig.shape.at(i)

        if pt.x() < 0 or pt.x() > size_x:
            return False

        if pt.y() < 0 or pt.y() > size_y:
            return False
    return True


def check_rect_coll(fig, ofig):
    frect = fig.shape.boundingRect()  # retourne le rectangle qui englobe le polygone
    orect = ofig.shape.boundingRect()

    if frect.left() > orect.right() or frect.right() < orect.left() or frect.top() > orect.bottom() or frect.bottom() < orect.top():
        return False
    else:
        print("collision carré")
        return True


def check_poly_coll(fig, ofig):
    for i in range(fig.nbp):
        P = fig.shape.at(i)
        c = True

        for j in range(ofig.nbp):
            A = ofig.shape.at(j)
            if j == ofig.nbp - 1:
                B = ofig.shape.at(0)
            else:
                B = ofig.shape.at(j + 1)

            D = (B.x() - A.x(), B.y() - A.y())
            T = (P.x() - A.x(), P.y() - A.y())

            det = D[0] * T[1] - D[1] * T[0]
            if det < 0:
                c = False
                break
        if c:
            return False #collision poly

    for i in range(ofig.nbp):
        P = ofig.shape.at(i)
        c = True

        for j in range(fig.nbp):
            A = fig.shape.at(j)
            if j == fig.nbp - 1:
                B = fig.shape.at(0)
            else:
                B = fig.shape.at(j + 1)

            D = (B.x() - A.x(), B.y() - A.y())
            T = (P.x() - A.x(), P.y() - A.y())

            det = D[0] * T[1] - D[1] * T[0]
            if det < 0:
                c = False
                break
        if c:
            return False #pas collision poly

    print("pas collision poly")
    return True

'''
Check les collisions, d'abord par rectangle vu que c'est super rapide, puis si il y a collision
on check avec la méthode par polygones
Si il y a collision on retourne l'objet collisionné
'''
def check_collisions(fig, ofig, scene):

    collisionedObjects = []

    if check_borders(fig, scene.height(), scene.width()):
        for obj in ofig:
            if check_rect_coll(fig, obj):
                if check_poly_coll(fig, obj):
                    collisionedObjects.append(obj)

    return collisionedObjects

'''Si collision :
		Est ce que l'objet est déplaçable ?
			Si Oui :
				Le déplacer
			Si Non :
				Rien faire'''


def get_movable(fig, ofig, scene):


    # TODO : Déplacement des objets si c'est possible
    pass
