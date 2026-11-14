import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('build_report', Path(__file__).resolve().parents[1] / 'tools/research-report/build.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

FINDINGS = '''# Why <things> happen

Date: 2026-11-12. See [the script](analyze.py) and https://example.com/a?b=1&c=2.

## Answer

| Measure | Claude | Codex |
|---|---:|---:|
| Opened `a\\|b` \\| piped | 7 | 169 |

1. **First** item with `code <b>` and *stress*
   continued on the next line.
   - nested bullet
2. Second item

<!-- include: chart.html -->

```python
print("<raw>")
```

> A quoted line.
'''


class ResearchReportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)
        (self.folder / 'findings.md').write_text(FINDINGS)
        (self.folder / 'chart.html').write_text('<div class="hbar">chart</div>\n')

    def test_findings_become_one_self_contained_page(self):
        page = module.build(self.folder).read_text()

        self.assertIn('<title>Why &lt;things&gt; happen</title>', page)
        self.assertIn('<h1>Why &lt;things&gt; happen</h1>', page)
        self.assertIn('<a href="analyze.py">the script</a>', page)
        self.assertIn('<a href="https://example.com/a?b=1&amp;c=2">https://example.com/a?b=1&amp;c=2</a>.', page)
        self.assertIn('<th>Measure</th><th class="num">Claude</th><th class="num">Codex</th>', page)
        self.assertIn('<td>Opened <code>a|b</code> | piped</td><td class="num">7</td><td class="num">169</td>', page)
        self.assertIn('<ol><li><strong>First</strong> item with <code>code &lt;b&gt;</code> and <em>stress</em> continued on the next line.'
                      '<ul><li>nested bullet</li></ul></li><li>Second item</li></ol>', page)
        self.assertIn('<div class="hbar">chart</div>', page)
        self.assertIn('<pre><code>print(&quot;&lt;raw&gt;&quot;)</code></pre>', page)
        self.assertIn('<blockquote><p>A quoted line.</p></blockquote>', page)
        self.assertIn('var(--foreground, #1c1c1c)', page)
        self.assertNotRegex(page, r'<(script|link)[^>]*(src|href)="https?:')

    def render(self, markdown):
        return module.render(markdown)

    def test_a_separator_row_without_outer_pipes_is_still_a_table(self):
        self.assertEqual(self.render('| A | B |\n--- | ---\n| one | two |'),
                         '<div class="scroll"><table><thead><tr><th>A</th><th>B</th></tr></thead>'
                         '<tbody><tr><td>one</td><td>two</td></tr></tbody></table></div>')

    def test_a_list_ends_at_the_next_block(self):
        self.assertEqual(self.render('- Evidence\n## Conclusion\nAll done'),
                         '<ul><li>Evidence</li></ul>\n<h2>Conclusion</h2>\n<p>All done</p>')

    def test_links_are_not_nested_and_their_targets_are_escaped(self):
        self.assertEqual(self.render('[https://example.com](https://example.com)'),
                         '<p><a href="https://example.com">https://example.com</a></p>')
        self.assertEqual(self.render('See https://example.com/?q="x" onmouseover="y".'),
                         '<p>See <a href="https://example.com/?q=">https://example.com/?q=</a>"x" onmouseover="y".</p>')
        self.assertEqual(self.render('[a](https://example.com/?q="x")'),
                         '<p><a href="https://example.com/?q=&quot;x&quot;">a</a></p>')


if __name__ == '__main__':
    unittest.main()
