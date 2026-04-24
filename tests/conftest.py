import sys
import os

# Pega o caminho absoluto da pasta pai (onde estão os códigos)
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Adiciona ao início do caminho de busca do Python
sys.path.insert(0, root_dir)