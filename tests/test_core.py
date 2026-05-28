import sys, os, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from core import organize_directory, get_unique_path, CATEGORIES
from pathlib import Path

def run(d, active=None, opts=None):
    if active is None:
        active = {cat: True for cat in CATEGORIES}
    r = organize_directory(str(d), active, opts or {})
    return r["moved"]

def touch(d, *names):
    for n in names:
        (d / n).touch()

def test_basic():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        touch(d, "foto.jpg", "musica.mp3", "relatorio.pdf", "sem.xyz")
        assert run(d) == 3
        assert (d / "Imagens" / "foto.jpg").exists()
        assert (d / "Áudio" / "musica.mp3").exists()
        assert (d / "Documentos" / "relatorio.pdf").exists()
        assert (d / "sem.xyz").exists()
    print("✓ test_basic")

def test_disabled_category():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        touch(d, "foto.jpg", "video.mp4")
        active = {cat: True for cat in CATEGORIES}
        active["Vídeos"] = False
        assert run(d, active) == 1
        assert (d / "video.mp4").exists()
    print("✓ test_disabled_category")

def test_unique_path():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        (d / "arquivo.txt").touch()
        u = get_unique_path(d / "arquivo.txt")
        assert u == d / "arquivo (1).txt"
        u.touch()
        u2 = get_unique_path(d / "arquivo.txt")
        assert u2 == d / "arquivo (2).txt"
    print("✓ test_unique_path")

def test_hidden_ignored():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        touch(d, ".oculto.jpg", "visivel.jpg")
        assert run(d, opts={"ignore_hidden": True}) == 1
        assert (d / ".oculto.jpg").exists()
    print("✓ test_hidden_ignored")

def test_dry_run():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        touch(d, "foto.jpg", "doc.pdf")
        assert run(d, opts={"dry_run": True}) == 2
        # Files must still be in original location
        assert (d / "foto.jpg").exists()
        assert (d / "doc.pdf").exists()
    print("✓ test_dry_run")

if __name__ == "__main__":
    test_basic()
    test_disabled_category()
    test_unique_path()
    test_hidden_ignored()
    test_dry_run()
    print("\nTodos os testes passaram!")
