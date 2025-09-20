# tests/test_parser.py
from scraper.parser import parse_quotes


def test_parse_quotes():
    html = """
    <div class="quote">
        <span class="text">"La vida es bella"</span>
        <span class="author">Autor X</span>
        <div class="tags">
            <a class="tag">inspiración</a>
        </div>
    </div>
    """
    results = parse_quotes(html)
    assert len(results) == 1
    assert results[0]["author"] == "Autor X"
    assert "inspiración" in results[0]["tags"]
