# 📌 MVP - Sistema de Gerenciamento de Testes

Este documento define as funcionalidades mínimas necessárias para a primeira versão utilizável do sistema, focado em organização, documentação e execução de testes manuais.

---

## 🧪 Funcionalidades do MVP

| Funcionalidade         | Descrição                                                                                                                                           | Prioridade |
|------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------|------------|
| **Planos de Teste**    | CRUD completo (criar, listar, editar, excluir planos). Cada plano pode conter uma ou mais suítes de teste.                                          | Alta       |
| **Suítes de Teste**    | CRUD completo. Deve permitir alocar casos de teste e ser associada a planos e regressivos.                                                          | Alta       |
| **Casos de Teste**     | CRUD completo. Deve ser possível associar a múltiplas suítes. Casos não têm status de execução global.                                              | Alta       |
| **Execução de Suíte**  | Interface para executar os casos de uma suíte. Gera um registro com os resultados (passou, falhou, observação).                                     | Alta       |
| **Histórico de Execuções** | Cada suíte deve manter histórico das execuções, com data e resultados.                                                                       | Média      |
| **Regressivo**         | Entidade que agrupa suítes reutilizadas para execuções recorrentes. Permite execução e histórico.                                                   | Média      |
| **Dashboard**          | Exibir resumo geral (últimas execuções, status por suíte, etc). Pode ser básico no MVP.                                                             | Baixa      |
| **Login de Usuário**   | Login simples com autenticação (mock ou backend leve, apenas para organização de autoria e uso).                                                    | Média      |
| **Documentação**       | Sistema de documentação com duas abas (edição e visualização). Permite criar pastas com regras e associar múltiplos casos de teste.                 | Alta       |

---

## ✅ Observações Técnicas

- A execução acontece **na suíte**, e não no caso de teste individual.
- Casos de teste são **imutáveis** e **reutilizáveis** entre suítes.
- Execuções devem ser armazenadas com data e resultado por caso.
- A documentação permite organização hierárquica de casos de teste com regras específicas por pasta.

---

## 🛠️ Sugestões Futuras (Fora do MVP)

- Integração com APIs de bug tracking (ex: Jira, GitHub Issues).
- Execução automatizada (Cypress, Postman, etc).
- Exportação em PDF/Excel.
- Controle de permissões por usuário.

---

> Desenvolvido por e para QAs. Qualquer melhoria na estrutura é bem-vinda!