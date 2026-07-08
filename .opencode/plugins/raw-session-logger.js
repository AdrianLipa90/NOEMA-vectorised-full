import fs from "fs";
import path from "path";

const PROJECT = "/media/adrian/New Volume1/CIEL_PROJECT_CANON/NOEMA";
const LOG_ROOT = path.join(PROJECT, ".opencode", "raw-sessions");

const sessionDirs = new Map();
const seenMarkdown = new Set();

function safeName(value) {
  return String(value || "unknown").replace(/[^a-zA-Z0-9_.-]/g, "_").slice(0, 120);
}

function nowStamp() {
  return new Date().toISOString();
}

function filesystemStamp() {
  return nowStamp().replace(/[:.]/g, "-");
}

function ensureSessionDir(sessionID) {
  const id = safeName(sessionID);
  if (sessionDirs.has(id)) return sessionDirs.get(id);

  const dir = path.join(LOG_ROOT, `${filesystemStamp()}_${id}`);
  fs.mkdirSync(dir, { recursive: true });
  sessionDirs.set(id, dir);
  return dir;
}

function appendJSONL(file, value) {
  fs.appendFileSync(file, JSON.stringify(value) + "\n", "utf8");
}

function appendMarkdownOnce(dir, key, markdown) {
  if (seenMarkdown.has(key)) return;
  seenMarkdown.add(key);
  fs.appendFileSync(path.join(dir, "chat.md"), markdown + "\n", "utf8");
}

function extractSessionID(event) {
  return (
    event?.properties?.sessionID ||
    event?.properties?.info?.sessionID ||
    event?.properties?.part?.sessionID ||
    event?.properties?.message?.sessionID ||
    event?.sessionID ||
    "unknown"
  );
}

function textFromParts(parts) {
  if (!Array.isArray(parts)) return "";
  return parts
    .filter((part) => part?.type === "text" && typeof part.text === "string")
    .map((part) => part.text)
    .join("\n");
}

function markdownBlock(title, value) {
  const body = typeof value === "string" ? value : JSON.stringify(value, null, 2);
  return `\n## ${title}\n\n${body || "_empty_"}\n`;
}

function writeEvent(event) {
  const sessionID = extractSessionID(event);
  const dir = ensureSessionDir(sessionID);
  const record = {
    ts: nowStamp(),
    kind: "event",
    event,
  };

  appendJSONL(path.join(dir, "events.jsonl"), record);

  const type = event?.type || "event";
  const props = event?.properties || {};

  if (type === "message.updated" && props.info) {
    appendJSONL(path.join(dir, "chat.jsonl"), {
      ts: record.ts,
      kind: "message.updated",
      message: props.info,
    });
    appendMarkdownOnce(
      dir,
      `${sessionID}:${type}:${props.info.id}:${JSON.stringify(props.info)}`,
      markdownBlock(`${props.info.role || "message"} ${props.info.id || ""}`.trim(), props.info),
    );
  }

  if (type === "message.part.updated" && props.part) {
    appendJSONL(path.join(dir, "chat.jsonl"), {
      ts: record.ts,
      kind: "message.part.updated",
      part: props.part,
    });
    if (props.part.type === "text" && props.part.text) {
      appendMarkdownOnce(
        dir,
        `${sessionID}:${type}:${props.part.id}:${props.part.text}`,
        markdownBlock(`text part ${props.part.messageID || ""}`.trim(), props.part.text),
      );
    }
  }
}

export const RawSessionLoggerPlugin = async () => {
  fs.mkdirSync(LOG_ROOT, { recursive: true });

  return {
    event: async ({ event }) => {
      try {
        writeEvent(event);
      } catch (error) {
        console.error("[raw-session-logger:event]", error?.message || error);
      }
    },

    "chat.message": async (input, output) => {
      try {
        const dir = ensureSessionDir(input.sessionID);
        const record = {
          ts: nowStamp(),
          kind: "chat.message",
          input,
          message: output.message,
          parts: output.parts,
        };

        appendJSONL(path.join(dir, "chat.jsonl"), record);
        appendJSONL(path.join(dir, "events.jsonl"), record);

        const text = textFromParts(output.parts);
        appendMarkdownOnce(
          dir,
          `${input.sessionID}:chat.message:${input.messageID || output.message?.id}:${text}`,
          markdownBlock(`user ${input.messageID || output.message?.id || ""}`.trim(), text || record),
        );
      } catch (error) {
        console.error("[raw-session-logger:chat.message]", error?.message || error);
      }
    },

    "tool.execute.before": async (input, output) => {
      try {
        const dir = ensureSessionDir(input.sessionID);
        appendJSONL(path.join(dir, "tools.jsonl"), {
          ts: nowStamp(),
          kind: "tool.execute.before",
          input,
          args: output.args,
        });
      } catch (error) {
        console.error("[raw-session-logger:tool.before]", error?.message || error);
      }
    },

    "tool.execute.after": async (input, output) => {
      try {
        const dir = ensureSessionDir(input.sessionID);
        appendJSONL(path.join(dir, "tools.jsonl"), {
          ts: nowStamp(),
          kind: "tool.execute.after",
          input,
          output,
        });
      } catch (error) {
        console.error("[raw-session-logger:tool.after]", error?.message || error);
      }
    },
  };
};
