# Reorganização de Pastas - Plano de Implementação

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Unificar toda documentação sob `docs/`, eliminar duplicatas, padronizar nomes de pasta em kebab-case.

**Architecture:** Mover todos os arquivos de `doc/` e `benchmark/` para dentro de `docs/` com nomes padronizados. Atualizar referências internas nos READMEs. Remover pastas vazias.

**Tech Stack:** git mv, bash

---

### Task 1: Criar estrutura de diretórios

**Step 1: Criar pastas de destino**

```bash
mkdir -p docs/proposta
mkdir -p docs/cursos/casqueamento-e-ferrageamento
mkdir -p docs/cursos/domador-de-sucesso
mkdir -p docs/cursos/rancho-de-sucesso
mkdir -p docs/cursos/trato-e-manejo
mkdir -p docs/derivados/resumos
mkdir -p docs/derivados/briefings
mkdir -p docs/derivados/marketing-cursos
mkdir -p docs/marketing/brand
mkdir -p docs/marketing/campanhas
mkdir -p docs/marketing/landing-page
mkdir -p docs/marketing/templates
mkdir -p docs/eduzz
mkdir -p docs/ideias
mkdir -p docs/benchmark
```

**Step 2: Commit**

```bash
git add docs/
git commit -m "chore: create new directory structure under docs/"
```

---

### Task 2: Mover proposta central

**Step 1: Mover proposta**

```bash
git mv "docs/plans/2026-01-25-doma-pro-proposta.md" "docs/proposta/doma-pro-proposta.md"
```

**Step 2: Remover duplicata palavras-proibidas**

```bash
git rm "docs/plans/palavras-proibidas.md"
```

**Step 3: Commit**

```bash
git commit -m "chore: move proposta to docs/proposta/ and remove duplicate palavras-proibidas"
```

---

### Task 3: Mover cursos (.srt)

**Step 1: Mover Casqueamento e Ferrageamento**

```bash
git mv "doc/aulas/Casqueamento e Ferrageamento"/*.srt docs/cursos/casqueamento-e-ferrageamento/
```

**Step 2: Mover Domador de Sucesso**

```bash
git mv "doc/aulas/Domador de Sucesso"/*.srt docs/cursos/domador-de-sucesso/
```

**Step 3: Mover Rancho de Sucesso**

```bash
git mv "doc/aulas/Rancho de Sucesso"/*.srt docs/cursos/rancho-de-sucesso/
```

**Step 4: Mover Trato e Manejo**

```bash
git mv "doc/aulas/Trato e Manejo"/*.srt docs/cursos/trato-e-manejo/
```

**Step 5: Commit**

```bash
git add .
git commit -m "chore: move course subtitles to docs/cursos/ with kebab-case names"
```

---

### Task 4: Mover derivados

**Step 1: Mover resumos**

```bash
git mv doc/derivados/resumos/*.md docs/derivados/resumos/
```

**Step 2: Mover briefings**

```bash
git mv doc/derivados/briefings/BRIEFINGS.md docs/derivados/briefings/
```

**Step 3: Mover marketing-cursos (antigo doc/derivados/marketing/)**

```bash
git mv doc/derivados/marketing/*.md docs/derivados/marketing-cursos/
```

**Step 4: Mover README dos derivados**

```bash
git mv doc/derivados/README.md docs/derivados/README.md
```

**Step 5: Commit**

```bash
git add .
git commit -m "chore: move derivados to docs/derivados/"
```

---

### Task 5: Mover marketing

**Step 1: Mover brand**

```bash
git mv doc/marketing/brand/*.md docs/marketing/brand/
```

**Step 2: Mover campanhas**

```bash
git mv doc/marketing/campanhas/ docs/marketing/campanhas-old && \
  cp -r docs/marketing/campanhas-old/* docs/marketing/campanhas/ && \
  git rm -r docs/marketing/campanhas-old
```

Alternativa mais simples — como git mv não sobrescreve diretórios, fazer manualmente:

```bash
# Mover conteúdo de campanhas recursivamente
git mv "doc/marketing/campanhas/2026-02-lancamento-doma-pro/README.md" "docs/marketing/campanhas/2026-02-lancamento-doma-pro/README.md"
git mv "doc/marketing/campanhas/2026-02-lancamento-doma-pro/conteudos/instagram/reels/pre-lancamento-20-posts.md" "docs/marketing/campanhas/2026-02-lancamento-doma-pro/conteudos/instagram/reels/pre-lancamento-20-posts.md"
git mv "doc/marketing/campanhas/2026-02-lancamento-doma-pro/conteudos/whatsapp/live-abertura-carrinho.md" "docs/marketing/campanhas/2026-02-lancamento-doma-pro/conteudos/whatsapp/live-abertura-carrinho.md"
```

**Step 3: Mover landing-page**

```bash
git mv doc/marketing/landing-page/*.md docs/marketing/landing-page/
```

**Step 4: Mover templates**

```bash
git mv doc/marketing/templates/*.md docs/marketing/templates/
```

**Step 5: Mover README do marketing**

```bash
git mv doc/marketing/README.md docs/marketing/README.md
```

**Step 6: Commit**

```bash
git add .
git commit -m "chore: move marketing to docs/marketing/"
```

---

### Task 6: Mover eduzz, ideias, benchmark

**Step 1: Mover eduzz**

```bash
git mv doc/eduzz/*.md docs/eduzz/
```

**Step 2: Mover ideias (antigo ideias-carol)**

```bash
git mv "doc/ideias-carol/Doma Pro (IDÉIAS)_260125_181311.pdf" "docs/ideias/"
git mv "doc/ideias-carol/Doma Pro (Ideias 2)_260125_182459.pdf" "docs/ideias/"
```

**Step 3: Mover benchmark**

```bash
git mv "benchmark/Assinantes Pro – Método Thiago Leal.mhtml" "docs/benchmark/"
```

**Step 4: Commit**

```bash
git add .
git commit -m "chore: move eduzz, ideias, and benchmark to docs/"
```

---

### Task 7: Remover pastas antigas vazias

**Step 1: Remover doc/ e benchmark/**

```bash
# git rm não remove dirs vazios, mas podemos limpar
rm -rf doc/
rm -rf benchmark/
git add -A
```

**Step 2: Commit**

```bash
git commit -m "chore: remove old empty directories (doc/, benchmark/)"
```

---

### Task 8: Atualizar referências internas nos READMEs

**Arquivos que precisam de atualização:**

**File: `docs/derivados/README.md`**

Atualizar de:
```markdown
Conteúdos gerados e documentos de apoio criados a partir de `doc/aulas/**/*.srt`.

- Resumos por curso (com aulas): `doc/derivados/resumos/README.md`
- Briefings (conteúdo): `doc/derivados/briefings/BRIEFINGS.md`
- Briefings de marketing: `doc/derivados/marketing/README.md`
```

Para:
```markdown
Conteúdos gerados e documentos de apoio criados a partir de `docs/cursos/**/*.srt`.

- Resumos por curso (com aulas): `docs/derivados/resumos/README.md`
- Briefings (conteúdo): `docs/derivados/briefings/BRIEFINGS.md`
- Briefings de marketing: `docs/derivados/marketing-cursos/README.md`
```

**File: `docs/derivados/resumos/README.md`**

Atualizar de:
```markdown
Arquivos gerados automaticamente a partir de `doc/aulas/**/*.srt`.

- Resumo completo (todos os cursos): `doc/derivados/resumos/resumo_cursos.md`
- Casqueamento e Ferrageamento: `doc/derivados/resumos/casqueamento_e_ferrageamento.resumo.md`
- Domador de Sucesso: `doc/derivados/resumos/domador_de_sucesso.resumo.md`
- Rancho de Sucesso: `doc/derivados/resumos/rancho_de_sucesso.resumo.md`
- Trato e Manejo: `doc/derivados/resumos/trato_e_manejo.resumo.md`
- Briefings (conteúdo): `doc/derivados/briefings/BRIEFINGS.md`
- Briefings de marketing: `doc/derivados/marketing/README.md`
```

Para:
```markdown
Arquivos gerados automaticamente a partir de `docs/cursos/**/*.srt`.

- Resumo completo (todos os cursos): `docs/derivados/resumos/resumo_cursos.md`
- Casqueamento e Ferrageamento: `docs/derivados/resumos/casqueamento_e_ferrageamento.resumo.md`
- Domador de Sucesso: `docs/derivados/resumos/domador_de_sucesso.resumo.md`
- Rancho de Sucesso: `docs/derivados/resumos/rancho_de_sucesso.resumo.md`
- Trato e Manejo: `docs/derivados/resumos/trato_e_manejo.resumo.md`
- Briefings (conteúdo): `docs/derivados/briefings/BRIEFINGS.md`
- Briefings de marketing: `docs/derivados/marketing-cursos/README.md`
```

**File: `docs/derivados/marketing-cursos/README.md`**

Atualizar de:
```markdown
- Casqueamento e Ferrageamento: `doc/derivados/marketing/casqueamento_e_ferrageamento.marketing.md`
- Domador de Sucesso: `doc/derivados/marketing/domador_de_sucesso.marketing.md`
- Rancho de Sucesso: `doc/derivados/marketing/rancho_de_sucesso.marketing.md`
- Trato e Manejo: `doc/derivados/marketing/trato_e_manejo.marketing.md`

Índice geral: `doc/derivados/README.md`
```

Para:
```markdown
- Casqueamento e Ferrageamento: `docs/derivados/marketing-cursos/casqueamento_e_ferrageamento.marketing.md`
- Domador de Sucesso: `docs/derivados/marketing-cursos/domador_de_sucesso.marketing.md`
- Rancho de Sucesso: `docs/derivados/marketing-cursos/rancho_de_sucesso.marketing.md`
- Trato e Manejo: `docs/derivados/marketing-cursos/trato_e_manejo.marketing.md`

Índice geral: `docs/derivados/README.md`
```

**File: `docs/derivados/briefings/BRIEFINGS.md`**

Atualizar referência de:
```
doc/aulas/**/*.srt
```
Para:
```
docs/cursos/**/*.srt
```

**File: `docs/marketing/README.md`**

Atualizar paths de:
```
doc/marketing/
```
Para:
```
docs/marketing/
```

**Step: Commit**

```bash
git add .
git commit -m "chore: update internal references after folder reorganization"
```

---

### Task 9: Verificação final

**Step 1: Verificar que doc/ e benchmark/ não existem mais**

```bash
ls -la
# Deve mostrar apenas: docs/  .git/
```

**Step 2: Verificar estrutura final**

```bash
find docs/ -type f | sort
```

Deve listar todos os arquivos nas novas localizações.

**Step 3: Verificar que não há links quebrados nos READMEs**

Revisar manualmente os READMEs atualizados na Task 8.
