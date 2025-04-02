import os
import requests
from bs4 import BeautifulSoup
import zipfile

def baixar_pdfs():
    url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
    response = requests.get(url)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, "html.parser")
    pdf_links = []
    
    for link in soup.find_all("a", href=True):
        if "Anexo" in link.text and link["href"].endswith(".pdf"):
            pdf_links.append(link["href"])
    
    if not pdf_links:
        raise ValueError("Não foi encontrado nenhum PDF.")
    
    os.makedirs("downloads", exist_ok=True)
    arquivos_baixados = []
    
    for pdf_link in pdf_links:
        pdf_url = pdf_link if pdf_link.startswith("http") else url + pdf_link
        pdf_nome = os.path.join("downloads", os.path.basename(pdf_url))
        
        with requests.get(pdf_url, stream=True) as r:
            r.raise_for_status()
            with open(pdf_nome, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        
        arquivos_baixados.append(pdf_nome)
        print(f"Baixado: {pdf_nome}")
    
    return arquivos_baixados

def compactar_pdfs(arquivos):
    zip_nome = "anexos.zip"
    with zipfile.ZipFile(zip_nome, "w") as zipf:
        for arquivo in arquivos:
            zipf.write(arquivo, os.path.basename(arquivo))
    print(f"Compactado em: {zip_nome}")

def main():
    arquivos = baixar_pdfs()
    compactar_pdfs(arquivos)

if __name__ == "__main__":
    main()