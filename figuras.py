from functions import *


def calcular_normal_cilindro(xVert, zVert, xCentro, zCentro):
    # Vetor que vai do centro da base ao ponto da superfície (só interessa a projeção no plano XZ
    normal = glm.vec3(xVert - xCentro, 0, zVert - zCentro)
    return glm.normalize(normal)


def desenha_cilindro(altura, raio, xCentro, yCentro, zCentro, num_segments=40):
    # Propriedades do material do cilindro
    surfaceAmbient = glm.vec3(0.2, 0.2, 0.2)
    surfaceDiffuse = glm.vec3(0.8, 0.8, 0.8)
    surfaceSpecular = glm.vec3(1.0, 1.0, 1.0)
    surfaceShine = 32

    # Base superior
    glBegin(GL_TRIANGLE_FAN)
    glVertex3f(xCentro, yCentro + altura / 2, zCentro)  # Centro da base superior
    for i in range(num_segments + 1):
        theta = 2 * np.pi * i / num_segments
        xVert = raio * np.cos(theta) + xCentro
        zVert = raio * np.sin(theta) + zCentro

        # Normal e cor da base superior (normal apontando para cima)
        normal = glm.vec3(0, 1, 0)
        ponto = glm.vec3(xVert, yCentro + altura / 2, zVert)
        cor = calcular_iluminacao(ponto, normal, surfaceAmbient, surfaceDiffuse, surfaceSpecular, surfaceShine)

        # Aplicando cor com base na iluminação (sombreamento Gouraud)
        glColor3f(cor.r, cor.g, cor.b)
        glVertex3f(xVert, yCentro + altura / 2, zVert)
    glEnd()

    # Base inferior
    glBegin(GL_TRIANGLE_FAN)
    glVertex3f(xCentro, yCentro - altura / 2, zCentro)  # Centro da base inferior
    for i in range(num_segments + 1):
        theta = 2 * np.pi * i / num_segments
        xVert = raio * np.cos(theta) + xCentro
        zVert = raio * np.sin(theta) + zCentro

        # Normal e cor da base inferior (normal apontando para baixo)
        normal = glm.vec3(0, -1, 0)
        ponto = glm.vec3(xVert, yCentro - altura / 2, zVert)
        cor = calcular_iluminacao(ponto, normal, surfaceAmbient, surfaceDiffuse, surfaceSpecular, surfaceShine)

        # Aplicando cor com base na iluminação (sombreamento Gouraud)
        glColor3f(cor.r, cor.g, cor.b)
        glVertex3f(xVert, yCentro - altura / 2, zVert)
    glEnd()

    # Superfície lateral
    glBegin(GL_TRIANGLE_STRIP)
    for i in range(num_segments + 1):
        theta = 2 * np.pi * i / num_segments
        xVert = raio * np.cos(theta) + xCentro
        zVert = raio * np.sin(theta) + zCentro

        # Calcular normal para a superfície lateral
        normal = calcular_normal_cilindro(xVert, zVert, xCentro, zCentro)

        # Cálculo das cores em cada vértice para o sombreamento Gouraud
        ponto_superior = glm.vec3(xVert, yCentro + altura / 2, zVert)
        ponto_inferior = glm.vec3(xVert, yCentro - altura / 2, zVert)

        # Cor do vértice superior
        cor_superior = calcular_iluminacao(ponto_superior, normal, surfaceAmbient, surfaceDiffuse, surfaceSpecular, surfaceShine)
        glColor3f(cor_superior.r, cor_superior.g, cor_superior.b)
        glVertex3f(xVert, yCentro + altura / 2, zVert)

        # Cor do vértice inferior
        cor_inferior = calcular_iluminacao(ponto_inferior, normal, surfaceAmbient, surfaceDiffuse, surfaceSpecular, surfaceShine)
        glColor3f(cor_inferior.r, cor_inferior.g, cor_inferior.b)
        glVertex3f(xVert, yCentro - altura / 2, zVert)
    glEnd()




def desenha_circulo2d(xCentro, zCentro, raio):
    glBegin(GL_LINE_LOOP)
    num_segments = 40
    for i in range(num_segments):
        theta = 2 * np.pi * i / num_segments
        xVert = raio * np.cos(theta) + xCentro
        zVert = raio * np.sin(theta) + zCentro
        glVertex3f(xVert, 0, zVert)
    glEnd()


def desenha_meio_circulo2d_direita(xCentro, zCentro, raio):
    glBegin(GL_LINE_LOOP)
    num_segments = 20
    for i in range(num_segments + 1):  
        theta = -np.pi/2 + (np.pi * i / num_segments)  # Varia de -π/2 a π/2
        xVert = raio * np.cos(theta) + xCentro
        zVert = raio * np.sin(theta) + zCentro
        glVertex3f(xVert, 0, zVert)
    glEnd()


def desenha_meio_circulo2d_esquerda(xCentro, zCentro, raio):
    glBegin(GL_LINE_LOOP)
    num_segments = 20
    for i in range(num_segments + 1):  
        theta = np.pi/2 + (np.pi * i / num_segments)  # Varia de π/2 a 3π/2
        xVert = raio * np.cos(theta) + xCentro
        zVert = raio * np.sin(theta) + zCentro
        glVertex3f(xVert, 0, zVert)
    glEnd()


def desenha_campo():
    #desenhando o campo no plano xz
    glPushMatrix()
    glColor3f(0.0,0.5,0.0)
    glBegin(GL_QUADS)
    glVertex3f(-1.5, 0,-1)
    glVertex3f( 1.5, 0,-1)
    glVertex3f( 1.5, 0, 1)
    glVertex3f(-1.5, 0, 1)
    glEnd()

    
    glColor3f(1.0, 1.0, 1.0)  # Cor branca para as linhas


    glLineWidth(3.0)  # Ajuste no tamanho das linhas

    # Linha do meio
    glBegin(GL_LINES)
    glVertex3f(0.0, 0, -1)
    glVertex3f(0.0, 0, 1)
    glEnd()

    # Grande area esquerda
    glBegin(GL_LINE_LOOP)
    glVertex3f(-1.5, 0, -0.4)
    glVertex3f(-1.3, 0, -0.4)
    glVertex3f(-1.3, 0, 0.4)
    glVertex3f(-1.5, 0, 0.4)
    glEnd()

    # Meio circulo area esquerda
    desenha_meio_circulo2d_direita(-1.3, 0, 0.08)

    # Grande area direita
    glBegin(GL_LINE_LOOP)
    glVertex3f(1.5, 0, -0.4)
    glVertex3f(1.3, 0, -0.4)
    glVertex3f(1.3, 0, 0.4)
    glVertex3f(1.5, 0, 0.4)
    glEnd()

    # Meio circulo area direita
    desenha_meio_circulo2d_esquerda(1.3, 0, 0.08)

    # Pequena area esquerda
    glBegin(GL_LINE_LOOP)
    glVertex3f(-1.5, 0, -0.25)
    glVertex3f(-1.4, 0, -0.25)
    glVertex3f(-1.4, 0, 0.25)
    glVertex3f(-1.5, 0, 0.25)
    glEnd()

    # Pequena area direita
    glBegin(GL_LINE_LOOP)
    glVertex3f(1.5, 0, -0.25)
    glVertex3f(1.4, 0, -0.25)
    glVertex3f(1.4, 0, 0.25)
    glVertex3f(1.5, 0, 0.25)
    glEnd()


    # Linha lateral esquerda
    glBegin(GL_LINES)
    glVertex3f(-1.5, 0, -1)
    glVertex3f(-1.5, 0, 1)
    glEnd()

    # Linha lateral direita
    glBegin(GL_LINES)
    glVertex3f(1.5, 0, -1)
    glVertex3f(1.5, 0, 1)
    glEnd()

    # Linha de fundo superior
    glBegin(GL_LINES)
    glVertex3f(-1.5, 0, 1)
    glVertex3f(1.5, 0, 1)
    glEnd()

    # Linha de fundo inferior
    glBegin(GL_LINES)
    glVertex3f(-1.5, 0, -1)
    glVertex3f(1.5, 0, -1)
    glEnd()

    # Círculo central
    desenha_circulo2d(0, 0, 0.2)

    glPopMatrix()

def desenha_cubo(tamanho, xCentro=0.0, yCentro=0.0, zCentro=0.0):

    t = tamanho / 2.0  # Metade do tamanho para calcular os vértices

    # Define a cor amadeirada (marrom claro)
    glColor3f(0.64, 0.32, 0.18)  # Cor de madeira

    glBegin(GL_QUADS)

    # Face frontal
    glVertex3f(xCentro - t, yCentro - t, zCentro + t)  # Inferior esquerdo
    glVertex3f(xCentro + t, yCentro - t, zCentro + t)  # Inferior direito
    glVertex3f(xCentro + t, yCentro + t, zCentro + t)  # Superior direito
    glVertex3f(xCentro - t, yCentro + t, zCentro + t)  # Superior esquerdo

    # Face traseira
    glVertex3f(xCentro - t, yCentro - t, zCentro - t)  # Inferior esquerdo
    glVertex3f(xCentro + t, yCentro - t, zCentro - t)  # Inferior direito
    glVertex3f(xCentro + t, yCentro + t, zCentro - t)  # Superior direito
    glVertex3f(xCentro - t, yCentro + t, zCentro - t)  # Superior esquerdo

    # Face lateral esquerda
    glVertex3f(xCentro - t, yCentro - t, zCentro + t)  # Inferior frente
    glVertex3f(xCentro - t, yCentro - t, zCentro - t)  # Inferior trás
    glVertex3f(xCentro - t, yCentro + t, zCentro - t)  # Superior trás
    glVertex3f(xCentro - t, yCentro + t, zCentro + t)  # Superior frente

    # Face lateral direita
    glVertex3f(xCentro + t, yCentro - t, zCentro + t)  # Inferior frente
    glVertex3f(xCentro + t, yCentro - t, zCentro - t)  # Inferior trás
    glVertex3f(xCentro + t, yCentro + t, zCentro - t)  # Superior trás
    glVertex3f(xCentro + t, yCentro + t, zCentro + t)  # Superior frente

    # Face superior
    glVertex3f(xCentro - t, yCentro + t, zCentro + t)  # Frente esquerda
    glVertex3f(xCentro + t, yCentro + t, zCentro + t)  # Frente direita
    glVertex3f(xCentro + t, yCentro + t, zCentro - t)  # Trás direita
    glVertex3f(xCentro - t, yCentro + t, zCentro - t)  # Trás esquerda

    # Face inferior
    glVertex3f(xCentro - t, yCentro - t, zCentro + t)  # Frente esquerda
    glVertex3f(xCentro + t, yCentro - t, zCentro + t)  # Frente direita
    glVertex3f(xCentro + t, yCentro - t, zCentro - t)  # Trás direita
    glVertex3f(xCentro - t, yCentro - t, zCentro - t)  # Trás esquerda

    glEnd()
   
def desenha_parede_cubos_com_gol(lado_cubo, largura_campo, altura_parede, comprimento_campo, largura_gol, altura_gol, xCentro, yCentro, zCentro):

    num_cubos_horizontal = int(largura_campo // lado_cubo)
    num_cubos_vertical = int(altura_parede // lado_cubo)
    num_cubos_profundo = int(comprimento_campo // lado_cubo)
    
    # Metade da largura do gol para calcular os limites da abertura
    largura_gol_metade = largura_gol / 2
    altura_gol_topo = yCentro + altura_gol

    # Posição das paredes nas extremidades do campo
    pos_z_frontal = zCentro + comprimento_campo / 2
    pos_z_traseira = zCentro - comprimento_campo / 2

    # Paredes frontal e traseira (sólidas, sem abertura)
    for i in range(num_cubos_horizontal):
        for j in range(num_cubos_vertical):
            # Posição X varia ao longo da largura
            x = xCentro - largura_campo / 2 + i * lado_cubo + lado_cubo / 2
            y = yCentro + j * lado_cubo + lado_cubo / 2

            # Parede frontal sólida
            desenha_cubo(lado_cubo, x, y, pos_z_frontal)

            # Parede traseira sólida
            desenha_cubo(lado_cubo, x, y, pos_z_traseira)

    # Paredes laterais (com abertura para o gol)
    for i in range(num_cubos_profundo):
        for j in range(num_cubos_vertical):
            # Posição Z varia ao longo do comprimento
            z = zCentro - comprimento_campo / 2 + i * lado_cubo + lado_cubo / 2
            y = yCentro + j * lado_cubo + lado_cubo / 2

            # Parede lateral esquerda (com abertura para o gol)
            if not (-largura_gol_metade <= (z - zCentro) <= largura_gol_metade and y <= altura_gol_topo):
                desenha_cubo(lado_cubo, xCentro - largura_campo / 2, y, z)

            # Parede lateral direita (com abertura para o gol)
            if not (-largura_gol_metade <= (z - zCentro) <= largura_gol_metade and y <= altura_gol_topo):
                desenha_cubo(lado_cubo, xCentro + largura_campo / 2, y, z)


def desenha_jogadores():
    raio_cilindro = 0.05
    altura_cilindro = 0.12
    yCentro_cilindro = altura_cilindro/2

    # Distribuição dos jogadores
    x_centros = [
        -1.2, -1.2, -1.05, -1.05,  # Defesa Esquerda
        -1.4,                      # Goleiro Esquerdo
        -0.8, -0.65, -0.65,          # Meio Esquerdo
        -0.35, -0.2, -0.2,          # Ataque Esquerdo

        1.2, 1.2, 1.05, 1.05,  # Defesa Direito
        1.4,                      # Goleiro Direito
        0.8, 0.65, 0.65,          # Meio Direito
        0.35, 0.2, 0.2          # Ataque Direito

    ]
    z_centros = [
        0.8, -0.8, 0.3, -0.3,   # Defesa Esquerda
        0,                      # Goleiro Esquerdo
        0, 0.5, -0.5,           # Meio Esquerdo
        0, 0.7, -0.7,            # Ataque Esquerdo

        0.8, -0.8, 0.3, -0.3,   # Defesa Direito
        0,                      # Goleiro Direito
        0, 0.5, -0.5,           # Meio Direito
        0, 0.7, -0.7            # Ataque Direito
    ]
    for xCentro, zCentro in zip(x_centros, z_centros):
        desenha_cilindro(altura_cilindro, raio_cilindro, xCentro, yCentro_cilindro, zCentro)

    return x_centros, z_centros