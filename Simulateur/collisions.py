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
            return False

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
            return False

    return True


def check_collisions(fig, ofig, scene):
    if check_borders(fig, scene.height(), scene.width()):
        for i in range(len(ofig)):
            if check_rect_coll(fig, ofig[i]):
                if not check_poly_coll(fig, ofig[i]):
                    return False
        return True
    else:
        return False


'''Si collision :
		Est ce que l'objet est déplaçable ?
			Si Oui :
				Le déplacer
			Si Non :
				Rien faire'''


def check_movable(fig, ofig, scene):
    # TODO : Déplacement des objets si c'est possible
    pass
