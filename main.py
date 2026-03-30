"""
Prática 3 — Processamento Digital de Sinais (PDS)
Sistema DTMF: Codificação e Decodificação

Script principal que demonstra o pipeline completo.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import freqz

from dtmfdial import dtmfdial
from dtmfrun import dtmfrun
from dtmfdesign import dtmfdesign


def main():
    fs = 8000
    L = 40

    # === 1. Codificação e Decodificação — sequência "5551234" ===
    seq1 = "5551234"
    print(f"{'='*50}")
    print(f"Teste 1: Sequência \"{seq1}\"")
    print(f"{'='*50}")

    signal1 = dtmfdial(seq1, fs=fs)
    decoded1 = dtmfrun(signal1, L=L, fs=fs)

    print(f"  Original:     {seq1}")
    print(f"  Decodificada: {decoded1}")
    print(f"  Correto: {'SIM' if seq1 == decoded1 else 'NÃO'}")

    # Plotar o sinal no domínio do tempo
    t1 = np.arange(len(signal1)) / fs
    fig1, ax1 = plt.subplots(figsize=(12, 3))
    ax1.plot(t1, signal1, linewidth=0.5)
    ax1.set_title(f"Sinal DTMF — \"{seq1}\"")
    ax1.set_xlabel("Tempo (s)")
    ax1.set_ylabel("Amplitude")
    ax1.grid(True)
    plt.tight_layout()
    plt.savefig("main_sinal_5551234.png", dpi=100)
    plt.show()
    print("  Gráfico salvo: main_sinal_5551234.png\n")

    # === 2. Teste com todas as teclas ===
    seq2 = "*#0123456789ABCD"
    print(f"{'='*50}")
    print(f"Teste 2: Sequência \"{seq2}\"")
    print(f"{'='*50}")

    signal2 = dtmfdial(seq2, fs=fs)
    decoded2 = dtmfrun(signal2, L=L, fs=fs)

    print(f"  Original:     {seq2}")
    print(f"  Decodificada: {decoded2}")
    print(f"  Correto: {'SIM' if seq2 == decoded2 else 'NÃO'}")

    # Plotar o sinal completo
    t2 = np.arange(len(signal2)) / fs
    fig2, ax2 = plt.subplots(figsize=(14, 3))
    ax2.plot(t2, signal2, linewidth=0.5)
    ax2.set_title(f"Sinal DTMF — todas as teclas")
    ax2.set_xlabel("Tempo (s)")
    ax2.set_ylabel("Amplitude")
    ax2.grid(True)
    plt.tight_layout()
    plt.savefig("main_sinal_todas_teclas.png", dpi=100)
    plt.show()
    print("  Gráfico salvo: main_sinal_todas_teclas.png\n")

    # === 3. Plotar os 8 filtros BPF ===
    center_freqs = [697, 770, 852, 941, 1209, 1336, 1477, 1633]
    hh = dtmfdesign(center_freqs, L, fs)

    fig3, ax3 = plt.subplots(figsize=(12, 5))
    for i, fc in enumerate(center_freqs):
        w, H = freqz(hh[:, i], worN=4096)
        freq_hz = w * fs / (2 * np.pi)
        ax3.plot(freq_hz, np.abs(H), linewidth=1.5, label=f"{fc} Hz")

    for fc in center_freqs:
        ax3.axvline(fc, color='gray', linestyle='--', alpha=0.4)

    ax3.set_title("Resposta em Frequência dos 8 Filtros BPF — DTMF")
    ax3.set_xlabel("Frequência (Hz)")
    ax3.set_ylabel("|H(f)|")
    ax3.legend(ncol=2)
    ax3.grid(True)
    ax3.set_xlim(0, fs / 2)
    plt.tight_layout()
    plt.savefig("main_filtros_bpf.png", dpi=150)
    plt.show()
    print("Gráfico salvo: main_filtros_bpf.png\n")

    # === 4. Reproduzir áudio (opcional) ===
    try:
        import sounddevice as sd
        print("Reproduzindo áudio da sequência \"5551234\"...")
        sd.play(signal1 / np.max(np.abs(signal1)), samplerate=fs)
        sd.wait()
        print("Reprodução concluída.")
    except ImportError:
        print("sounddevice não disponível — reprodução de áudio ignorada.")

    print(f"\n{'='*50}")
    print("Pipeline DTMF completo executado com sucesso!")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
