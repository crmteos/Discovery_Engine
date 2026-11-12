#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""BigQuery Agent Search (v5.4.0 / Phase 45) - enterprise search with offline fallback."""

from __future__ import annotations

import argparse
import json
import sys
import sqlite3
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
BRIDGE_DIR = PROJECT_ROOT / "Bridge"
LOCAL_KB = PROJECT_ROOT / "Bridge" / "messages.jsonl"
SQLITE_KB = PROJECT_ROOT / "Bridge" / "offline_kb_index.jsonl"

try:
    from google.cloud import bigquery
    HAS_BQ = True
except ImportError:
    HAS_BQ = False

PROV_NS = "http://www.w3.org/ns/prov#"


def _prov_entity(uri, label, prov=None):
    e = {"@id": uri, "@type": "prov:Entity", "prov:label": label}
    if prov:
        e["prov:wasDerivedFrom"] = prov.get("wasDerivedFrom", "") if prov else ""
    return e


def _search_local_kb(query, limit=10):
    results = []
    if not LOCAL_KB.is_file():
        return results
    try:
        with open(LOCAL_KB, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if query.lower() in json.dumps(rec).lower():
                    preview = str(rec.get("content", "")[:200]).replace(chr(10), " ")
                    results.append({
                        "source": "local_kb",
                        "preview": preview,
                        "prov": _prov_entity(
                            uri=f"local_kb:{rec.get('id', '')}",
                            label=rec.get("title", "local KB"),
                            prov=rec.get("prov")
                        ),
                        "score": 1.0
                    })
    except Exception:
        pass
    results.sort(key=lambda r: r.get("score", 0), reverse=True)
    return results[:limit]


def _search_sqlite(query, limit=10):
    results = []
    if not SQLITE_KB.is_file():
        return results
    try:
        conn = sqlite3.connect(str(SQLITE_KB))
        cur = conn.cursor()
        try:
            cur.execute(
                "SELECT id, content, title, prov_json FROM kb_index WHERE content LIKE ? LIMIT ?",
                (f"%{query}%", limit),
            )
            for row in cur.fetchall():
                cid, content, title, prov_json = row
                try:
                    p = json.loads(prov_json) if prov_json else {}
                except Exception:
                    p = {}
                results.append({
                    "source": "sqlite",
                    "title": title or "unknown",
                    "content": content[:200] if content else "",
                    "prov": _prov_entity(uri=f"sqlite:{cid}", label=title or "SQLite entry", prov=p)
                })
        except sqlite3.OperationalError:
            try:
                cur.execute("CREATE TABLE IF NOT EXISTS kb_index (id TEXT, content TEXT, title TEXT, prov_json TEXT)")
                conn.commit()
            except Exception:
                pass
        conn.close()
    except Exception:
        pass
    return results


def _query_bq(dataset_id, query_str, limit=10):
    if not HAS_BQ:
        return [], False
    try:
        client = bigquery.Client()
        qp = bigquery.ArrayQueryParameter("q", "STRING", f"%{query_str}%")
        rows = client.query(
            f"SELECT * FROM `{dataset_id}` WHERE LOWER(content) LIKE LOWER(q)",
            job_config={"maximum_results": limit},
            query_parameters=[qp],
        ).result()
        results = []
        for row in rows:
            rd = dict(row)
            results.append({
                "source": "bq",
                "data": rd,
                "prov": _prov_entity(
                    uri=f"bq:{dataset_id}:{rd.get('id', '?')}",
                    label=str(rd.get("title", "BQ entry")),
                    prov=rd.get("prov")
                )
            })
        return results, True
    except Exception as e:
        print(f"BQ error (fallback): {e}", file=sys.stderr)
        return [], False


class BigQueryAgentSearch:
    def __init__(self, dataset_id=None, query=None, limit=10, enterprise=False, offline=False):
        self.dataset_id = dataset_id
        self.query = query
        self.limit = limit
        self.enterprise = enterprise
        self.offline = offline

    def search(self):
        if self.enterprise and self.dataset_id and self.query:
            results, success = _query_bq(self.dataset_id, self.query, self.limit)
            if success and results:
                return {"mode": "enterprise_bq", "results": results, "query": self.query,
                        "dataset_id": self.dataset_id, "exit_code": 0}
        if self.offline:
            results = _search_local_kb(self.query, self.limit)
            results.extend(_search_sqlite(self.query, self.limit))
        else:
            results = _search_local_kb(self.query, self.limit)
        seen = set()
        deduped = []
        for r in results:
            uri = r.get("prov", {}).get("@id", "")
            if uri not in seen:
                seen.add(uri)
                deduped.append(r)
        return {"mode": "offline_local_kb", "results": deduped, "query": self.query, "exit_code": 0}

    def to_json(self):
        return json.dumps(self.search(), ensure_ascii=False, indent=2, default=str)


def main(argv=None):
    parser = argparse.ArgumentParser(description="BigQuery Agent Search (v5.4.0)")
    parser.add_argument("--dataset", default=None, help="BigQuery dataset ID")
    parser.add_argument("--query", default=None, help="Search query")
    parser.add_argument("--limit", type=int, default=10, help="Max results")
    parser.add_argument("--offline", action="store_true", help="Force offline mode")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--enterprise", action="store_true", help="Enterprise BQ mode")
    args = parser.parse_args(argv)
    if not args.query:
        print("Error: --query is required", file=sys.stderr)
        return 1
    agent = BigQueryAgentSearch(dataset_id=args.dataset, query=args.query, limit=args.limit,
                                enterprise=args.enterprise, offline=args.offline)
    result = agent.search()
    if args.json:
        print(agent.to_json())
    else:
        print(f"mode: {result.get('mode', 'unknown')}")
        print(f"query: {result.get('query', '')}")
        print(f"results: {len(result.get('results', []))}")
        for i, r in enumerate(result.get("results", []), 1):
            src = r.get("source", "unknown")
            label = r.get("prov", {}).get("label", "N/A")
            print(f"  {i}. [{src}] {label}: {str(r.get('preview', r.get('content', '')))[:150]}...")
    print(f"exit_code: {result.get('exit_code', 1)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())