import statistics

from c4_ruta_optima.ruta_optima import held_karp
from c6_aproximacion.aproximacion_tsp import tsp_2_aproximado
from datos.generador import generar_puntos
from experimentos.utilidades import cronometrar, pendiente_loglog

REPETICIONES = 5
INSTANCIAS = 30
TOLERANCIA = 1e-9



def experimento_razon():
    print("=== Razón de aproximación frente a Held-Karp (30 instancias por n) ===")
    print(f"{'n':>3} {'razón media':>12} {'razón máx.':>11} {'peor caso teórico':>18} "
          f"{'violaciones':>12} {'w(MST)/OPT medio':>17}")
    for n in range(5, 15):
        razones, mst_sobre_opt, violaciones = [], [], 0
        for semilla in range(INSTANCIAS):
            puntos = generar_puntos(n, semilla=semilla)
            optimo, _ = held_karp(puntos)
            longitud, _, peso = tsp_2_aproximado(puntos)
            razones.append(longitud / optimo)
            mst_sobre_opt.append(peso / optimo)
            if not (peso <= optimo + TOLERANCIA <= longitud + TOLERANCIA
                    and longitud <= 2 * peso + TOLERANCIA):
                violaciones += 1
        print(f"{n:>3} {statistics.mean(razones):>12.3f} {max(razones):>11.3f} "
              f"{2.0:>18.1f} {violaciones:>12} {statistics.mean(mst_sobre_opt):>17.3f}")
    print()


def experimento_escala():
    print("=== Tiempo y distancias evaluadas: Θ(n²) (5 repeticiones, mediana) ===")
    print(f"{'n':>6} {'T med (s)':>10} {'sigma':>8} {'dist. cont.':>12} {'n(n-1)/2':>10}")
    tamanos, medianas = [], []
    for n in (250, 500, 1000, 2000, 4000):
        puntos = generar_puntos(n)                 # fuera del tiempo medido
        tiempos = [cronometrar(tsp_2_aproximado, puntos)[0] for _ in range(REPETICIONES)]
        contador = [0]
        tsp_2_aproximado(puntos, contador)
        mediana = statistics.median(tiempos)
        print(f"{n:>6} {mediana:>10.4f} {statistics.pstdev(tiempos):>8.4f} "
              f"{contador[0]:>12} {n * (n - 1) // 2:>10}")
        tamanos.append(n)
        medianas.append(mediana)
    print(f"Pendiente log-log estimada: {pendiente_loglog(tamanos, medianas):.3f} (esperada 2)")


def main():
    experimento_razon()
    experimento_escala()


if __name__ == "__main__":
    main()
