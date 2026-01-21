#!/usr/bin/env python3
from __future__ import annotations

import argparse
import math
import re
import unicodedata
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path


def read_text_best_effort(path: Path) -> str:
    raw = path.read_bytes()
    for enc in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def normalize_token(token: str) -> str:
    token = token.strip().lower()
    token = unicodedata.normalize("NFKD", token)
    token = "".join(ch for ch in token if not unicodedata.combining(ch))
    token = re.sub(r"[^a-z0-9]+", "", token)
    return token


def slugify_filename(name: str) -> str:
    n = unicodedata.normalize("NFKD", name)
    n = "".join(ch for ch in n if not unicodedata.combining(ch))
    n = n.lower()
    n = re.sub(r"[^a-z0-9]+", "_", n)
    n = re.sub(r"_+", "_", n).strip("_")
    return n or "curso"


_RAW_PT_STOPWORDS = {
    "a",
    "o",
    "os",
    "as",
    "um",
    "uma",
    "uns",
    "umas",
    "de",
    "da",
    "do",
    "das",
    "dos",
    "em",
    "no",
    "na",
    "nos",
    "nas",
    "para",
    "pra",
    "por",
    "com",
    "sem",
    "sobre",
    "entre",
    "até",
    "e",
    "ou",
    "mas",
    "porque",
    "que",
    "se",
    "não",
    "sim",
    "já",
    "também",
    "muito",
    "mais",
    "menos",
    "bem",
    "só",
    "aqui",
    "ali",
    "lá",
    "hoje",
    "agora",
    "então",
    "assim",
    "como",
    "quando",
    "onde",
    "qual",
    "quais",
    "quem",
    "eu",
    "tu",
    "você",
    "vocês",
    "ele",
    "ela",
    "eles",
    "elas",
    "nós",
    "nos",
    "me",
    "te",
    "seu",
    "sua",
    "seus",
    "suas",
    "meu",
    "minha",
    "meus",
    "minhas",
    "isso",
    "isto",
    "aquilo",
    "este",
    "esta",
    "isto",
    "esse",
    "essa",
    "isso",
    "aqueles",
    "aquelas",
    "aquele",
    "aquela",
    "deste",
    "desta",
    "disso",
    "desse",
    "dessa",
    "dele",
    "dela",
    "deles",
    "delas",
    "ser",
    "estar",
    "ter",
    "tem",
    "têm",
    "vai",
    "vão",
    "vou",
    "fazer",
    "faz",
    "fazendo",
    "fez",
    "dar",
    "dá",
    "diz",
    "disse",
    "gente",
    "pessoal",
    "primos",
    # Fala de aula / muletas comuns em transcrição
    "voces",
    "voce",
    "ta",
    "tá",
    "né",
    "cara",
    "tipo",
    "assim",
    "entao",
    "então",
    "nao",
    "não",
    "aí",
    "ai",
    "aqui",
    "agente",
    "gente",
    "pessoal",
    "olá",
    "ola",
}

PT_STOPWORDS = {normalize_token(w) for w in _RAW_PT_STOPWORDS}


SENT_SPLIT_RE = re.compile(r"(?<=[.!?])\s+|\n{2,}")
TOKEN_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ0-9]+", re.UNICODE)


def split_sentences(text: str) -> list[str]:
    chunks = [c.strip() for c in SENT_SPLIT_RE.split(text) if c.strip()]
    # Further split long newline-only paragraphs
    out: list[str] = []
    for c in chunks:
        for line in c.splitlines():
            line = line.strip()
            if line:
                out.append(line)
    return out


def tokenize(text: str) -> list[str]:
    tokens: list[str] = []
    for m in TOKEN_RE.finditer(text):
        t = normalize_token(m.group(0))
        if not t or t in PT_STOPWORDS:
            continue
        if len(t) <= 2:
            continue
        tokens.append(t)
    return tokens


@dataclass(frozen=True)
class AulaSummary:
    course: str
    title: str
    path: Path
    top_keywords: list[str]
    key_sentences: list[str]


def score_sentences(sentences: list[str], word_weights: dict[str, float]) -> list[tuple[float, str]]:
    scored: list[tuple[float, str]] = []
    for s in sentences:
        toks = tokenize(s)
        if not toks:
            continue
        # Skip very repetitive lines (common in noisy transcripts)
        unique_ratio = len(set(toks)) / max(1, len(toks))
        most_common_count = Counter(toks).most_common(1)[0][1]
        dominance = most_common_count / max(1, len(toks))
        if (unique_ratio < 0.50 and len(toks) >= 8) or dominance >= 0.65:
            continue
        # Prefer mid-length sentences; penalize extremely short/long ones
        length = len(toks)
        length_penalty = 1.0
        if length < 6:
            length_penalty = 0.7
        elif length > 30:
            length_penalty = 0.75
        score = sum(word_weights.get(t, 0.0) for t in toks) / math.sqrt(length)
        scored.append((score * length_penalty, s))
    scored.sort(key=lambda x: x[0], reverse=True)
    return scored


def summarize_file(path: Path, course: str, keyword_limit: int, sentence_limit: int) -> AulaSummary:
    text = read_text_best_effort(path)
    sentences = split_sentences(text)

    words = tokenize(text)
    freqs = Counter(words)

    # Simple weighting: log-scaled term frequency
    weights = {w: math.log1p(c) for w, c in freqs.items()}

    top_keywords = [w for w, _ in freqs.most_common(keyword_limit)]

    ranked = score_sentences(sentences, weights)
    key_sentences: list[str] = []
    seen = set()
    for _, s in ranked:
        s_norm = " ".join(s.split()).lower()
        if s_norm in seen:
            continue
        seen.add(s_norm)
        key_sentences.append(s.strip())
        if len(key_sentences) >= sentence_limit:
            break

    title = path.stem
    return AulaSummary(
        course=course,
        title=title,
        path=path,
        top_keywords=top_keywords,
        key_sentences=key_sentences,
    )


def course_overview(aulas: list[AulaSummary], top_n: int) -> list[str]:
    course_tokens: Counter[str] = Counter()
    for a in aulas:
        course_tokens.update(a.top_keywords)
    return [w for w, _ in course_tokens.most_common(top_n)]


def render_course_md(course: str, aulas: list[AulaSummary], course_keywords: int) -> str:
    lines: list[str] = []
    lines.append(f"# {course}\n")
    ck = course_overview(aulas, course_keywords)
    if ck:
        lines.append("**O curso aborda (palavras-chave):** " + ", ".join(ck) + "\n")

    for a in aulas:
        rel = a.path.as_posix()
        lines.append(f"## {a.title}\n")
        lines.append(f"- Arquivo: `{rel}`")
        if a.top_keywords:
            lines.append("- Palavras-chave: " + ", ".join(a.top_keywords))
        if a.key_sentences:
            lines.append("- Pontos extraídos:")
            for s in a.key_sentences:
                lines.append(f"  - {s}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Gera resumos por curso e por aula a partir dos .srt em doc/aulas."
    )
    parser.add_argument("--root", default="doc/aulas", help="Diretório raiz (default: doc/aulas).")
    parser.add_argument(
        "--out",
        default="doc/derivados/resumos/resumo_cursos.md",
        help="Arquivo de saída Markdown (default: doc/derivados/resumos/resumo_cursos.md).",
    )
    parser.add_argument(
        "--out-dir",
        default="doc/derivados/resumos",
        help="Diretório de saída (um .md por curso) (default: doc/derivados/resumos).",
    )
    parser.add_argument("--keywords", type=int, default=12, help="Palavras-chave por aula.")
    parser.add_argument("--sentences", type=int, default=6, help="Frases-chave por aula.")
    parser.add_argument("--course-keywords", type=int, default=20, help="Palavras-chave por curso.")
    args = parser.parse_args()

    root = Path(args.root)
    out_path = Path(args.out)
    out_dir = Path(args.out_dir)
    if not root.exists():
        raise SystemExit(f"Root não existe: {root}")

    # Collect aulas grouped by course directory
    grouped: dict[str, list[Path]] = defaultdict(list)
    for p in sorted(root.rglob("*.srt")):
        course = p.parent.name
        grouped[course].append(p)

    summaries_by_course: dict[str, list[AulaSummary]] = {}
    for course, paths in sorted(grouped.items()):
        summaries_by_course[course] = [
            summarize_file(p, course, args.keywords, args.sentences) for p in paths
        ]

    out_dir.mkdir(parents=True, exist_ok=True)

    index_lines: list[str] = []
    index_lines.append("# Resumos por curso\n")
    index_lines.append("Arquivos gerados automaticamente a partir de `doc/aulas/**/*.srt`.\n")
    index_lines.append(f"- Resumo completo (todos os cursos): `{out_path.as_posix()}`")

    for course, aulas in summaries_by_course.items():
        filename = f"{slugify_filename(course)}.resumo.md"
        course_path = out_dir / filename
        course_md = render_course_md(course, aulas, args.course_keywords)
        course_path.write_text(course_md, encoding="utf-8", newline="\n")
        index_lines.append(f"- {course}: `{course_path.as_posix()}`")

    index_lines.append(f"- Briefings (conteúdo): `{(out_dir.parent / 'briefings' / 'BRIEFINGS.md').as_posix()}`")
    index_lines.append(f"- Briefings de marketing: `{(out_dir.parent / 'marketing' / 'README.md').as_posix()}`")

    (out_dir / "README.md").write_text("\n".join(index_lines).rstrip() + "\n", encoding="utf-8", newline="\n")

    # Keep the combined output for convenience/backwards-compatibility.
    combined: list[str] = []
    combined.append("# Resumo dos cursos e aulas\n")
    combined.append(
        "Resumo extraído automaticamente dos textos das aulas (`doc/aulas/**/*.srt`). "
        "Use como base para revisão/edição final.\n"
    )
    combined.append(f"Índice por curso: `doc/derivados/resumos/README.md`\n")
    for course, aulas in summaries_by_course.items():
        combined.append(render_course_md(course, aulas, args.course_keywords))

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(combined).rstrip() + "\n", encoding="utf-8", newline="\n")

    print(out_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
