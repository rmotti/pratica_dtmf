"""
Função de pontuação — detecta se um segmento DTMF contém a frequência de um filtro.
"""

import numpy as np

# Limiar de detecção
THRESHOLD = 0.59


def dtmfscore(xx: np.ndarray, hh: np.ndarray) -> int:
    """
    Verifica se o segmento xx contém a frequência do filtro hh.

    Parâmetros
    ----------
    xx : segmento do sinal DTMF (um tom isolado).
    hh : resposta ao impulso de um filtro BPF (vetor 1D).

    Retorna
    -------
    1 se a frequência é detectada, 0 caso contrário.
    """
    # Normalizar para que cada senoide tenha amplitude ~1.0
    xx = xx * (2.0 / np.max(np.abs(xx)))
    # Filtragem por convolução
    y = np.convolve(xx, hh, mode='same')
    # Amplitude máxima da saída
    score_val = np.max(np.abs(y))
    return 1 if score_val >= THRESHOLD else 0


if __name__ == "__main__":
    from dtmfdial import dtmfdial
    from dtmfdesign import dtmfdesign

    fs = 8000
    # Gerar um tom da tecla '5' (770 Hz + 1336 Hz)
    signal = dtmfdial("5", fs=fs, silence_duration=0.0)

    center_freqs = [697, 770, 852, 941, 1209, 1336, 1477, 1633]
    hh = dtmfdesign(center_freqs, L=40, fs=fs)

    print("Pontuação do tom '5' contra cada filtro:")
    for i, fc in enumerate(center_freqs):
        s = dtmfscore(signal, hh[:, i])
        print(f"  {fc} Hz: {s}")
