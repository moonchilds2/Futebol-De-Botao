from figuras import *
from figuras import desenha_parede_cubos_com_gol

# Variáveis globais
FPS = 60
camPos = glm.vec4(6.7, 7, 0.05, 0)  # Posição inicial da câmera

camRotacao = glm.rotate(glm.mat4(1.0), glm.radians(1.0), glm.vec3(0, 1, 0))  # Matriz de rotação para girar a câmera
gira = False  # Variável que determina se a câmera está ou não girando
janelaLargura = 800  # Largura da janela em pixels
janelaAltura = 700  # Altura da janela em pixels
aspectRatio = 1  # Aspect ratio da janela (largura dividida pela altura)


bola_pos = glm.vec3(0, 0, 0)  # Posição inicial da bola
bola_velocidade = glm.vec3(0, 0, 0)  # Velocidade da bola ( vetor de translacao)
limites_campo = {'x': [-1.5, 1.5], 'z': [-1, 1]}  # Limites do campo

mouse_pos_atual = glm.vec3(0, 0.015, 0)  # Posição inicial do mouse ao arrastar (definida ao iniciar o arrasto)
mouse_click_pos = None  # Posição inicial do clique do mouse
mouse_dragging = False  # Indica se o botão do mouse está sendo pressionado




# Função chamada sempre que a janela sofre alteração em seu tamanho
def alteraJanela(largura, altura):
    global janelaLargura, janelaAltura, aspectRatio
    janelaLargura = largura
    janelaAltura = altura
    aspectRatio = largura / altura  # Calculando o aspect ratio da janela
    glViewport(0, 0, largura, altura)  # Reserva a área inteira da janela para desenhar


def teclado(key, x, y):
    global gira, camRotacao
    
    if key == GLUT_KEY_LEFT:
        camRotacao = glm.rotate(glm.mat4(1.0), glm.radians(1.0), glm.vec3(0, -1, 0))
        gira =  not gira # Liga ou desliga a variável gira que realiza a rotação da posição da câmera a cada frame

    elif key == GLUT_KEY_RIGHT:
        camRotacao = glm.rotate(glm.mat4(1.0), glm.radians(1.0), glm.vec3(0, 1, 0))
        gira = not gira


# Função para lidar com clique do mouse
def mouse(button, state, x, y):
    global mouse_click_pos, mouse_dragging, bola_velocidade, bola_pos, mouse_pos_atual

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        # Converte as coordenadas da tela para o mundo
        world_click_pos = screen_to_world(x, y)
        clicou_na_bola = (bola_pos.x - 0.05 <= world_click_pos.x <= bola_pos.x + 0.05) and (bola_pos.z - 0.05 <= world_click_pos.z <= bola_pos.z + 0.05)
        if clicou_na_bola:
            mouse_click_pos = glm.vec2(world_click_pos.x, world_click_pos.z)
            mouse_dragging = True  # Inicia o arraste
        else:
            mouse_dragging = False  # Evita arraste se o clique não for na bola

    elif button == GLUT_LEFT_BUTTON and state == GLUT_UP:
        print("Mouse parou de arrastar")

        if mouse_dragging:
           
           bola_velocidade = calcula_velocidade_bola(bola_pos, mouse_pos_atual)

        mouse_dragging = False  # Para o arraste ao soltar o botão


# Função que acompanha o movimento do mouse
def movimento_mouse(x, y):
    global mouse_dragging, mouse_pos_atual
    
    if mouse_dragging:

        
        # Atualiza a posição atual do mouse
        mouse_pos_atual = screen_to_world(x, y)
        print("Mouse sendo arrastado, posição: ", mouse_pos_atual)
        glutPostRedisplay()  # Solicita redesenho da janela



# Função que altera variáveis de translação, escala e rotação a cada frame e manda redesenhar a tela
def timer(v):
    global camPos

    # Agendando a execução da função timer para daqui a 1000/FPS milissegundos
    glutTimerFunc(int(1000 / FPS), timer, 0)

    if gira:  # Posição da câmera é modificada apenas se o giro estiver habilitado
        camPos = camRotacao * camPos  # Aplicando a matriz de rotação apenas na posição da câmera

    glutPostRedisplay()




# Função usada para redesenhar o conteúdo do frame buffer
def desenha():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    definir_projecao(aspectRatio, 5, 200)
    definir_camera(camPos)

    desenha_campo()
    desenha_parede_cubos_com_gol(
        lado_cubo=0.15,   # Tamanho do cubo
        largura_campo=3.18,   # Largura da caixa
        altura_parede=0.4,    # Altura da caixa
        comprimento_campo=2,  # Profundidade da caixa
        largura_gol=0.54,       # Largura da abertura do gol
        altura_gol=0.2,        # Altura da abertura do gol
        xCentro=0.0,   # Posição X do centro da caixa
        yCentro=0.0,   # Posição Y do centro da caixa (altura)
        zCentro=0.0,    # Posição Z do centro da caixa (profundidade)
    )
    jogadores = desenha_jogadores()

    bola = desenha_cilindro(0.03, 0.05, bola_pos.x, bola_pos.y, bola_pos.z)
    if not gol(bola_pos, bola_velocidade, limites_campo):
        mover_bola(bola_pos, bola_velocidade, limites_campo, jogadores)
    detectar_colisao_jogadores(jogadores[0], jogadores[1], bola_pos)
    

    if mouse_dragging:
        
        ponto_final_seta = calcula_ponto_final_seta(bola_pos, mouse_pos_atual)
        desenhar_seta(bola_pos, ponto_final_seta)


    glutSwapBuffers()



# Corpo principal do código
glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)  # Utilizando Double Buffering
glutInitWindowSize(int(janelaLargura), int(janelaAltura))
glutInitWindowPosition(320, 10)
glutCreateWindow("primeiro fi")
inicializar()
glutDisplayFunc(desenha)
glutReshapeFunc(alteraJanela)
glutKeyboardFunc(teclado)
glutSpecialFunc(teclado)
glutMotionFunc(movimento_mouse)
glutMouseFunc(mouse)
glutTimerFunc(int(1000 / FPS), timer, 0)
glutMainLoop()
