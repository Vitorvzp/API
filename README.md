# API · Python / Flask

> **Escopo deste rascunho:** este PR inclui somente código, documentação e testes. As remoções de arquivos privados do índice foram preparadas apenas no commit local e não estão incluídas aqui, para evitar sua exposição no diff. Os arquivos legados continuam rastreados nesta branch remota e no histórico até uma etapa específica.

Protótipo de API com consultas de usuários, funcionários e produtos, importação de arquivos e integração com um bot Discord. O código usa Flask, SQLModel/SQLite, discord.py e dicionários legados de substituição de caracteres.

## Estrutura

- `main.py`: rotas HTTP e inicialização da API e do bot.
- `Functions/database.py`: modelos e conexão SQLite.
- `Functions/bot.py`: integração Discord e registros de acesso.
- `Functions/security.py`: carregamento sob demanda dos dicionários privados.
- `runtime_paths.py`: resolução dos caminhos externos de dados e chaves.
- `import.py`: importação de arquivos CSV locais.
- `tests/`: testes isolados com dados sintéticos.

## Desenvolvimento local

Crie um ambiente virtual e instale `requirements.txt`. Antes de executar `python main.py`, configure as variáveis abaixo no ambiente ou em um `.env` local ignorado pelo Git. A execução corrigida exige caminhos externos explícitos, sem fallback para os arquivos legados.

| Variável | Uso |
| --- | --- |
| `API_DATA_DIR` | Diretório absoluto fora do checkout para SQLite, logs e arquivos de importação. Obrigatório para iniciar. |
| `API_KEY_FILE` | Arquivo absoluto de chave Fernet fora do checkout. Obrigatório para usar os dicionários. |
| `API_CRIPTO_FILE` | Dicionário cifrado de substituição, em arquivo externo. |
| `API_DESCRIPTO_FILE` | Dicionário inverso cifrado, em arquivo externo. |
| `DISCORD_BOT_TOKEN` | Token da integração Discord. |

O banco fica em `API_DATA_DIR/Data/database.db`, os logs em `API_DATA_DIR/Logs/`, os CSVs em `API_DATA_DIR/Imports/` e o estado do bot em `API_DATA_DIR/message_geo_db.json`. Os diretórios necessários são criados sob o caminho configurado; arquivos privados existentes não são copiados nem migrados automaticamente. Caminhos relativos ou dentro deste checkout são recusados. Configuração ausente interrompe a operação correspondente, sem procurar arquivos antigos no repositório.

O processo carrega os dicionários somente na primeira operação e os mantém em memória até reiniciar. Esse mecanismo de substituição é legado e não substitui criptografia adequada de dados ou hashing de senhas.

## Testes sem serviços externos

Com `cryptography` e `sqlmodel` instalados no ambiente virtual:

```sh
python -m unittest discover -s tests -v
```

Os testes usam apenas chaves efêmeras, dicionários inventados e SQLite temporário. Não execute `main.py` ou `import.py` como parte desses testes: eles iniciam serviços ou processam arquivos de dados.

## Estado de segurança

Os padrões de chave, dicionários, SQLite, logs e caches estão cobertos pelo .gitignore. A retirada efetiva das entradas legadas do índice permanece somente no preparo local, fora deste PR. Isso não remove versões anteriores do histórico nem invalida material já exposto. Rotação de chaves, avaliação de dados expostos, migração e eventual limpeza do histórico exigem uma etapa específica; não foram executadas por esta alteração.

As rotas de consulta ainda não têm autenticação na aplicação, retornam campos sensíveis e o bot ainda envia registros ao Discord. A correção de armazenamento local não resolve esses comportamentos. Antes de qualquer uso com dados reais, revise autenticação, minimização e transmissão dos dados em uma mudança separada. Nenhum serviço ou configuração de produção foi alterado.

## Autoria e licença

A autoria e o histórico existentes foram preservados. O checkout atual não contém arquivo `LICENSE`; este README não atribui uma licença ausente.
