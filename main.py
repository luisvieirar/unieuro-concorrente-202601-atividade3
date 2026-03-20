import os
import time
import multiprocessing

# Função de processamento detalhada
def processar_arquivo(caminho):
    # Identifica qual processo está trabalhando agora
    pid = os.getpid()
    nome_arquivo = os.path.basename(caminho)
    
    print(f"[Processo {pid}] Iniciando: {nome_arquivo}")
    
    try:
        inicio_arq = time.time()
        with open(caminho, "r", encoding="utf-8") as f:
            conteudo = f.readlines()
        
        total_linhas = len(conteudo)
        total_palavras = 0
        total_caracteres = 0
        contagem = {"erro": 0, "warning": 0, "info": 0}
        
        for linha in conteudo:
            palavras = linha.split()
            total_palavras += len(palavras)
            total_caracteres += len(linha)
            for p in palavras:
                if p.lower() in contagem:
                    contagem[p.lower()] += 1
            
            # Simulação de peso (pode ser reduzida se quiser ir mais rápido)
            for _ in range(1000): pass 
            
        fim_arq = time.time()
        print(f"[Processo {pid}] Finalizado: {nome_arquivo} ({fim_arq - inicio_arq:.2f}s)")
        
        return {"linhas": total_linhas, "palavras": total_palavras, "caracteres": total_caracteres, "contagem": contagem}
    except Exception as e:
        print(f"[Processo {pid}] ERRO em {nome_arquivo}: {e}")
        return None

def consolidar_resultados(resultados):
    resumo = {"linhas": 0, "palavras": 0, "caracteres": 0, "contagem": {"erro": 0, "warning": 0, "info": 0}}
    for r in resultados:
        if r:
            resumo["linhas"] += r["linhas"]
            resumo["palavras"] += r["palavras"]
            resumo["caracteres"] += r["caracteres"]
            for k in resumo["contagem"]:
                resumo["contagem"][k] += r["contagem"][k]
    return resumo

if __name__ == "__main__":
    diretorio_script = os.path.dirname(os.path.abspath(__file__))
    pasta = os.path.join(diretorio_script, "log2")

    if not os.path.exists(pasta):
        print(f"ATENÇÃO: Pasta {pasta} não encontrada! Criando teste...")
        os.makedirs(pasta, exist_ok=True)
        for i in range(10):
            with open(os.path.join(pasta, f"teste_{i}.txt"), "w") as f:
                f.write("erro warning info processo dados\n" * 100)
    
    arquivos = [os.path.join(pasta, f) for f in os.listdir(pasta) if f.endswith('.txt')]
    
    print(f"=== Preparado para processar {len(arquivos)} arquivos ===\n")
    
    # Executando apenas as baterias de teste solicitadas
    for n in [2, 4, 8, 12]:
        print(f"\n" + "="*50)
        print(f"INICIANDO TESTE COM {n} PROCESSOS")
        print("="*50)
        
        inicio = time.time()
        
        # O Pool gerencia os processos trabalhadores
        with multiprocessing.Pool(processes=n) as pool:
            resultados = pool.map(processar_arquivo, arquivos)
        
        fim = time.time()
        resumo = consolidar_resultados(resultados)
        
        print(f"\n>>> RESULTADO FINAL ({n} PROCESSOS) <<<")
        print(f"Tempo Total da Bateria: {fim - inicio:.4f}s")
        print(f"Total de Linhas: {resumo['linhas']}")
        print(f"Resumo Global: {resumo['contagem']}")