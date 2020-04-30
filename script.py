import mdl
from display import *
from matrix import *
from draw import *

def run(filename):
    """
    This function runs an mdl script
    """
    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print("Parsing failed.")
        return

    view = [0,
            0,
            1];
    ambient = [50,
               50,
               50]
    light = [[0.5,
              0.75,
              1],
             [255,
              255,
              255]]

    areflect = [0.1,
            0.1,
            0.1]
    dreflect = [0.5,
            0.5,
            0.5]
    sreflect = [0.5,
            0.5,
            0.5]

    color = [0, 0, 0]
    tmp = new_matrix()
    ident( tmp )

    stack = [ [x[:] for x in tmp] ]
    screen = new_screen()
    zbuffer = new_zbuffer()
    tmp = []
    step_3d = 100
    consts = ''
    coords = []
    coords1 = []
    symbols['.white'] = ['constants',
                         {'red': [0.2, 0.5, 0.5],
                          'green': [0.2, 0.5, 0.5],
                          'blue': [0.2, 0.5, 0.5]}]
    reflect = '.white'

    #print(symbols)
    

    for command in commands:
        args = command['args']
        if command['op'] in ['sphere','torus','box']:
            if command['constants'] == None:
                reflect = '.white'
            else:
                reflect = command['constants']
        if command['op'] == 'push':
            stack.append( [x[:] for x in stack[-1]] )
        elif command['op'] == 'pop':
            stack.pop()
        elif command['op'] == 'move':
            t = make_translate(float(args[0]), float(args[1]), float(args[2]))
            matrix_mult( stack[-1], t )
            stack[-1] = [ x[:] for x in t]
        elif command['op'] == 'rotate':
            theta = float(args[1]) * (math.pi / 180)
            if args[0] == 'x':
                t = make_rotX(theta)
            elif args[0] == 'y':
                t = make_rotY(theta)
            else:
                t = make_rotZ(theta)
            matrix_mult( stack[-1], t )
            stack[-1] = [ x[:] for x in t]
        if command['op'] == 'sphere':
            add_sphere(coords1,
                       float(args[0]), float(args[1]), float(args[2]),
                       float(args[3]), step_3d)
            matrix_mult( stack[-1], coords1 )
            draw_polygons(coords1, screen, zbuffer, view, ambient, light, symbols, reflect)
            coords1 = []
        elif command['op'] == 'torus':
            add_torus(coords1,
                      float(args[0]), float(args[1]), float(args[2]),
                      float(args[3]), float(args[4]), step_3d)
            matrix_mult( stack[-1], coords1 )
            draw_polygons(coords1, screen, zbuffer, view, ambient, light, symbols, reflect)
            coords1 = []
        elif command['op'] == 'box':
            add_box(coords1,
                    float(args[0]), float(args[1]), float(args[2]),
                    float(args[3]), float(args[4]), float(args[5]))
            matrix_mult( stack[-1], coords1 )
            draw_polygons(coords1, screen, zbuffer, view, ambient, light, symbols, reflect)
            coords1 = []
        elif command['op'] == 'circle':
            add_circle(coords,
                       float(args[0]), float(args[1]), float(args[2]),
                       float(args[3]), coords)
            matrix_mult( stack[-1], coords )
            draw_lines(coords, screen, zbuffer, color)
            coords = []
        elif command['op'] == 'hermite' or command['op'] == 'bezier':
            add_curve(coords,
                      float(args[0]), float(args[1]),
                      float(args[2]), float(args[3]),
                      float(args[4]), float(args[5]),
                      float(args[6]), float(args[7]),
                      100, command['op'])
            matrix_mult( stack[-1], coords )
            draw_lines(coords, screen, zbuffer, color)
            coords = []
        elif command['op'] == 'line':
            add_edge( coords,
                      float(args[0]), float(args[1]), float(args[2]),
                      float(args[3]), float(args[4]), float(args[5]) )
            matrix_mult( stack[-1], coords )
            draw_lines(coords, screen, zbuffer, color)
            coords = []
        elif command['op'] == 'scale':
            t = make_scale(float(args[0]), float(args[1]), float(args[2]))
            matrix_mult( stack[-1], t )
            stack[-1] = [ x[:] for x in t]
        elif command['op'] == 'display' or command['op'] == 'save':
            if command['op'] == 'display':
                display(screen)
            else:
                save_extension(screen, args[0])
