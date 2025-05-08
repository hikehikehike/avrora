from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtCore import Qt
from OpenGL.GL import *
from OpenGL.GLU import *
from weather_app.utils.obj_loader import load_obj
import os

model_path = os.path.join(os.path.dirname(__file__), "../models/model.obj")
model_path = os.path.abspath(model_path)


class ModelWidget(QOpenGLWidget):
    def __init__(self):
        super().__init__()
        self.vertices, self.texcoords, self.normals, self.faces = load_obj(model_path)
        self.zoom = -5.0
        self.rot_x = 0
        self.rot_y = 0
        self.last_pos = None
        self.model_color = (1.0, 0.8, 0.6)

    def initializeGL(self):

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)

        glLightfv(GL_LIGHT0, GL_POSITION, (1, 1, 1, 0))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1))
        glLightfv(GL_LIGHT0, GL_SPECULAR, (1, 1, 1, 1))

        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

        glEnable(GL_NORMALIZE)
        glClearColor(0.2, 0.2, 0.3, 1.0)

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect = w / h if h else 1
        gluPerspective(45, aspect, 1, 100)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        glTranslatef(0.0, 0.0, self.zoom)
        glRotatef(self.rot_x, 1, 0, 0)
        glRotatef(self.rot_y, 0, 1, 0)

        glColor3f(*self.model_color)

        glBegin(GL_TRIANGLES)
        for face in self.faces:
            if len(face) == 3:
                for v_idx, vt_idx, vn_idx in face:
                    if vn_idx is not None:
                        glNormal3fv(self.normals[vn_idx])
                    if vt_idx is not None:
                        glTexCoord2fv(self.texcoords[vt_idx])
                    glVertex3fv(self.vertices[v_idx])
        glEnd()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.last_pos = event.position()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton and self.last_pos is not None:
            dx = event.position().x() - self.last_pos.x()
            dy = event.position().y() - self.last_pos.y()

            sensitivity = 0.5
            self.rot_x += dy * sensitivity
            self.rot_y += dx * sensitivity

            self.last_pos = event.position()
            self.update()

    def wheelEvent(self, event):
        delta = event.angleDelta().y() / 120
        self.zoom += delta * 0.3
        self.update()

    def reset_view(self):
        self.rot_x = 0
        self.rot_y = 0
        self.zoom = -5.0
        self.update()

    def load_new_model(self, path):
        self.vertices, self.texcoords, self.normals, self.faces = load_obj(path)
        self.update()
