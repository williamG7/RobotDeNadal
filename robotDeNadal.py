from enum import Enum
import random

class Casilla(Enum):
    PARED = "🧱"
    ROBOT = "🤖"
    ROCA = "🪨"
    DINAMITA = "🧨"

class Robot:
  # define el constructor
    def __init__(robot, mapa):
        robot.posX = 0
        robot.posY = 0
        robot.velocidad = 1
        robot.mapa = mapa
        robot.jugando = True
        robot.mapa[robot.posY][robot.posX] = Casilla.ROBOT

    def _mover(robot, cambioPosX, cambioPosY):
        # Calcula nueva posicion
        nuevaPosX = robot.posX + cambioPosX * robot.velocidad
        nuevaPosY = robot.posY + cambioPosY * robot.velocidad

        # Limitar a los bordes
        nuevaPosX = max(0, min(19, nuevaPosX))
        nuevaPosY = max(0, min(19, nuevaPosY))

        # Comprobar rocas Y dinamita
        if robot.mapa[nuevaPosY][nuevaPosX] == Casilla.ROCA:
            print("Hay una roca en el camino")
            return
        if robot.mapa[nuevaPosY][nuevaPosX] == Casilla.DINAMITA:
            print("Dinamita encontrada. Fin del juego.")
            robot.jugando = False # si se encuentra una dinamita se acaba el juego
            return

        # Dejar dinamita en la posicion actual
        robot.mapa[robot.posY][robot.posX] = Casilla.DINAMITA

        # Mover robot
        robot.posX, robot.posY = nuevaPosX, nuevaPosY
        robot.mapa[robot.posY][robot.posX] = Casilla.ROBOT

    # Metodos de movimiento     usa el metodo interno _mover
    def mover_arriba(robot):    robot._mover(0, 1)
    def mover_abajo(robot):     robot._mover(0,-1)
    def mover_derecha(robot):   robot._mover(1, 0)
    def mover_izquierda(robot): robot._mover(-1,0)

    # Metodos de velocidad
    def acelerar(robot):
        if robot.velocidad < 5: robot.velocidad += 1

    def frenar(robot):
        if robot.velocidad > 0: robot.velocidad -= 1

    # Méeodos de informacion
    def posicion(robot):
        print(f"La posición del robot es ({robot.posX}, {robot.posY})")

    def velocidad(robot):
        print(f"La velocidad del robot es de {robot.velocidad} m/s")

    # Metodo para mostrar el plano
    def mostrar(robot):
        for fila in reversed(robot.mapa):  # para que y = 0 quede abajo
            print("".join(c.value for c in fila))

    # Metodo de reinicio
    def reiniciar(robot):
        for y in range(20):
            for x in range(20):
                if robot.mapa[y][x] != Casilla.ROCA:
                    robot.mapa[y][x] = Casilla.PARED
                    robot.posX = robot.posY = 0
                    robot.velocidad = 1
                    robot.mapa[0][0] = Casilla.ROBOT


def crear_mapa():
    mapa = [[Casilla.PARED for _ in range(20)] for _ in range(20)] # Crear un mapa 20x20 lleno inicialmente de paredes
    # Colocar rocas aleatorias
    for _ in range(random.randint(30,70)):
        columna, fila = random.randint(0,19), random.randint(0,19)
        if (columna, fila) != (0,0): # evita que la roca se coloque en la posicion inicial
            mapa[fila][columna] = Casilla.ROCA
    return mapa


def mostrar_instrucciones():
    print("""
=======================================
   🤖 Bienvenido al Robot Wall-E 🤖
=======================================
Comandos disponibles (en MAYUSCULAS):
  ARRIBA     - Mover hacia arriba
  BAJO       - Mover hacia abajo
  DERECHA    - Mover hacia la derecha
  IZQUIERDA  - Mover hacia la izquierda
  ACELERAR   - Aumenta velocidad (max 5 m/s)
  FRENAR     - Reduce velocidad (mín 0 m/s)
  POSICION   - Muestra coordenadas actuales
  VELOCIDAD  - Muestra velocidad actual
  MOSTRAR    - Dibuja el plano 20x20
  REINICIAR  - Vuelve a (0,0) con vel 1 m/s
  END        - Terminar programa

Recuerda:
  • Todos los comandos deben ir en MAYUSCULAS.
  • El plano es de 20x20 casillas.
  • Evita las 🪨 rocas y no pises dos veces una 🧨 dinamita.
""")


# Bucle principal
def main():
    mapa = crear_mapa()
    walle = Robot(mapa)

    # Muestra las instrucciones al iniciar
    mostrar_instrucciones()

    while walle.jugando:
        comando = input("> ").strip().upper()
        if comando == "END":
            walle.jugando = False
        elif comando == "ARRIBA":
            walle.mover_arriba()
        elif comando == "BAJO":
            walle.mover_abajo()
        elif comando == "DERECHA":
            walle.mover_derecha()
        elif comando == "IZQUIERDA":
            walle.mover_izquierda()
        elif comando == "ACELERAR":
            walle.acelerar()
        elif comando == "FRENAR":
            walle.frenar()
        elif comando == "POSICION":
            walle.posicion()
        elif comando == "VELOCIDAD":
            walle.velocidad()
        elif comando == "MOSTRAR":
            walle.mostrar()
        elif comando == "REINICIAR":
            walle.reiniciar()
        else:
            print("🤖 Instrucción no entendida")


        # si esta jugando se muestra las instruccioes y el mapa acutalizado
        if walle.jugando:
          mostrar_instrucciones()
          walle.mostrar()

main()