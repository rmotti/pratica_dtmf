"""
Análise com Transformada Z para o filtro BPF de 852 Hz.
Calcula zeros, polos, equação de diferenças e diagrama de polos/zeros.
"""

import numpy as np
from scipy.signal import freqz
import matplotlib.pyplot as plt


def analise_tz(fc: float = 852, L: int = 40, fs: int = 8000):
    """Executa a análise completa via Transformada Z do filtro BPF de 852 Hz."""

    n = np.arange(L)

    # Gerar o filtro escalado
    h_raw = np.cos(2 * np.pi * fc * n / fs)
    _, H = freqz(h_raw, worN=4096)
    peak = np.max(np.abs(H))
    beta = 1.0 / peak
    h = beta * h_raw

    # --- Coeficientes ---
    b = h  # numerador
    a = np.array([1.0])  # denominador (FIR puro)

    print(f"=== Análise Transformada Z — BPF {fc} Hz ===\n")
    print(f"Fator de escala β = {beta:.6f}")
    print(f"Comprimento do filtro L = {L}")
    print(f"\nCoeficientes do numerador b[n] (primeiros 10):")
    for i in range(min(10, L)):
        print(f"  b[{i}] = {b[i]:.6f}")
    if L > 10:
        print(f"  ... ({L} coeficientes no total)")
    print(f"\nCoeficientes do denominador: a = {a}")

    # --- Equação de diferenças ---
    print(f"\n--- Equação de Diferenças ---")
    print(f"H(z) = Y(z)/X(z) = Σ h[n] z^(-n), para n = 0 até {L-1}")
    print(f"y[n] = h[0]*x[n] + h[1]*x[n-1] + ... + h[{L-1}]*x[n-{L-1}]")
    terms = []
    for i in range(min(5, L)):
        terms.append(f"{b[i]:.4f}*x[n-{i}]")
    eq_str = " + ".join(terms) + " + ..."
    print(f"y[n] = {eq_str}")

    # --- Zeros de H(z) ---
    zeros = np.roots(h)
    print(f"\n--- Zeros de H(z) ---")
    print(f"Número de zeros: {len(zeros)}")
    for i, z in enumerate(zeros):
        print(f"  z_{i+1} = {z:.4f}  |z| = {np.abs(z):.4f}")

    # Polos: todos na origem (FIR), multiplicidade L-1
    print(f"\n--- Polos de H(z) ---")
    print(f"Todos os {L-1} polos estão na origem (z = 0)")

    # --- Diagrama de Polos e Zeros ---
    fig, ax = plt.subplots(figsize=(8, 8))

    # Círculo unitário
    theta = np.linspace(0, 2 * np.pi, 300)
    ax.plot(np.cos(theta), np.sin(theta), 'k-', linewidth=0.8, label='Círculo unitário')

    # Zeros
    ax.plot(np.real(zeros), np.imag(zeros), 'bo', markersize=5, alpha=0.7, label=f'Zeros ({len(zeros)})')

    # Polo na origem (multiplicidade L-1)
    ax.plot(0, 0, 'rx', markersize=12, markeredgewidth=2, label=f'Polo (z=0, mult. {L-1})')

    ax.set_title(f"Diagrama de Polos e Zeros — BPF {fc} Hz")
    ax.set_xlabel("Parte Real")
    ax.set_ylabel("Parte Imaginária")
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')
    ax.axhline(0, color='k', linewidth=0.5)
    ax.axvline(0, color='k', linewidth=0.5)

    plt.tight_layout()
    plt.savefig("polos_zeros_852hz.png", dpi=150)
    plt.show()
    print("\nGráfico salvo: polos_zeros_852hz.png")


if __name__ == "__main__":
    analise_tz()
