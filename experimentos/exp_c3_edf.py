import math

from c1_merge_sort.merge_sort import ordenar_pedidos_por_plazo
from c3_voraz.edf import planificar_edf
from datos.generador import generar_pedidos
from experimentos.utilidades import medir, pendiente_loglog

REPETICIONES = 15  # una corrida de C3 con n = 5 000 dura ~0,5 ms: más repeticiones bajan el ruido



def main():
    tamanos = []
    tiempos_edf = []
    tiempos_total = []
    print("EDF sobre lista YA ordenada (solo C3) vs. C1 + C3 desde cero")
    print(f"{'n':>8} {'C3 (s)':>10} {'sigma':>9} {'T/n (us)':>9} "
          f"{'C1+C3 (s)':>10} {'sigma':>9} {'T/(n log n) (us)':>17}")
    n = 5000
    for _ in range(6):  # 6 tamaños, n se duplica
        pedidos = generar_pedidos(n)  # generación fuera del tiempo medido
        ordenados = ordenar_pedidos_por_plazo(pedidos)

        t_edf, s_edf = medir(lambda p: planificar_edf(p, ya_ordenados=True), ordenados,
                             repeticiones=REPETICIONES)
        t_tot, s_tot = medir(planificar_edf, pedidos, repeticiones=REPETICIONES)

        tamanos.append(n)
        tiempos_edf.append(t_edf)
        tiempos_total.append(t_tot)
        print(f"{n:>8} {t_edf:>10.5f} {s_edf:>9.5f} {t_edf / n * 1e6:>9.3f} "
              f"{t_tot:>10.5f} {s_tot:>9.5f} {t_tot / (n * math.log2(n)) * 1e6:>17.4f}")
        n *= 2

    print()
    print(f"Pendiente log-log de C3 solo   : {pendiente_loglog(tamanos, tiempos_edf):.3f} (esperada ~1)")
    print(f"Pendiente log-log de C1 + C3   : {pendiente_loglog(tamanos, tiempos_total):.3f} (esperada ~1.1, n log n)")


if __name__ == "__main__":
    main()
