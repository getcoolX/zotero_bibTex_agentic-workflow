import sqlite3
from pathlib import Path


class PaperStore:
    def __init__(self, db_path: Path):
        self.db_path = str(db_path)
        self._init_db()

    def _conn(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        with self._conn() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS papers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    authors TEXT,
                    year TEXT,
                    doi TEXT,
                    url TEXT,
                    source TEXT
                )
                """
            )

    def save_papers(self, papers):
        inserted = []
        with self._conn() as conn:
            for paper in papers:
                cur = conn.execute(
                    """
                    INSERT INTO papers (title, authors, year, doi, url, source)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        paper.get("title", "Unknown Title"),
                        ", ".join(paper.get("authors", [])),
                        paper.get("year", ""),
                        paper.get("doi", ""),
                        paper.get("url", ""),
                        paper.get("source", "user_input"),
                    ),
                )
                inserted.append({"id": cur.lastrowid, **paper})
        return inserted

    def list_papers(self):
        with self._conn() as conn:
            rows = conn.execute("SELECT id, title, authors, year, doi, url, source FROM papers ORDER BY id DESC").fetchall()
        return [
            {
                "id": row[0],
                "title": row[1],
                "authors": row[2],
                "year": row[3],
                "doi": row[4],
                "url": row[5],
                "source": row[6],
            }
            for row in rows
        ]

    def get_papers(self, ids):
        if not ids:
            return []
        placeholders = ",".join("?" for _ in ids)
        with self._conn() as conn:
            rows = conn.execute(
                f"SELECT id, title, authors, year, doi, url, source FROM papers WHERE id IN ({placeholders})",
                ids,
            ).fetchall()
        return [
            {
                "id": row[0],
                "title": row[1],
                "authors": row[2].split(", ") if row[2] else [],
                "year": row[3],
                "doi": row[4],
                "url": row[5],
                "source": row[6],
            }
            for row in rows
        ]
