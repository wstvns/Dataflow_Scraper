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

def substituir_abreviacoes(df):
    legenda = {
        "OD": "Odontologia",
        "AMB": "Ambulatorial"
    }
    
    df.replace(legenda, inplace=True)
    return df

def salvar_csv(dados, nome_csv):
    df = pd.DataFrame(dados)
    df = substituir_abreviacoes(df)
    df.to_csv(nome_csv, index=False, encoding='utf-8')
    print(f"Arquivo salvo: {nome_csv}")

def compactar_csv(nome_csv, nome_zip):
    with zipfile.ZipFile(nome_zip, 'w') as zipf:
        zipf.write(nome_csv, nome_csv)
    print(f"Compactado em: {nome_zip}")

def main():
    pdf_path = "../webScrapping/downloads/Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf"
    nome_csv = "rol_de_Procedimentos.csv"
    nome_zip = "Teste_Stevan.zip"
    
    dados = extrair_tabela(pdf_path)
    salvar_csv(dados, nome_csv)
    compactar_csv(nome_csv, nome_zip)
    
if __name__ == "__main__":
    main()