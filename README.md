# Test TPM

Um sistema simples para gerenciamento de planos de teste desenvolvido com Streamlit e SQLite.

## Funcionalidades

- Criação e gerenciamento de planos de teste
- Organização de suítes de teste
- Documentação de casos de teste
- Acompanhamento de testes regressivos
- Interface amigável e intuitiva

## Requisitos

- Python 3.8+
- Streamlit
- SQLite3 (já incluído no Python)

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/test-tpm.git
cd test-tpm
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Executando

Para iniciar o sistema, execute:

```bash
streamlit run app.py
```

O sistema estará disponível em `http://localhost:8501`

## Estrutura do Projeto

```
test-tpm/
├── app.py                 # Arquivo principal
├── requirements.txt       # Dependências
├── database/             # Banco de dados SQLite
└── src/
    ├── pages/           # Páginas da aplicação
    ├── components/      # Componentes reutilizáveis
    └── database/        # Código de acesso ao banco
```

## Contribuindo

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes. 