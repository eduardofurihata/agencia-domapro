# Design: Reorganização de Pastas e Arquivos

> Data: 2026-03-05

## Contexto

O repositório agencia-domapro contém toda a documentação do projeto Doma Pro (assinatura de formação em doma de André Pedroso). A estrutura atual tem problemas:

1. Duas pastas concorrentes: `doc/` e `docs/`
2. Arquivo duplicado: `palavras-proibidas.md` em `docs/plans/` e `doc/marketing/brand/`
3. Pasta `benchmark/` solta na raiz
4. `doc/derivados/marketing/` conflita com `doc/marketing/`
5. Nomes de pasta com espaço e maiúscula (prejudica uso no terminal)
6. Proposta central enterrada em `docs/plans/`

## Decisões

- **Repo será docs + código futuro** (landing page, automações)
- **Legendas .srt ficam no repo** (são fonte para derivados)
- **Abordagem: reorganização completa por área**

## Estrutura Final

```
agencia-domapro/
├── docs/
│   ├── proposta/
│   │   └── doma-pro-proposta.md
│   ├── cursos/
│   │   ├── casqueamento-e-ferrageamento/
│   │   ├── domador-de-sucesso/
│   │   ├── rancho-de-sucesso/
│   │   └── trato-e-manejo/
│   ├── derivados/
│   │   ├── resumos/
│   │   ├── briefings/
│   │   └── marketing-cursos/
│   ├── marketing/
│   │   ├── brand/
│   │   ├── campanhas/
│   │   ├── landing-page/
│   │   └── templates/
│   ├── eduzz/
│   ├── ideias/
│   ├── benchmark/
│   └── plans/
└── src/                           # (futuro)
```

## Mapeamento de Mudanças

| Origem | Destino | Tipo |
|--------|---------|------|
| `docs/plans/2026-01-25-doma-pro-proposta.md` | `docs/proposta/doma-pro-proposta.md` | Move |
| `doc/aulas/Casqueamento e Ferrageamento/` | `docs/cursos/casqueamento-e-ferrageamento/` | Move + rename |
| `doc/aulas/Domador de Sucesso/` | `docs/cursos/domador-de-sucesso/` | Move + rename |
| `doc/aulas/Rancho de Sucesso/` | `docs/cursos/rancho-de-sucesso/` | Move + rename |
| `doc/aulas/Trato e Manejo/` | `docs/cursos/trato-e-manejo/` | Move + rename |
| `doc/derivados/resumos/` | `docs/derivados/resumos/` | Move |
| `doc/derivados/briefings/` | `docs/derivados/briefings/` | Move |
| `doc/derivados/marketing/` | `docs/derivados/marketing-cursos/` | Move + rename |
| `doc/derivados/README.md` | `docs/derivados/README.md` | Move |
| `doc/marketing/` (toda a pasta) | `docs/marketing/` | Move |
| `doc/eduzz/` | `docs/eduzz/` | Move |
| `doc/ideias-carol/` | `docs/ideias/` | Move + rename |
| `benchmark/` | `docs/benchmark/` | Move |
| `docs/plans/palavras-proibidas.md` | (remover) | Delete (duplicata) |

## Arquivos a Remover

- `docs/plans/palavras-proibidas.md` — duplicata de `doc/marketing/brand/palavras-proibidas.md`

## Atualizações de Referências Internas

Após mover, atualizar paths internos nos READMEs:
- `doc/derivados/README.md` — refs para `doc/aulas/**/*.srt` → `docs/cursos/`
- `doc/marketing/README.md` — paths relativos
- `doc/derivados/marketing/README.md` — se existir refs internas
