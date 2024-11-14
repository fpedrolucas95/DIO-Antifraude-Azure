# Analisador de Documentos e Detector de Fraudes com Azure AI

Este projeto foi desenvolvido como parte do desafio **Análise Automatizada de Documentos com Azure AI** da DIO, para o **Bootcamp Microsoft Certification Challenge #1 - AI 102**.

## 📝 Descrição do Projeto

Uma ferramenta de análise automatizada que utiliza Azure AI para detectar possíveis fraudes em documentos, validando sua autenticidade através de análise inteligente. Suporta:
- Documentos PDF
- Imagens (JPG, PNG)
- Análise multi-página
- Detecção de múltiplos tipos de fraude

## 🚀 Funcionalidades

- Análise detalhada de documentos
- Detecção de indicadores de fraude
- Extração de informações relevantes:
  - Tipo de documento
  - Data de emissão
  - Número do documento
  - Nome do titular
- Suporte a documentos multi-página
- Interface via linha de comando

## 🛠️ Tecnologias Utilizadas

- Python 3.12
- Azure Document Intelligence
- Bibliotecas Python:
  - azure-ai-documentintelligence
  - PyPDF2
  - Pillow
  - python-dotenv

## ⚙️ Como Configurar

1. Clone o repositório:
```bash
git clone https://github.com/fpedrolucas95/DIO-Antifraude-Azure.git
cd DIO-Antifraude-Azure
```

2. Instale as dependências:
```bash
pip install azure-ai-documentintelligence python-dotenv Pillow PyPDF2
```

3. Configure as variáveis de ambiente:
   - Crie um arquivo `.env` na raiz do projeto
   - Adicione suas credenciais do Azure:
```
AZURE_KEY=sua_chave_aqui
AZURE_ENDPOINT=seu_endpoint_aqui
```

## 📖 Como Usar

### Analisar PDF
```bash
python main.py documento.pdf
```

### Analisar Imagem
```bash
python main.py documento.jpg --formato imagem
```

## 🔍 Indicadores de Fraude Detectados

- Datas inválidas ou inconsistentes
- Números de documento suspeitos
- Formatos de documento inválidos
- Modificações não autorizadas
- Inconsistências no layout

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma issue ou enviar um pull request.

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 🔗 Links Úteis

- [DIO - Digital Innovation One](https://www.dio.me/)
- [Documentação Azure Document Intelligence](https://learn.microsoft.com/pt-br/azure/ai-services/document-intelligence/)
- [Bootcamp Microsoft Azure AI Fundamentals](https://web.dio.me/track/microsoft-azure-ai-fundamentals)
