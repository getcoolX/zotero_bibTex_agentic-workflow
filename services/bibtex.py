def _safe_key(paper):
    title = paper.get("title", "paper").split()
    head = "".join(ch for ch in (title[0] if title else "paper") if ch.isalnum()).lower()
    year = paper.get("year") or "n.d."
    return f"{head}{year}"


def export_acm_bibtex(papers):
    entries = []
    for paper in papers:
        authors = " and ".join(paper.get("authors", [])) or "Unknown"
        doi = paper.get("doi", "")
        url = paper.get("url", "")
        year = paper.get("year", "")
        entries.append(
            "\n".join(
                [
                    f"@article{{{_safe_key(paper)},",
                    f"  author = {{{authors}}},",
                    f"  title = {{{paper.get('title', 'Untitled')}}},",
                    f"  year = {{{year}}},",
                    f"  doi = {{{doi}}}," if doi else "",
                    f"  url = {{{url}}}," if url else "",
                    "}"
                ]
            ).replace("\n\n", "\n")
        )
    return "\n\n".join(entries)
