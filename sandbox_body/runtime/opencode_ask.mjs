#!/usr/bin/env -S /home/adrian/.cache/ms-playwright-go/1.57.0/node
/**
 * opencode_ask.mjs — zapytaj model opencode przez SDK.
 * Użycie: echo "prompt" | ./opencode_ask.mjs [model]
 *         ./opencode_ask.mjs "promt" [model]
 *         
 * Domyślny model: opencode/deepseek-v4-flash-free
 */

import { createOpencode } from '@opencode-ai/sdk';
import { readFileSync } from 'fs';

const model = process.argv[3] || process.env.OPENCODE_MODEL || 'opencode/deepseek-v4-flash-free';

// Prompt z argumentu lub stdin
let prompt = process.argv[2];
if (!prompt) {
  try {
    prompt = readFileSync('/dev/stdin', 'utf-8').trim();
  } catch {}
}
if (!prompt) {
  console.error('Usage: echo "prompt" | opencode_ask.mjs [model]');
  process.exit(1);
}

try {
  const oc = await createOpencode({
    config: {
      model: model,
    },
  });

  const result = await oc.client.chat.completions.create({
    model: model,
    messages: [{ role: 'user', content: prompt }],
    max_tokens: 800,
    temperature: 0.7,
  });

  const text = result.choices?.[0]?.message?.content?.trim() || '';
  if (text) {
    // Wyczyść ewentualne znaczniki agenta
    const clean = text.replace(/^>\s+\w+\s+·\s+\S+\s*$/gm, '').trim();
    console.log(clean);
  }

  await oc.server.stop?.();
  process.exit(0);
} catch (e) {
  console.error('ERROR:', e.message);
  process.exit(1);
}
