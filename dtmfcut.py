"""
Segmentação do sinal DTMF — identifica início e fim de cada tom.
Implementação fornecida pelo professor (não alterar a lógica).
"""

import numpy as np


def dtmfcut(xx: np.ndarray, fs: int):
    """
    DTMFCUT find the DTMF tones within x[n]

    usage:
        nstart, nstop = dtmfcut(xx, fs)

    length of nstart = M = number of tones found
    nstart is the set of STARTING indices
    nstop is the set of ENDING indices
    xx = input signal vector
    fs = sampling frequency
    """
    xx = xx.flatten() / np.max(np.abs(xx))  # normalize
    Lx = len(xx)
    Lz = round(0.01 * fs)
    setpoint = 0.02  # make everything below 2% zero

    # Filtro de média móvel
    xx_filtered = np.convolve(np.abs(xx), np.ones(Lz) / Lz, mode='same')
    xx_diff = np.diff(xx_filtered > setpoint)
    jkl = np.where(xx_diff != 0)[0]

    if len(jkl) == 0:
        return np.array([]), np.array([])

    if xx_filtered[jkl[0] + 1] > setpoint:
        jkl = np.concatenate([[0], jkl])

    if xx_filtered[jkl[-1] + 1] > setpoint:
        jkl = np.concatenate([jkl, [Lx - 1]])

    indx = []
    i = 0
    while i < len(jkl) - 1:
        if jkl[i + 1] > (jkl[i] + 10 * Lz):
            indx.extend([jkl[i], jkl[i + 1]])
        i += 2

    if len(indx) == 0:
        return np.array([]), np.array([])

    nstart = np.array(indx[::2])
    nstop = np.array(indx[1::2])
    return nstart, nstop


if __name__ == "__main__":
    from dtmfdial import dtmfdial

    seq = "123"
    signal = dtmfdial(seq)
    nstart, nstop = dtmfcut(signal, 8000)
    print(f"Sequência: {seq}")
    print(f"Tons encontrados: {len(nstart)}")
    for i in range(len(nstart)):
        print(f"  Tom {i+1}: amostras {nstart[i]} a {nstop[i]}")
