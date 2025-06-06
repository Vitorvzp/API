
# 🌐 API de Processamento de Dados

Uma API desenvolvida em Python para processamento e análise de dados, com funcionalidades de importação, registro de logs e visualização de resultados.

## 🚀 Funcionalidades

- Importação de dados a partir de arquivos ou fontes externas.
- Registro detalhado de logs para monitoramento de processos.
- Armazenamento e gerenciamento de dados processados.
- Visualização de resultados por meio de templates HTML.

## 🛠️ Tecnologias Utilizadas

- [Python 3.x](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/)
- [Jinja2](https://jinja.palletsprojects.com/)
- Outras bibliotecas listadas em `requirements.txt`

## 📁 Estrutura do Projeto

```
API/
├── Data/               # Diretório para armazenamento de dados brutos
├── Functions/          # Módulos com funções auxiliares
├── Logs/               # Arquivos de log gerados durante o processamento
├── templates/          # Templates HTML para visualização de resultados
├── __pycache__/        # Arquivos de cache do Python
├── import.py           # Script para importação de dados
├── main.py             # Arquivo principal para execução da API
├── message_geo_db.json # Base de dados geográficos em formato JSON
├── requirements.txt    # Dependências do projeto
└── .gitignore          # Arquivos e pastas ignorados pelo Git
```

## ⚙️ Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/Vitorvzp/API.git
   ```

2. Navegue até o diretório do projeto:
   ```bash
   cd API
   ```

3. Crie e ative um ambiente virtual (opcional, mas recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/MacOS
   venv\Scripts\activate   # Windows
   ```

4. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

5. Execute a aplicação:
   ```bash
   python main.py
   ```

## 🔧 Configuração

Antes de executar a aplicação, certifique-se de:

- Configurar as variáveis de ambiente necessárias, se houver.
- Verificar as permissões de leitura/escrita nos diretórios `Data/` e `Logs/`.
- Personalizar os templates HTML conforme as necessidades do projeto.

## 📄 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

---

Para mais informações sobre desenvolvimento de APIs com Flask, consulte a [documentação oficial do Flask](https://flask.palletsprojects.com/).
