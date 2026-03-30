"""
Codificador DTMF — gera sinais de tons dual-tone multi-frequency.
"""

import numpy as np
from typing import Optional


# Tabela DTMF: mapeia cada tecla para (frequência_linha, frequência_coluna)
DTMF_FREQS = {
    '1': (697, 1209), '2': (697, 1336), '3': (697, 1477), 'A': (697, 1633),
    '4': (770, 1209), '5': (770, 1336), '6': (770, 1477), 'B': (770, 1633),
    '7': (852, 1209), '8': (852, 1336), '9': (852, 1477), 'C': (852, 1633),
    '*': (941, 1209), '0': (941, 1336), '#': (941, 1477), 'D': (941, 1633),
}


def dtmfdial(
    key_sequence: str,
    fs: int = 8000,
    tone_duration: float = 0.20,
    silence_duration: float = 0.05,
) -> np.ndarray:
    """
    Gera o sinal DTMF para uma sequência de teclas.

    Parâmetros
    ----------
    key_sequence : str
        Sequência de teclas (ex: "5551234").
    fs : int
        Frequência de amostragem em Hz.
    tone_duration : float
        Duração de cada tom em segundos.
    silence_duration : float
        Duração do silêncio entre tons em segundos.

    Retorna
    -------
    np.ndarray
        Sinal DTMF concatenado.
    """
    # Vetores de tempo para tom e silêncio
    t_tone = np.arange(int(fs * tone_duration)) / fs
    silence = np.zeros(int(fs * silence_duration))

    segments = []
    for ch in key_sequence:
        key = ch.upper()
        if key not in DTMF_FREQS:
            print(f"Aviso: tecla inválida '{ch}' — ignorada.")
            continue
        f_row, f_col = DTMF_FREQS[key]
        # Soma das duas senoides (amplitude total ~2.0)
        tone = np.sin(2 * np.pi * f_row * t_tone) + np.sin(2 * np.pi * f_col * t_tone)
        segments.append(tone)
        segments.append(silence)

    if not segments:
        return np.array([])

    return np.concatenate(segments)


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    seq = "5551234"
    print(f"Gerando sinal DTMF para: {seq}")
    signal = dtmfdial(seq)
    print(f"Amostras geradas: {len(signal)}")

    t = np.arange(len(signal)) / 8000
    plt.figure(figsize=(12, 3))
    plt.plot(t, signal)
    plt.title(f"Sinal DTMF — \"{seq}\"")
    plt.xlabel("Tempo (s)")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("dtmfdial_demo.png", dpi=100)
    plt.show()
    print("Gráfico salvo: dtmfdial_demo.png")
