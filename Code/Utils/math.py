def is_collided(x1, y1, l1, h1, x2, y2, l2, h2):
    return (x1 < x2 + l2 and
            x1 + l1 > x2 and
            y1 < y2 + h2 and
            y1 + h1 > y2)
