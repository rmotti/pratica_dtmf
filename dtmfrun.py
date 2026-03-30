"""
Decodificador DTMF completo — identifica a sequência de teclas a partir do sinal.
"""

import numpy as np
from dtmfdesign import dtmfdesign
from dtmfcut import dtmfcut
from dtmfscore import dtmfscore


# Frequências centrais DTMF
CENTER_FREQS = [697, 770, 852, 941, 1209, 1336, 1477, 1633]

# Mapa de teclas DTMF: [linha][coluna]
DTMF_KEYS = [
    ['1', '2', '3', 'A'],
    ['4', '5', '6', 'B'],
    ['7', '8', '9', 'C'],
    ['*', '0', '#', 'D'],
]


def dtmfrun(xx: np.ndarray, L: int, fs: int) -> str:
    """
    Decodifica um sinal DTMF completo em uma sequência de teclas.

    Parâmetros
    ----------
    xx : sinal DTMF completo (múltiplas teclas).
    L  : comprimento dos filtros BPF.
    fs : frequência de amostragem (Hz).

    Retorna
    -------
    str com as teclas decodificadas.
    """
    # Projetar os 8 filtros BPF
    hh = dtmfdesign(CENTER_FREQS, L, fs)

    # Segmentar o sinal em tons individuais
    nstart, nstop = dtmfcut(xx, fs)

    keys = ""
    for kk in range(len(nstart)):
        # Extrair segmento do tom
        x_seg = xx[nstart[kk]:nstop[kk]]

        # Pontuar contra cada filtro
        scores = np.zeros(8, dtype=int)
        for i in range(8):
            scores[i] = dtmfscore(x_seg, hh[:, i])

        # Identificar linha e coluna detectadas
        row_hits = np.where(scores[0:4] == 1)[0]
        col_hits = np.where(scores[4:8] == 1)[0]

        if len(row_hits) == 1 and len(col_hits) == 1:
            row_idx = row_hits[0]
            col_idx = col_hits[0]
            keys += DTMF_KEYS[row_idx][col_idx]
        else:
            keys += '?'

    return keys


if __name__ == "__main__":
    from dtmfdial import dtmfdial

    seq = "5551234"
    print(f"Sequência original: {seq}")
    signal = dtmfdial(seq)
    decoded = dtmfrun(signal, L=40, fs=8000)
    print(f"Sequência decodificada: {decoded}")
    print(f"Correto: {seq == decoded}")
