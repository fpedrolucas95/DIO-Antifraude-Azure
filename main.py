import os
from dotenv import load_dotenv
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
import argparse
import sys
from typing import Dict, Any
from PyPDF2 import PdfReader
from PIL import Image
import io

load_dotenv()

class AnalisadorDocumentos:
    def __init__(self):
        self.token = os.getenv("AZURE_KEY")
        if not self.token:
            raise ValueError("AZURE_KEY não encontrada nas variáveis de ambiente")
            
        self.endpoint = os.getenv("AZURE_ENDPOINT")
        if not self.endpoint:
            raise ValueError("AZURE_ENDPOINT não encontrado nas variáveis de ambiente")
            
        self.cliente = DocumentIntelligenceClient(
            endpoint=self.endpoint,
            credential=AzureKeyCredential(self.token)
        )

    def _analisar_documento_com_ai(self, conteudo: bytes, tipo_documento: str) -> Dict[str, Any]:
        try:
            poller = self.cliente.begin_analyze_document(
                "prebuilt-document",
                documento=conteudo
            )
            resultado = poller.result()
            return self._extrair_informacoes(resultado)
        except Exception as e:
            print(f"Erro na análise do documento: {e}")
            sys.exit(1)

    def _extrair_informacoes(self, resultado: Any) -> Dict[str, Any]:
        informacoes = {
            "tipo_documento": "",
            "data_emissao": "",
            "numero_documento": "",
            "nome_titular": "",
            "indicadores_fraude": []
        }
        
        for documento in resultado.documents:
            campos = documento.fields
            
            if "DocumentType" in campos:
                informacoes["tipo_documento"] = campos["DocumentType"].content
            if "IssueDate" in campos:
                informacoes["data_emissao"] = campos["IssueDate"].content
            if "DocumentNumber" in campos:
                informacoes["numero_documento"] = campos["DocumentNumber"].content
            if "Name" in campos:
                informacoes["nome_titular"] = campos["Name"].content
                
            informacoes["indicadores_fraude"] = self._verificar_fraudes(campos)
            
        return informacoes

    def _verificar_fraudes(self, campos: Dict[str, Any]) -> list:
        indicadores = []
        
        regras_validacao = {
            "data_invalida": lambda x: not self._validar_data(x.get("IssueDate", {}).get("content")),
            "numero_suspeito": lambda x: not self._validar_numero_documento(x.get("DocumentNumber", {}).get("content")),
            "formato_invalido": lambda x: not self._validar_formato(x.get("DocumentType", {}).get("content")),
            "conteudo_modificado": lambda x: self._detectar_modificacoes(x)
        }
        
        for regra, validador in regras_validacao.items():
            if validador(campos):
                indicadores.append(regra)
                
        return indicadores

    def analisar_arquivo(self, caminho_arquivo: str) -> Dict[str, Any]:
        try:
            extensao = caminho_arquivo.lower().split(".")[-1]
            
            if extensao == "pdf":
                return self._analisar_pdf(caminho_arquivo)
            elif extensao in ["jpg", "jpeg", "png"]:
                with open(caminho_arquivo, "rb") as arquivo:
                    return self._analisar_imagem(arquivo.read())
            else:
                raise ValueError(f"Formato de arquivo não suportado: {extensao}")
                
        except Exception as e:
            print(f"Erro ao processar arquivo: {e}")
            sys.exit(1)

    def _analisar_pdf(self, caminho_arquivo: str) -> Dict[str, Any]:
        resultados = []
        
        with open(caminho_arquivo, "rb") as arquivo:
            leitor = PdfReader(arquivo)
            
            for pagina in leitor.pages:
                texto = pagina.extract_text()
                resultado = self._analisar_documento_com_ai(
                    texto.encode('utf-8'),
                    "pdf"
                )
                resultados.append(resultado)
            
        return self._consolidar_resultados(resultados)

    def _analisar_imagem(self, conteudo: bytes) -> Dict[str, Any]:
        imagem = Image.open(io.BytesIO(conteudo))
        return self._analisar_documento_com_ai(conteudo, "imagem")

    def _consolidar_resultados(self, resultados: list) -> Dict[str, Any]:
        consolidado = {
            "tipo_documento": "",
            "indicadores_fraude": set(),
            "paginas_analisadas": len(resultados),
            "detalhes_por_pagina": resultados
        }
        
        for resultado in resultados:
            consolidado["indicadores_fraude"].update(resultado["indicadores_fraude"])
            
        consolidado["indicadores_fraude"] = list(consolidado["indicadores_fraude"])
        return consolidado

def main():
    parser = argparse.ArgumentParser(description="Analisador de Documentos e Detector de Fraudes")
    parser.add_argument("arquivo", help="Caminho do arquivo a ser analisado")
    parser.add_argument("--formato", choices=["pdf", "imagem"], 
                       help="Formato do documento (opcional)")
    
    args = parser.parse_args()
    
    try:
        analisador = AnalisadorDocumentos()
        resultado = analisador.analisar_arquivo(args.arquivo)
        
        print("\nResultado da análise:")
        print("-" * 50)
        
        if resultado["indicadores_fraude"]:
            print("\n⚠️  ALERTAS DE FRAUDE DETECTADOS!")
            for indicador in resultado["indicadores_fraude"]:
                print(f"- {indicador}")
        else:
            print("\n✅ Nenhum indicador de fraude detectado")
            
        print("\nDetalhes do documento:")
        print(f"Tipo: {resultado.get('tipo_documento', 'Não identificado')}")
        print(f"Data de Emissão: {resultado.get('data_emissao', 'Não identificada')}")
        print(f"Número: {resultado.get('numero_documento', 'Não identificado')}")
        print(f"Titular: {resultado.get('nome_titular', 'Não identificado')}")
            
    except Exception as e:
        print(f"Erro durante a análise: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()