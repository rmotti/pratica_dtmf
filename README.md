# Prática 3 — Sistema DTMF: Codificação e Decodificação

Projeto de Processamento Digital de Sinais (PDS) — CIMATEC.

## Estrutura

| Arquivo | Descrição |
|---------|-----------|
| `dtmfdial.py` | Codificador DTMF — gera sinais a partir de sequências de teclas |
| `dtmfcut.py` | Segmentação do sinal — identifica início/fim de cada tom |
| `dtmfdesign.py` | Projeto dos 8 filtros BPF FIR para detecção |
| `dtmfscore.py` | Função de pontuação — detecta frequência em um segmento |
| `dtmfrun.py` | Decodificador completo — pipeline de detecção DTMF |
| `analise_bpf.py` | Análise teórica de filtro BPF com ω_c = 0.2π, L = 51 |
| `analise_tz.py` | Análise via Transformada Z do filtro de 852 Hz |
| `main.py` | Script principal — demonstra o pipeline completo |

## Parâmetros

- **fs** = 8000 Hz (frequência de amostragem)
- **L** = 40 (comprimento dos filtros BPF)
- **Duração do tom** = 0.20 s
- **Silêncio entre tons** = 0.05 s
- **Limiar de detecção** = 0.59

## Como executar

```bash
pip install -r requirements.txt
python main.py
```

Cada arquivo também pode ser executado individualmente:

```bash
python dtmfdial.py
python dtmfdesign.py
python analise_bpf.py
python analise_tz.py
```
