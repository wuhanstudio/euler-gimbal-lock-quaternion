#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from imgui.integrations.pygame import PygameRenderer

import sys
import imgui
import pygame

from pygame.locals import *
from pygame.constants import *

from OpenGL.GL import *
from OpenGL.GLU import *

from rotate import rotate_x, rotate_y, rotate_vertices

# IMPORT OBJECT LOADER
from objloader import *

# Function to draw the 3D object
def draw_object(vertices, faces):
    glBegin(GL_TRIANGLES)
    for face in faces:
        for vertex in face:
            glVertex3fv(vertices[vertex])
    glEnd()

def main():
    pygame.init()
    size = 800, 600

    pygame.display.set_mode(size, pygame.DOUBLEBUF | pygame.OPENGL | pygame.RESIZABLE)

    glLightfv(GL_LIGHT0, GL_POSITION,  (-40, 200, 100, 0.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)           # most obj files expect to be smooth-shaded

    # LOAD OBJECT AFTER PYGAME INIT
    obj = OBJ("airplane/airplane.obj", swapyz=True)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    width, height = size
    gluPerspective(90.0, width/float(height), 1, 100.0)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_MODELVIEW)

    imgui.create_context()
    impl = PygameRenderer()

    io = imgui.get_io()
    io.display_size = size

    gluPerspective(45, (size[0]/size[1]), 0.1, 50.0)

    glTranslatef(0.0,0.0, -5)

    rx, ry = (0, 0)
    tx, ty = (0, 0)
    zpos = 5
    rotate = move = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 4: zpos = max(1, zpos-1)
                elif event.button == 5: zpos += 1
                elif event.button == 1: rotate = True
                elif event.button == 3: move = True
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1: rotate = False
                elif event.button == 3: move = False
            elif event.type == MOUSEMOTION:
                i, j = event.rel
                if rotate:
                    rx += j
                    ry += i
                if move:
                    tx += i
                    ty -= j
            impl.process_event(event)

        impl.process_inputs()

        imgui.new_frame()

        # Main menu
        if imgui.begin_main_menu_bar():
            if imgui.begin_menu("File", True):

                clicked_quit, selected_quit = imgui.menu_item(
                    "Quit", "Cmd+Q", False, True
                )

                if clicked_quit:
                    sys.exit(0)

                imgui.end_menu()
            imgui.end_main_menu_bar()

        # Test Window
        imgui.show_test_window()

        # Custom Window
        is_expand, _ = imgui.begin("Custom window", True)
        if is_expand:
            imgui.text("Bar")
            imgui.text_colored("Eggs", 0.2, 1.0, 0.0)
        imgui.end()

        # Clear Screen
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        imgui.render()
        glRotatef(1, 3, 1, 1)
        impl.render(imgui.get_draw_data())

        # Cube()

        # RENDER OBJECT
        glTranslate(tx/20., ty/20., - zpos)

        # glRotate(rx, 0, 1, 0)
        # glRotate(ry, 1, 0, 0)

        # Rotate the vertices
        rotation_matrix = rotate_x(rx)
        obj.vertices = rotate_vertices(obj.vertices, rotation_matrix)

        # Rotate the vertices
        rotation_matrix = rotate_y(ry)
        obj.vertices = rotate_vertices(obj.vertices, rotation_matrix)

        rx = ry = 0
        
        obj.update()
        glCallList(obj.gl_list)

        glLoadIdentity()

        pygame.time.wait(10)
        pygame.display.flip()


if __name__ == "__main__":
    main()
