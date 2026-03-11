import re

DOI_PATTERN = re.compile(r"10\.\d{4,9}/[-._;()/:A-Z0-9]+", re.IGNORECASE)
URL_PATTERN = re.compile(r"https?://\S+", re.IGNORECASE)


def extract_papers(text: str):
    papers = []
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    for line in lines:
        doi = ""
        url = ""
        doi_match = DOI_PATTERN.search(line)
        url_match = URL_PATTERN.search(line)
        if doi_match:
            doi = doi_match.group(0)
        if url_match:
            url = url_match.group(0)
        title = line
        for token in [doi, url]:
            if token:
                title = title.replace(token, "").strip(" -,:;")
        papers.append(
            {
                "title": title or "Untitled Paper",
                "authors": [],
                "year": "",
                "doi": doi,
                "url": url,
                "source": "bulk_input",
            }
        )
    return papers
