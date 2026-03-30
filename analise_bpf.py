"""
Análise teórica do filtro passa-faixa FIR com ω_c = 0.2π e L = 51.
Gera gráficos de magnitude, fase e largura de banda.
"""

import numpy as np
from scipy.signal import freqz
import matplotlib.pyplot as plt


def analise_bpf(fs: int = 8000):
    """Executa a análise completa do filtro BPF teórico."""

    L = 51
    omega_c = 0.2 * np.pi
    n = np.arange(L)

    # --- Item (a): Projeto do filtro e resposta em frequência ---
    h_raw = np.cos(omega_c * n)
    w, H_raw = freqz(h_raw, worN=4096)
    peak = np.max(np.abs(H_raw))
    beta = 1.0 / peak
    h = beta * h_raw

    # Recalcular resposta em frequência do filtro escalado
    w, H = freqz(h, worN=4096)
    mag = np.abs(H)
    phase = np.angle(H)

    print(f"Fator de escala β = {beta:.6f}")
    print(f"Ganho máximo após escala: {np.max(mag):.6f}")

    # Gráfico: magnitude e fase
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7))

    ax1.plot(w, mag, 'b-', linewidth=1.5)
    ax1.axvline(omega_c, color='r', linestyle='--', label=f'ω_c = 0.2π')
    ax1.set_title('Magnitude |H(e^{jω})|')
    ax1.set_xlabel('Frequência (rad/amostra)')
    ax1.set_ylabel('|H(e^{jω})|')
    ax1.legend()
    ax1.grid(True)
    ax1.set_xlim(0, np.pi)

    ax2.plot(w, phase, 'b-', linewidth=1.5)
    ax2.axvline(omega_c, color='r', linestyle='--', label=f'ω_c = 0.2π')
    ax2.set_title('Fase ∠H(e^{jω})')
    ax2.set_xlabel('Frequência (rad/amostra)')
    ax2.set_ylabel('Fase (rad)')
    ax2.legend()
    ax2.grid(True)
    ax2.set_xlim(0, np.pi)

    plt.tight_layout()
    plt.savefig("analise_bpf_magnitude_fase.png", dpi=150)
    plt.show()
    print("Gráfico salvo: analise_bpf_magnitude_fase.png")

    # --- Item (b): Largura de banda (-3 dB) ---
    indices_bw = np.where(mag >= 0.707)[0]
    if len(indices_bw) > 0:
        bw = w[indices_bw[-1]] - w[indices_bw[0]]
        print(f"\nLargura de banda (-3 dB): {bw:.4f} rad/amostra")
    else:
        bw = 0
        print("\nNão foi possível determinar a largura de banda.")

    fig2, ax = plt.subplots(figsize=(10, 5))
    ax.plot(w, mag, 'b-', linewidth=1.5, label='|H(e^{jω})|')
    ax.axhline(0.707, color='g', linestyle='--', linewidth=1, label='0.707 (-3 dB)')
    ax.axvline(omega_c, color='r', linestyle='--', alpha=0.6, label=f'ω_c = 0.2π')
    if len(indices_bw) > 0:
        ax.axvspan(w[indices_bw[0]], w[indices_bw[-1]], alpha=0.2, color='orange',
                   label=f'Banda passante (BW = {bw:.4f} rad/am)')
    ax.set_title('Largura de Banda do Filtro BPF')
    ax.set_xlabel('Frequência (rad/amostra)')
    ax.set_ylabel('|H(e^{jω})|')
    ax.legend()
    ax.grid(True)
    ax.set_xlim(0, np.pi)
    plt.tight_layout()
    plt.savefig("analise_bpf_bandwidth.png", dpi=150)
    plt.show()
    print("Gráfico salvo: analise_bpf_bandwidth.png")

    # --- Item (c): Conversão para frequência analógica ---
    f_center = omega_c * fs / (2 * np.pi)
    f_bw = bw * fs / (2 * np.pi)
    f_low = f_center - f_bw / 2
    f_high = f_center + f_bw / 2

    print(f"\n--- Conversão para frequência analógica (fs = {fs} Hz) ---")
    print(f"Frequência central: {f_center:.1f} Hz")
    print(f"Largura de banda: {f_bw:.1f} Hz")
    print(f"Faixa de passagem: {f_low:.1f} Hz a {f_high:.1f} Hz")


if __name__ == "__main__":
    analise_bpf()
