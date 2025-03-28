#!/usr/bin/env python3
import os
import sys

def find_large_files(directory, size_threshold=100 * 1024 * 1024):
    """
    Percorre recursivamente o diretório e imprime os arquivos com tamanho
    maior ou igual ao tamanho especificado (default: 100 MB).
    """
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                file_size = os.path.getsize(file_path)
            except OSError as e:
                print(f"Erro ao acessar {file_path}: {e}")
                continue

            if file_size >= size_threshold:
                print(file_path)

def main():
    if len(sys.argv) < 2:
        print("Uso: python script.py <diretorio>")
        sys.exit(1)
    
    directory = sys.argv[1]
    if not os.path.isdir(directory):
        print(f"Erro: {directory} não é um diretório válido.")
        sys.exit(1)
    
    find_large_files(directory)

if __name__ == '__main__':
    main()
