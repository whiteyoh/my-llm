from pathlib import Path


def test_docs_integrity() -> None:
    readme = Path('README.md').read_text(encoding='utf-8')
    teacher = Path('docs/teacher_guide.md').read_text(encoding='utf-8')
    student = Path('docs/student_worksheet.md').read_text(encoding='utf-8')
    architecture = Path('docs/architecture.md').read_text(encoding='utf-8')
    how_llms = Path('docs/how_llms_work.md').read_text(encoding='utf-8')

    assert '## What you should see' in readme
    assert '## Learn Mode' in readme
    assert '(docs/teacher_guide.md)' in readme
    assert '(docs/student_worksheet.md)' in readme
    assert '(docs/architecture.md)' in readme
    assert '(docs/how_llms_work.md)' in readme

    assert '## Suggested classroom pacing' in teacher
    assert '## Troubleshooting' in teacher
    assert '# Challenge 1' in student
    assert '## What happens during training?' in architecture
    assert '## What is next-token prediction?' in how_llms

    assert Path('docs/assets/kairo-logo.svg').exists()
