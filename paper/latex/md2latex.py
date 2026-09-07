#!/usr/bin/env python3
"""Convert this paper's markdown section drafts into a single LaTeX body,
for the USENIX/EVT-WOTE-template submission build (`corla_10.tex`).

Not a general-purpose markdown-to-LaTeX converter -- deliberately narrow,
matching exactly the small set of markdown constructs actually used in
sections/*.md (headers, **bold**, bare *italic*, `code`, footnotes, pipe
tables, and already-inline \\cite{}/\\S LaTeX that the drafts embed
directly). Strips this project's own dev-only markup (HTML comments,
[TODO: ...] blocks) that should never reach the compiled paper. Written
for a one-time page-count mockup; re-run if the section text changes and
you want an updated page count.

Escaping order matters here: raw LaTeX already embedded in the markdown
(\\cite{}, \\S) is protected with placeholder tokens BEFORE the general
special-character escaping pass runs, then restored after -- otherwise
escaping would mangle the very backslashes those commands need. Every
LaTeX command this script itself generates (headers, tables, footnotes,
bold/italic) is produced AFTER escaping, so it's never at risk either.

Usage: python3 md2latex.py ../sections/*.md > body.tex
"""

import re
import sys

PLACEHOLDER_RE = re.compile(
    r"\\cite\{[^}]*\}|\\S\b|\\subsection\{[^}]*\}|\\section\{[^}]*\}"
)


def strip_dev_markup(text: str) -> str:
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    text = re.sub(r"\[TODO\b.*?\]", "", text, flags=re.DOTALL)
    return text


def escape_prose(s: str) -> str:
    for ch, esc in [
        ("%", r"\%"), ("&", r"\&"), ("#", r"\#"), ("_", r"\_"), ("$", r"\$"),
    ]:
        s = s.replace(ch, esc)
    return s


def protect_raw_latex(text: str):
    """Replace pre-existing \\cite{}/\\S commands with placeholders so the
    escaping pass can't touch their backslashes; return (text, restore_map)."""
    restore = {}

    def sub(m):
        key = f"@@LATEXTOKEN{len(restore)}@@"
        restore[key] = m.group(0)
        return key

    return PLACEHOLDER_RE.sub(sub, text), restore


def restore_raw_latex(text: str, restore: dict) -> str:
    for key, val in restore.items():
        text = text.replace(key, val)
    return text


def extract_footnotes(text: str):
    """Pull out [^label]: body definitions, escape their bodies now (while
    they're still isolated plain text), and return (text_without_defs,
    {label: escaped_body})."""
    defs = {}

    def collect(m):
        body = re.sub(r"\s+", " ", m.group("body")).strip()
        defs[m.group("label")] = escape_prose(body)
        return ""

    text = re.sub(
        r"^\[\^(?P<label>[\w-]+)\]:\s*(?P<body>.*?)(?=\n\[\^|\n\n|\Z)",
        collect,
        text,
        flags=re.DOTALL | re.MULTILINE,
    )
    return text, defs


def substitute_footnote_refs(text: str, defs: dict) -> str:
    return re.sub(
        r"\[\^([\w-]+)\]", lambda m: r"\footnote{%s}" % defs.get(m.group(1), ""), text
    )


def convert_tables(text: str) -> str:
    lines = text.split("\n")
    out = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.strip().startswith("|") and i + 1 < len(lines) and re.match(
            r"^\s*\|[\s:|-]+\|\s*$", lines[i + 1]
        ):
            header_cells = [c.strip() for c in line.strip().strip("|").split("|")]
            align_cells = [c.strip() for c in lines[i + 1].strip().strip("|").split("|")]
            col_spec = "".join(
                "r" if a.endswith(":") and not a.startswith(":") else "l" for a in align_cells
            )
            rows = []
            j = i + 2
            while j < len(lines) and lines[j].strip().startswith("|"):
                cells = [c.strip() for c in lines[j].strip().strip("|").split("|")]
                rows.append(cells)
                j += 1
            # A "Table: caption text \label{tab:slug}" line (pandoc's own
            # table-caption convention) directly below the last row, if
            # present, becomes this table's \caption/\label -- consumed
            # here so the outer loop never re-emits it as its own
            # paragraph. \label{} passes through escape_prose/convert_inline
            # untouched (no %&#_$ or */backtick), same as this file's
            # existing \cite{}/\S handling.
            caption = None
            if j < len(lines) and lines[j].strip().startswith("Table:"):
                caption = lines[j].strip()[len("Table:") :].strip()
                j += 1
            # table* spans both columns (standard two-column-float trick).
            # The tabular is resized to \textwidth only when its natural
            # width would otherwise overflow it (\ifdim compares the
            # measured natural \width against \textwidth); a table narrow
            # enough to already fit is left at its natural size, so its
            # font matches the surrounding body text instead of being
            # magnified to fill the full two-column span.
            out.append(r"\begin{table*}[t]\centering")
            out.append(r"\resizebox{\ifdim\width>\textwidth\textwidth\else\width\fi}{!}{%")
            out.append(r"\begin{tabular}{%s}" % col_spec)
            out.append(r"\hline")
            out.append(" & ".join(r"\textbf{%s}" % c for c in header_cells) + r" \\")
            out.append(r"\hline")
            for r in rows:
                out.append(" & ".join(r) + r" \\")
            out.append(r"\hline")
            out.append(r"\end{tabular}}")
            if caption:
                out.append(r"\caption{%s}" % caption)
            out.append(r"\end{table*}")
            i = j
            continue
        out.append(line)
        i += 1
    return "\n".join(out)


def convert_headers(text: str) -> str:
    out = []
    for line in text.split("\n"):
        m2 = re.match(r"^##\s+[\d.]+\s*(.*)$", line)
        m1 = re.match(r"^#\s+[\d.]+\s*(.*)$", line)
        if m2:
            out.append(r"\subsection{%s}" % m2.group(1).strip())
        elif m1:
            out.append(r"\section{%s}" % m1.group(1).strip())
        else:
            out.append(line)
    return "\n".join(out)


def convert_inline(text: str) -> str:
    # Content between backticks was already escaped by the earlier global
    # escape_prose() pass -- don't re-escape it here.
    text = re.sub(r"`([^`]+)`", r"\\texttt{\1}", text)
    # DOTALL: **bold** spans routinely wrap across lines in the source
    # markdown's own paragraph line-wrapping (not across paragraphs --
    # there's always a real "**" close before the next blank line).
    text = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", text, flags=re.DOTALL)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"\\textit{\1}", text)
    return text


def convert_file(path: str) -> str:
    with open(path, encoding="utf-8") as f:
        text = f.read()
    text = strip_dev_markup(text)
    text = convert_headers(text)
    text, footnote_defs = extract_footnotes(text)
    text, restore = protect_raw_latex(text)
    text = escape_prose(text)
    text = restore_raw_latex(text, restore)
    text = substitute_footnote_refs(text, footnote_defs)
    text = convert_inline(text)
    # Tables last: they introduce literal "*" (in \end{table*}) that the
    # italic-matching regex in convert_inline() would otherwise misparse
    # as a markdown *italic* delimiter, corrupting everything up to the
    # next stray "*" downstream.
    text = convert_tables(text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def main():
    parts = [convert_file(p) for p in sys.argv[1:]]
    print("\n\n".join(parts))


if __name__ == "__main__":
    main()
