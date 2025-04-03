import pdfplumber
import pandas as pd
import zipfile

def extrair_tabela(pdf_path):
    dados = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for pagina in pdf.pages:
            tabelas = pagina.extract_tables()
            for tabela in tabelas:
                for linha in tabela:
                    dados.append(linha)
    
    return dados

def salvar_csv(dados, nome_csv):
    df = pd.DataFrame(dados)
    df.to_csv(nome_csv, index=False, encoding='utf-8')
    print(f"Arquivo salvo: {nome_csv}")

def compactar_csv(nome_csv, nome_zip):
    with zipfile.ZipFile(nome_zip, 'w') as zipf:
        zipf.write(nome_csv, nome_csv)
    print(f"Compactado em: {nome_zip}")

def main():
    pdf_path = "webScrapping/downloads/Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf" #precisa ser o caminho correto do arquivo PDF
    # pdf_path = "downloads/Anexo_II.pdf" # tenho que arrumar uma maneira de pegar o nome do arquivo para não usar o nome fixo
    nome_csv = "Rol_de_Procedimentos.csv"
    nome_zip = "anexos.zip"
    
    dados = extrair_tabela(pdf_path)
    salvar_csv(dados, nome_csv)
    compactar_csv(nome_csv, nome_zip)
    
if __name__ == "__main__":
    main()
