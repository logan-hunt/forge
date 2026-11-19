#!/usr/bin/env python3
"""Render a research report or versioned plan as self-contained HTML.

Usage: python3 build.py <research-folder> or python3 build.py <version-folder>/plan.md

Markdown stays the source copy. A line `<!-- include: chart.html -->` in the Markdown source is replaced by that
file from the same folder, for a chart or other markup Markdown cannot express.
"""
import html
from pathlib import Path
import re
import sys

TEMPLATE = Path(__file__).with_name('template.html')
INCLUDE = re.compile(r'<!--\s*include:\s*([\w.-]+\.html)\s*-->')
LIST_ITEM = re.compile(r'(\s*)([-*]|\d+\.)\s+(.*)')
SEPARATOR_CELL = re.compile(r':?-{3,}:?')


def inline(text):
    """Escape the text, then restore code spans, links and emphasis. Code spans and links are set aside so nothing inside them is restyled."""
    spans = []

    def keep(match):
        spans.append(f'<code>{html.escape(match[1])}</code>')
        return f'\x00{len(spans) - 1}\x00'

    def link(target, label):
        spans.append(f'<a href="{html.escape(html.unescape(target))}">{label}</a>')
        return f'\x00{len(spans) - 1}\x00'

    text = html.escape(re.sub(r'`([^`]+)`', keep, text), quote=False)
    text = re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)', lambda m: link(m[2], m[1]), text)
    text = re.sub(r'https?://[^\s<)"\']+[^\s<)"\'.,;:]', lambda m: link(m[0], m[0]), text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'(?<![\w*])\*([^*\s][^*]*?)\*(?![\w*])', r'<em>\1</em>', text)
    while '\x00' in text:
        text = re.sub(r'\x00(\d+)\x00', lambda m: spans[int(m[1])], text)
    return text


def cells(row):
    return [cell.strip() for cell in re.split(r'(?<!\\)\|', row.strip().strip('|'))]


def table(rows):
    header, separator, *body = rows
    numeric = [cell.endswith(':') and not cell.startswith(':') for cell in cells(separator)]

    def line(row, tag):
        marked = zip(cells(row), numeric + [False] * len(cells(row)))
        rendered_cells = []
        for cell, right in marked:
            attribute = ' class="num"' if right else ''
            content = inline(cell.replace('\\|', '|'))
            rendered_cells.append(f'<{tag}{attribute}>{content}</{tag}>')
        return '<tr>' + ''.join(rendered_cells) + '</tr>'

    return ('<div class="scroll"><table><thead>' + line(header, 'th') + '</thead><tbody>'
            + ''.join(line(row, 'td') for row in body) + '</tbody></table></div>')


def listing(items):
    """Items are (indent, ordered, text). A deeper indent nests inside the item before it."""
    base, ordered = items[0][0], items[0][1]
    tag = 'ol' if ordered else 'ul'
    parts, index = [], 0
    while index < len(items):
        _, _, text = items[index]
        end = index + 1
        while end < len(items) and items[end][0] > base:
            end += 1
        nested = listing(items[index + 1:end]) if end > index + 1 else ''
        parts.append(f'<li>{inline(text)}{nested}</li>')
        index = end
    return f'<{tag}>' + ''.join(parts) + f'</{tag}>'


def render(markdown, folder=None):
    lines = markdown.splitlines()
    blocks, index = [], 0
    while index < len(lines):
        line = lines[index]
        stripped = line.strip()
        include = INCLUDE.fullmatch(stripped)

        if not stripped:
            index += 1
        elif include and folder is not None:
            blocks.append((folder / include[1]).read_text().strip())
            index += 1
        elif stripped.startswith('```'):
            end = next((n for n in range(index + 1, len(lines)) if lines[n].strip().startswith('```')), len(lines))
            blocks.append('<pre><code>' + html.escape('\n'.join(lines[index + 1:end])) + '</code></pre>')
            index = end + 1
        elif re.match(r'#{1,4} ', stripped):
            level = len(stripped.split(' ')[0])
            blocks.append(f'<h{level}>{inline(stripped[level + 1:])}</h{level}>')
            index += 1
        elif re.fullmatch(r'(-{3,}|\*{3,})', stripped):
            blocks.append('<hr>')
            index += 1
        elif (stripped.startswith('|') and index + 1 < len(lines)
              and all(SEPARATOR_CELL.fullmatch(cell) for cell in cells(lines[index + 1]))):
            end = index + 2
            while end < len(lines) and lines[end].strip().startswith('|'):
                end += 1
            blocks.append(table(lines[index:end]))
            index = end
        elif LIST_ITEM.match(line):
            items = []
            while index < len(lines) and lines[index].strip():
                item = LIST_ITEM.match(lines[index])
                if item:
                    items.append((len(item[1]), item[2][0].isdigit(), item[3]))
                elif lines[index][0].isspace() and not lines[index].strip().startswith('```'):
                    items[-1] = (*items[-1][:2], items[-1][2] + ' ' + lines[index].strip())
                else:
                    break
                index += 1
            blocks.append(listing(items))
        elif stripped.startswith('>'):
            end = index
            while end < len(lines) and lines[end].strip().startswith('>'):
                end += 1
            quoted = ' '.join(lines[n].strip().lstrip('>').strip() for n in range(index, end))
            blocks.append(f'<blockquote><p>{inline(quoted)}</p></blockquote>')
            index = end
        else:
            end = index
            while end < len(lines) and lines[end].strip() and not re.match(r'(#{1,4} |```|\||>)', lines[end].strip()) \
                    and not LIST_ITEM.match(lines[end]):
                end += 1
            end = max(end, index + 1)
            blocks.append('<p>' + inline(' '.join(part.strip() for part in lines[index:end])) + '</p>')
            index = end
    return '\n'.join(blocks)


def build(path):
    plan = path.is_file() and path.name == 'plan.md'
    source = path if plan else path / 'findings.md'
    folder = source.parent
    markdown = source.read_text()
    title = re.search(r'^# (.+)$', markdown, re.M)
    page = TEMPLATE.read_text().replace('{{title}}', html.escape(title[1] if title else folder.name))
    report = folder / ('plan.html' if plan else 'report.html')
    report.write_text(page.replace('{{content}}', render(markdown, folder)))
    return report


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    path = Path(sys.argv[1]).resolve()
    if not ((path.name == 'plan.md' and path.is_file()) or (path / 'findings.md').is_file()):
        sys.exit(__doc__)
    print(build(path))
