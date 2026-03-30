"""
Projeto dos 8 filtros passa-faixa (BPF) FIR para detecção DTMF.
"""

import numpy as np
from scipy.signal import freqz
from typing import Union, List


def dtmfdesign(
    fb: Union[List[float], np.ndarray],
    L: int,
    fs: int,
) -> np.ndarray:
    """
    Projeta filtros BPF FIR baseados em cosseno escalado.

    Parâmetros
    ----------
    fb : lista de frequências centrais (Hz).
    L  : comprimento de cada filtro FIR.
    fs : frequência de amostragem (Hz).

    Retorna
    -------
    np.ndarray de shape (L, len(fb)) — cada coluna é um filtro BPF.
    """
    fb = np.asarray(fb, dtype=float)
    n = np.arange(L)
    hh = np.zeros((L, len(fb)))

    for i, f_center in enumerate(fb):
        # Resposta ao impulso não-escalada
        h_raw = np.cos(2 * np.pi * f_center * n / fs)
        # Resposta em frequência para encontrar o pico
        _, H = freqz(h_raw, worN=4096)
        peak = np.max(np.abs(H))
        # Fator de escala para ganho máximo = 1.0
        beta = 1.0 / peak
        hh[:, i] = beta * h_raw

    return hh


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    center_freqs = [697, 770, 852, 941, 1209, 1336, 1477, 1633]
    L = 40
    fs = 8000

    hh = dtmfdesign(center_freqs, L, fs)
    print(f"Matriz de filtros: {hh.shape}")

    # Plotar resposta em frequência dos 8 filtros
    plt.figure(figsize=(10, 5))
    for i, fc in enumerate(center_freqs):
        w, H = freqz(hh[:, i], worN=4096)
        freq_hz = w * fs / (2 * np.pi)
        plt.plot(freq_hz, np.abs(H), label=f"{fc} Hz")

    for fc in center_freqs:
        plt.axvline(fc, color='gray', linestyle='--', alpha=0.4)

    plt.title("Resposta em Frequência dos 8 Filtros BPF — DTMF")
    plt.xlabel("Frequência (Hz)")
    plt.ylabel("|H(f)|")
    plt.legend()
    plt.grid(True)
    plt.xlim(0, fs / 2)
    plt.tight_layout()
    plt.savefig("dtmfdesign_filtros.png", dpi=100)
    plt.show()
    print("Gráfico salvo: dtmfdesign_filtros.png")
