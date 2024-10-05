from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import gluUnProject
import glm
import numpy as np

# Propriedades da luz
lightPosition = glm.vec3(5, 8, 5)
lightAmbient = glm.vec3(0.1, 0.1, 0.1)
lightDiffuse = glm.vec3(1.0, 1.0, 1.0)
lightSpecular = glm.vec3(1.0, 1.0, 1.0)
camPos = glm.vec3(6.7, 7, 0.05)

def calcular_iluminacao(ponto, normal, surfaceAmbient, surfaceDiffuse, surfaceSpecular, surfaceShine):
    global camPos, lightPosition, lightAmbient, lightDiffuse, lightSpecular

    # Reflexão ambiente
    ambient = lightAmbient * surfaceAmbient

    # Reflexão difusa
    l = glm.normalize(lightPosition - ponto)  # Direção da luz
    n = glm.normalize(normal)  # Normal do ponto

    # Usar max(0.0, glm.dot(l, n)) para evitar valores negativos que causariam escuridão excessiva
    diff = lightDiffuse * surfaceDiffuse * max(0.0, glm.dot(l, n))

    # Reflexão especular
    v = glm.normalize(camPos - ponto)  # Direção da câmera/ponto de vista
    r = glm.reflect(-l, n)  # Direção da luz refletida

    # Cálculo especular com tratamento correto para ângulo
    spec = lightSpecular * surfaceSpecular * pow(max(glm.dot(v, r), 0.0), surfaceShine)

    # Combinação de todas as componentes
    return ambient + diff + spec


# Função contendo configurações iniciais
def inicializar():
    glClearColor(0.5, 0.5, 0.5, 1)
    glLineWidth(1)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_MULTISAMPLE)

# Função que converte glm.mat4 em list<float>
def mat2list(M):
    return [list(M[i]) for i in range(4)]

def screen_to_world(x, y):
    # Obtendo a matriz de projeção e o modelo da câmera
    modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
    projection = glGetDoublev(GL_PROJECTION_MATRIX)
    viewport = glGetIntegerv(GL_VIEWPORT)

    # Como o OpenGL tem o eixo Y invertido em relação à tela, ajustamos a coordenada Y
    winX = float(x)
    winY = float(viewport[3] - y)  # Inverter o eixo Y do mouse
    winZ = glReadPixels(int(winX), int(winY), 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT)

    # Fazendo a conversão de coordenadas de tela (2D) para o espaço 3D
    pos = gluUnProject(winX, winY, winZ[0][0], modelview, projection, viewport)
    return glm.vec3(pos[0], pos[1], pos[2])  # Retorna como vetor glm

# Definição da projeção
def definir_projecao(aspectRatio, near, far):
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    if aspectRatio > 1:
        glFrustum(-aspectRatio, aspectRatio, -1, 1, near, far)
    else:
        glFrustum(-1, 1, -1/aspectRatio, 1/aspectRatio, near, far)

# Definição da câmera
def definir_camera(camPos):
    glMatrixMode(GL_MODELVIEW)
    matrizCamera = glm.lookAt(camPos.xyz, glm.vec3(0), glm.vec3(0, 1, 0))
    glLoadMatrixf(mat2list(matrizCamera))


def detectar_colisao_jogadores(x_centros, z_centros, bola_pos):
    raio = 0.05
    jogadores = list(zip(x_centros, z_centros))

    for jogador in jogadores:
        dist_x = bola_pos.x - jogador[0]
        dist_z = bola_pos.z - jogador[1]
        distancia = np.sqrt(dist_x**2 + dist_z**2)

        if distancia < 2 * raio:
            return jogador  # Retorna a posição do jogador que colidiu

    return None  # Retorna None se não houve colisão

def verifica_colisao_e_gol(bola_pos, limites_campo):

    colidiu_x = False
    colidiu_z = False
    gol = False
    

    # Verifica colisão com as bordas do campo
    colisao_borda_x = bola_pos.x - 0.05 < limites_campo['x'][0]  or bola_pos.x + 0.05 > limites_campo['x'][1] 
    colisao_borda_z = bola_pos.z - 0.05 < limites_campo['z'][0] + 0.1 or bola_pos.z + 0.05 > limites_campo['z'][1] - 0.1

    # Define o espaço do gol (entre -0.25 e 0.25 no eixo z)
    dentro_area_gol_z = -0.25 <= bola_pos.z <= 0.25

    # Considera colisão nas extremidades laterais (x) do campo, exceto na área do gol
    if colisao_borda_x and not dentro_area_gol_z:
        colidiu_x = True

    # Verifica se a bola está dentro da área do gol e entrou um pouco
    if colisao_borda_x and dentro_area_gol_z and (bola_pos.x - 0.05 < limites_campo['x'][0] - 0.1 or bola_pos.x + 0.05 > limites_campo['x'][1] + 0.1):
        colidiu_x = True
        gol = True

    # Considera colisão nas extremidades superiores/inferiores (z) do campo
    if colisao_borda_z:
        colidiu_z = True
    
    return colidiu_x, colidiu_z, gol



def gol(bola_pos, bola_velocidade, limites_campo):
    _, _, gol = verifica_colisao_e_gol(bola_pos, limites_campo)
    
    if gol:
        bola_pos.x, bola_pos.y, bola_pos.z = 0, 0, 0  # Move a bola para o centro
        bola_velocidade.x, bola_velocidade.y, bola_velocidade.z = 0, 0, 0  # Para a bola
        return True  # Retorna que o gol foi detectado
    return False



# Mover a bola e verificar colisões
def mover_bola(bola_pos, bola_velocidade, limites_campo, jogadores):
    atrito = 0.98 
    limiar_parada = 0.001 
    bola_velocidade *= atrito

    # Se a magnitude da velocidade for menor que o limiar, para a bola
    if glm.length(bola_velocidade) < limiar_parada:
        bola_velocidade = glm.vec3(0, 0, 0)

    # Atualiza a posição da bola
    bola_pos += bola_velocidade

    if verifica_colisao_e_gol(bola_pos, limites_campo)[0] == True:
        bola_velocidade.x *= -1
    elif verifica_colisao_e_gol(bola_pos, limites_campo)[1] == True:
        bola_velocidade.z *= -1

    # Verifica colisão com jogadores
    jogador_colidido = detectar_colisao_jogadores(jogadores[0], jogadores[1], bola_pos)

    if jogador_colidido:
        # Calcula o vetor de colisão
        dist_x = bola_pos.x - jogador_colidido[0]
        dist_z = bola_pos.z - jogador_colidido[1]
        vetor_colisao = glm.vec2(dist_x, dist_z)
        vetor_colisao = glm.normalize(vetor_colisao)

        # Projeta a velocidade da bola no vetor de colisão
        velocidade_bola_2d = glm.vec2(bola_velocidade.x, bola_velocidade.z)
        componente_velocidade = glm.dot(velocidade_bola_2d, vetor_colisao)

        # Rebate a bola
        nova_velocidade = velocidade_bola_2d - 2 * componente_velocidade * vetor_colisao
        bola_velocidade.x = nova_velocidade.x
        bola_velocidade.z = nova_velocidade.y


def calcular_direcao_bola(bola_pos, ponto_final_seta):
    # Calcula a direção normalizada a partir da bola até o ponto final da seta
    direcao = (ponto_final_seta - bola_pos) * -1

    return glm.normalize(direcao)  # Normaliza a direção para obter um vetor unitário

def calcula_velocidade_bola(bola_pos, mouse_pos_atual):
     # Calcular a direção da bola quando o mouse for solto
        ponto_final_seta = calcula_ponto_final_seta(bola_pos, mouse_pos_atual)
        direcao_bola = calcular_direcao_bola(bola_pos, ponto_final_seta)

        # Calcula a distância entre a bola e o ponto final da seta
        distancia_seta = glm.distance(bola_pos, ponto_final_seta)

        # Define a velocidade inicial com base no comprimento da seta
        velocidade_inicial = distancia_seta * 0.2 

        # Define a velocidade da bola baseada na direção e distância
        bola_velocidade = glm.vec3(direcao_bola.x, 0, direcao_bola.z) * velocidade_inicial

        return bola_velocidade


def calcula_ponto_final_seta(bola_pos, mouse_pos_atual):

    # Raio máximo da linha (3 vezes o raio da bola)
    raio = 10 * 0.03  # Ajusta o raio se necessário
    
    ponto_final_seta = glm.vec3(mouse_pos_atual.x, 0.015, mouse_pos_atual.z)  # Mantendo a altura constante

    # Calcular a distância entre a posição da bola e a posição do mouse
    distancia = glm.distance(bola_pos, ponto_final_seta)

    # Verifica se a distância excede o raio
    if distancia > raio:
        # Normaliza a direção do vetor da bola até o ponto final da seta
        direcao = glm.normalize(ponto_final_seta - bola_pos)
        # Define o ponto final da seta na borda da circunferência
        ponto_final_seta = bola_pos + direcao * raio

    return ponto_final_seta




# Função que desenha uma seta
def desenhar_seta(inicio, fim):

    glColor3f(1, 1, 1)  # Define a cor branca para a seta
    glLineWidth(2.0)  # Define a largura da linha

    # Desenha a linha representando a seta
    glBegin(GL_LINES)
    glVertex3f(inicio.x, 0.02, inicio.z)  # Começa no centro da bola
    glVertex3f(fim.x, 0.02, fim.z)  # Termina onde o mouse está
    glEnd()
