from parser import parser
import sys

if len(sys.argv) < 2:
    print("Uso: python main.py [nome.txt]")
    sys.exit(1)

file = sys.argv[1]

try:
    with open(file, 'r', encoding='utf-8') as arquivo:
        source_code = arquivo.read()

    parser.parse(source_code)

except Exception as e:
    print(f"Erro ao compilar arquivo: {e}")
