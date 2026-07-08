#!/usr/bin/env python3
"""Minimal client for local opencode headless server."""
from __future__ import annotations
import json, urllib.request, urllib.parse
from typing import Any

class OpencodeBodyClient:
    def __init__(self, base_url: str, directory: str):
        self.base_url = base_url.rstrip('/')
        self.directory = directory

    def _request(self, method: str, path: str, body: dict | None = None) -> Any:
        url = self.base_url + path
        if '?' not in url:
            url += ('?' if '?' not in url else '&') + 'directory=' + urllib.parse.quote(self.directory)
        data = None
        headers = {'Content-Type': 'application/json', 'x-opencode-directory': self.directory}
        if body is not None:
            data = json.dumps(body).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        with urllib.request.urlopen(req, timeout=30) as r:
            raw = r.read().decode('utf-8')
            return json.loads(raw) if raw else None

    def list_sessions(self):
        return self._request('GET', '/session')

    def create_session(self, title: str | None = None, parent_id: str | None = None):
        body = {}
        if title:
            body['title'] = title
        if parent_id:
            body['parentID'] = parent_id
        return self._request('POST', '/session', body)

    def prompt(self, session_id: str, text: str, agent: str = 'build'):
        body = {
            'agent': agent,
            'parts': [{'type': 'text', 'text': text}],
        }
        return self._request('POST', f'/session/{session_id}/message', body)

    def messages(self, session_id: str):
        return self._request('GET', f'/session/{session_id}/messages')

    def agents(self):
        return self._request('GET', '/app/agents')

    def tui_append_prompt(self, text: str):
        return self._request('POST', '/tui/append-prompt', {'text': text})
