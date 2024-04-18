from .base import BaseClient

import sqlite3
import json

import logging

LOGGER = logging.getLogger("piddiplatsch")

conn = sqlite3.connect(":memory:")
cursor = conn.cursor()


def table_exists(table_name):
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,)
    )
    return cursor.fetchone() is not None


if not table_exists("data"):
    cursor.execute(
        """CREATE TABLE data (
                id TEXT PRIMARY KEY,
                json_string TEXT
        )"""
    )


class DummyClient(BaseClient):

    def register_handle(self, handle, record):
        LOGGER.info(f"handle: {handle}")
        LOGGER.info(f"record: {record}")

        data = json.dumps(record)

        cursor.execute(
            """INSERT INTO data (id, json_string) VALUES (?, ?)""",
            (handle, data),
        )
        conn.commit()

    def check_if_handle_exists(self, handle):
        if not handle:
            return False
        elif "invalid" in handle:
            return False
        return True
