# API de Livros – Documentação

## Descrição Geral do Projeto

O projeto consiste em uma **API para gerenciamento e busca de livros**, com foco em **busca híbrida** (textual e semântica) e **interações de conversação**. Ele foi desenvolvido como parte de um estudo de caso para avaliar técnicas de **Processamento de Linguagem Natural (NLP)** e **busca vetorial**, combinando tecnologias como PostgreSQL com pgvector, Redis e Langchain. Além disso, inclui um **Jupyter Notebook** para análise exploratória de similaridade entre documentos e prototipagem de chatbot.

### Funcionalidades Principais

- Cadastro e consulta de livros com resumos detalhados.
- Busca híbrida que combina:
  - Busca textual tradicional (full-text)
  - Busca semântica por embeddings
- Conversação contextualizada sobre os livros cadastrados baseado nos seus resumos, utilizando histórico temporário de mensagens com Redis.
- Prototipagem de chatbot para programação em Python e análise de similaridade de documentos usando LangChain, OpenAI e FAISS.

---

# Executando o Projeto

1. Entre na pasta `api`:

```bash
cd api
```

Crie um arquivo .env com as credenciais solicitadas:

```bash
# POSTGRES
POSTGRES_USER=root
POSTGRES_PASSWORD=root
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=hybrid_search

# REDIS
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# AI'S CREDENTIAL
AI_SERVICE_KEY=
```

Execute o projeto:

```bash
docker compose up --build name
```

Após iniciar, a documentação da API pode ser acessada pelo Swagger:

```bash
http://localhost:8000/docs
```

# Endpoints da API
1. Cadastro de Livros – POST /livros

Cria um novo livro no sistema.

URL:

```bash
POST http://localhost:8000/v1/livros
```

Exemplo de payload 1:

```bash
{
  "autor": "Machado de Assis",
  "titulo": "Dom Casmurro",
  "resumo": "Um clássico da literatura brasileira que explora ciúmes, dúvida e traição.",
  "data_publicacao": "2025-10-16"
}
```

Exemplo de payload 2:

```bash
{
  "autor": "J.K. Rowling",
  "titulo": "Harry Potter e a Pedra Filosofal",
  "resumo": "O primeiro livro da série Harry Potter, onde o jovem bruxo descobre seus poderes e entra para Hogwarts.",
  "data_publicacao": "1997-06-26"
}
```


Exemplo de payload 3:

```bash
{
  "autor": "George Orwell",
  "titulo": "1984",
  "resumo": "Uma distopia clássica que explora totalitarismo, vigilância e controle social.",
  "data_publicacao": "1949-06-08"
}
```

Exemplo de uso com curl:

```bash
curl --location 'http://localhost:8000/api/v1/livros' \
--header 'Content-Type: application/json' \
--header 'Cookie: session=27c1a64a-e916-4800-94bd-74eb2814c558' \
--data '{
    "autor": "Paulo Coelho",
    "titulo": "O Alquimista",
    "resumo": "A história segue Santiago, um jovem pastor que parte em busca de um tesouro pessoal, atravessando desertos e enfrentando desafios. A obra mistura aventura e filosofia, explorando temas como sonhos, destino, autoconhecimento e a realização do potencial humano.",
    "data_publicacao": "2021-07-15"
}'
```

# Rodando todos os testes

Para executar os testes da aplicação usando pytest, basta rodar o comando:

```bash
pytest -v
```

O parâmetro -v ativa a saída detalhada dos testes.

O pytest irá executar testes unitários (funções/métodos isolados) e testes de integração (endpoints da API usando TestClient).

Tipos de testes incluídos

🔹 Testes unitários

Dependências externas como OpenAI ou Redis são substituídas por mocks usando unittest.mock.patch ou pytest-mock.

Exemplo: testar o método _semantich_search de HybridSearchService com embeddings simuladas.

🔹 Testes de integração

Testam endpoints da API completos, verificando requisições HTTP, validação de payload e resposta.
