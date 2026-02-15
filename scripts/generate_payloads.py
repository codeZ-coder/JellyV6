
import gzip
import os

def generate_bomb(filename, target_size_mb=100):
    """
    Gera uma "GZIP Bomb" segura para defesa ativa.
    
    O arquivo gerado será pequeno em disco (KB), mas conterá
    instruções para descompactar 'target_size_mb' (100MB) de zeros.
    """
    # Cria diretório se não existir
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # Cria um chunk de 1MB de zeros
    chunk = b'\0' * (1024 * 1024)
    
    print(f"--- FÁBRICA DE PORINAS (GZIP BOMB) ---")
    print(f"Alvo: {target_size_mb} MB descompactados.")
    print(f"Gerando '{filename}'...")

    with gzip.open(filename, 'wb') as f:
        # Escreve o chunk N vezes
        for _ in range(target_size_mb):
            f.write(chunk)
            
    # Estatísticas
    compressed_size = os.path.getsize(filename)
    uncompressed_size = target_size_mb * 1024 * 1024
    ratio = uncompressed_size / compressed_size
    
    print("-" * 30)
    print(f"✅ Bomba Criada com Sucesso!")
    print(f"Nome do Arquivo: {filename}")
    print(f"Tamanho Real (Disco): {compressed_size / 1024:.2f} KB")
    print(f"Potencial de Explosão: {target_size_mb} MB")
    print(f"Taxa de Compressão: {ratio:.1f}x")
    print("-" * 30)

if __name__ == "__main__":
    # Gera payload de 100MB para defesa padrão
    generate_bomb("assets/toxin.gz", target_size_mb=100)
