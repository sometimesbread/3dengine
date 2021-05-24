class vec3:
    x = float(0)
    y = float(0)
    z = float(0)
    
class vec2:
    x = float(0)
    y = float(0)

class triangle:
    point1 = vec3()
    point2 = vec3()
    point3 = vec3()


class mesh:
    m = []

class matrix4x4:
    m = [[float(0),float(0),float(0),float(0)],
        [float(0),float(0),float(0),float(0)],
        [float(0),float(0),float(0),float(0)],
        [float(0),float(0),float(0),float(0)]]    

test = vec3()
test.x = float(69)
test.y = float(420)
test.z = float(666)