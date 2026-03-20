# Relatório de Avaliação de Logs Paralelo

**Disciplina:** Programação Paralela e Distribuída  
**Aluno(s):** Luís Henrique  
**Turma:** 5° semestre  
**Professor:** Rafael Marconi  
**Data:** 13/03/2026

---

# 1. Descrição do Problema

O programa resolve o problema de processamento de grandes volumes de arquivos de log operacionais. O objetivo é extrair métricas de desempenho e contagem de palavras-chave específicas em um cenário onde o processamento sequencial (serial) consome um tempo proibitivo para a operação em tempo real.

* **Objetivo:** Reduzir o tempo de análise de logs utilizando o modelo **Produtor-Consumidor** com processos paralelos.
* **Volume de dados:** 1.000 arquivos de texto (pasta `log2`), contendo 10.000 linhas cada, totalizando **10.000.000 de linhas**.
* **Algoritmo:** Utilizou-se um **Pool de Processos** (`multiprocessing.Pool`) onde os arquivos são distribuídos em uma fila global e consumidos pelos núcleos disponíveis.
* **Complexidade:** A complexidade é $O(n)$, onde $n$ é o volume total de dados, uma vez que cada linha é lida e processada uma única vez.

---

# 2. Ambiente Experimental (Configuração do Laboratório)

Conforme solicitado, o ambiente reflete as máquinas de alto desempenho utilizadas no laboratório da instituição:

| Item | Descrição |
| :--- | :--- |
| **Processador** | Intel(R) Core(TM) i7-12700 (12ª Geração) |
| **Número de núcleos** | 12 núcleos físicos / 20 núcleos lógicos |
| **Memória RAM** | 16 GB DDR4 3200MHz |
| **Sistema Operacional** | Windows 10 Pro / Ubuntu 22.04 LTS |
| **Linguagem utilizada** | Python 3.13 |
| **Biblioteca de paralelização** | `multiprocessing` |
| **Compilador / Versão** | Python 3.13.0 |

---

# 3. Metodologia de Testes

Os testes foram conduzidos comparando a execução serial de referência contra execuções paralelas.
* **Configurações:** 1 (Serial), 2, 4, 8 e 12 processos.
* **Carga de Trabalho:** Foi mantida a carga de simulação de processamento pesado (loop interno) para garantir que o uso de CPU fosse o fator limitante (CPU-bound), permitindo observar o ganho real de cada núcleo adicional.

---

# 4. Resultados Experimentais

| Nº de Processos | Tempo de Execução (s) |
| :--- | :--- |
| 1 (Serial) | 115.9621 |
| 2 | 57.6676 |
| 4 | 29.2327 |
| 8 | 20.5816 |
| 12 | 17.8815 |

---

# 5. Tabela de Speedup e Eficiência

| Processos | Tempo (s) | Speedup | Eficiência |
| :--- | :--- | :--- | :--- |
| 1 | 115.9621 | 1.00 | 100% |
| 2 | 57.6676 | 2.01 | 100.5% |
| 4 | 29.2327 | 3.96 | 99.0% |
| 8 | 20.5816 | 5.63 | 70.3% |
| 12 | 17.8815 | 6.48 | 54.0% |

---

# 6. Análise dos Resultados

* **O speedup obtido foi próximo do ideal?** Sim. Até 4 processos, o speedup foi quase perfeito ($3.96 \approx 4.0$), indicando que o algoritmo escala linearmente com os núcleos físicos.
* **A aplicação apresentou escalabilidade?** Sim. A redução de tempo foi constante. O tempo caiu de quase 2 minutos para apenas 17 segundos.
* **Em qual ponto a eficiência começou a cair?** A eficiência apresentou queda a partir de 8 processos. Isso ocorre porque, embora a máquina tenha muitos núcleos, a disputa por acesso ao disco (I/O) e o gerenciamento de muitos processos pelo Sistema Operacional criam um gargalo.
* **O número de processos ultrapassa o número de núcleos físicos?** No ambiente do laboratório (i7-12700), temos 12 núcleos. Ao testar com 12 processos, atingimos o limite dos núcleos físicos, onde o ganho de desempenho começa a estabilizar.
* **Houve overhead de paralelização?** Sim. É visível na queda de eficiência de 100% para 54% quando usamos 12 processos; o custo de criar e sincronizar tantos processos passa a pesar no tempo total.

---

# 7. Conclusão

O experimento validou que a arquitetura multicore do laboratório é extremamente subutilizada em modos seriais. A implementação paralela reduziu o tempo de execução em **85%**. O uso da biblioteca `multiprocessing` foi essencial para contornar o GIL do Python e aproveitar o hardware moderno, sendo a configuração de **8 processos** a mais equilibrada para este volume de arquivos, oferecendo rapidez sem saturar excessivamente o barramento de memória da máquina.

---
 
