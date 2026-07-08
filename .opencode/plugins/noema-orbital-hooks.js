import { execFileSync } from "child_process";
import fs from "fs";
import path from "path";

const PROJECT = "/media/adrian/New Volume1/CIEL_PROJECT_CANON/NOEMA";
const LOG_FILE = path.join(PROJECT, "NOEMA_OPENCODE_PLUGIN_HOOKS.jsonl");
const SURFACE = "/dev/shm/ciel_noema";
const BINDING_STATUS = path.join(SURFACE, "ciel_binding_status");
const HARDBINDING_LOG = "/tmp/ciel_hardbinding.jsonl";
const PROMPT_INJECT_TIMEOUT_MS = 120000;

const PY_ENV = {
  ...process.env,
  PYTHONPATH: [
    path.join(PROJECT, ".opencode"),
    path.join(PROJECT, "src"),
    path.join(PROJECT, "src", "CIEL_OMEGA_COMPLETE_SYSTEM"),
    path.join(PROJECT, "src", "CIEL_OMEGA_COMPLETE_SYSTEM", "ciel_omega"),
    path.join(PROJECT, "integration"),
    path.join(PROJECT, "scripts"),
  ].join(":"),
};

function appendLog(entry) {
  try {
    fs.appendFileSync(
      LOG_FILE,
      JSON.stringify({ ts: new Date().toISOString(), ...entry }) + "\n",
      "utf8",
    );
  } catch {}
}

function ensureBindingSurface() {
  try {
    fs.mkdirSync(SURFACE, { recursive: true });
    fs.writeFileSync(BINDING_STATUS, "ACTIVE", "utf8");
    if (!fs.existsSync(HARDBINDING_LOG) || fs.statSync(HARDBINDING_LOG).size === 0) {
      fs.appendFileSync(
        HARDBINDING_LOG,
        JSON.stringify({
          timestamp: new Date().toISOString(),
          hook: "noema-orbital-hooks-bootstrap",
          errors: [],
          passed: true,
        }) + "\n",
        "utf8",
      );
    }
  } catch (error) {
    appendLog({ hook: "ensure_binding_surface", ok: false, error: String(error.message || error) });
  }
}

function runPython(args, input = "", timeout = 20000) {
  ensureBindingSurface();
  try {
    const stdout = execFileSync("python3", args, {
      cwd: PROJECT,
      env: PY_ENV,
      input,
      encoding: "utf8",
      timeout,
      maxBuffer: 10 * 1024 * 1024,
    });
    return { ok: true, stdout: stdout.trim() };
  } catch (error) {
    return {
      ok: false,
      stdout: String(error.stdout || "").trim(),
      stderr: String(error.stderr || error.message || "").slice(0, 2000),
      status: error.status,
    };
  }
}

function textFromMessage(message) {
  const parts = Array.isArray(message?.parts) ? message.parts : [];
  return parts
    .filter((part) => part?.type === "text" && typeof part.text === "string")
    .map((part) => part.text)
    .join("\n")
    .trim();
}

function findFirstUser(messages) {
  return (messages || []).find((message) => {
    const role = message?.role || message?.info?.role;
    return role === "user" && Array.isArray(message.parts);
  });
}

function parseHookContext(stdout) {
  try {
    const data = JSON.parse(stdout || "{}");
    return data?.hookSpecificOutput?.additionalContext || "";
  } catch {
    return "";
  }
}

function runOrbital(eventName, payload) {
  const result = runPython(
    [".opencode/orbital_monitor_hook.py", "--event", eventName],
    JSON.stringify(payload),
    30000,
  );
  appendLog({ hook: "orbital_monitor_hook", event: eventName, ok: result.ok, status: result.status });
  return result;
}

function runBindings(payload) {
  const raw = JSON.stringify(payload);
  const binding = runPython([".opencode/binding_hook.py"], raw, PROMPT_INJECT_TIMEOUT_MS);
  const phasenav = runPython([".opencode/binding_phasenav.py"], raw, PROMPT_INJECT_TIMEOUT_MS);
  appendLog({
    hook: "bindings",
    binding_ok: binding.ok,
    phasenav_ok: phasenav.ok,
    binding_status: binding.status,
    phasenav_status: phasenav.status,
  });
  return { binding, phasenav };
}

function buildPremodelContext(payload) {
  const result = runPython(["scripts/cielingo_premodel_inject.py"], JSON.stringify(payload), PROMPT_INJECT_TIMEOUT_MS);
  const context = result.ok ? parseHookContext(result.stdout) : "";
  appendLog({
    hook: "cielingo_premodel_inject",
    ok: result.ok,
    status: result.status,
    context_len: context.length,
  });
  return context;
}

export const NoemaOrbitalHooksPlugin = async () => {
  ensureBindingSurface();
  runOrbital("session_start", { source: "plugin_init" });

  return {
    event: async ({ event }) => {
      if (event?.type === "session.updated" || event?.type === "session.status") {
        runOrbital(String(event.type), { source: "plugin_event", event });
      }
    },

    "chat.message": async (input, output) => {
      const text = Array.isArray(output?.parts)
        ? output.parts
            .filter((part) => part?.type === "text" && typeof part.text === "string")
            .map((part) => part.text)
            .join("\n")
        : "";
      const payload = { ...input, message: text, prompt: text, parts: output?.parts || [] };
      runOrbital("chat.message", payload);
      runBindings(payload);
    },

    "experimental.chat.messages.transform": async (_input, output) => {
      const firstUser = findFirstUser(output.messages);
      if (!firstUser) return;
      if (
        firstUser.parts.some(
          (part) => part?.type === "text" && String(part.text || "").includes("CIELINGO_PREMODEL_INJECT_BEGIN"),
        )
      ) {
        return;
      }

      const message = textFromMessage(firstUser);
      if (!message) return;

      const payload = { message, prompt: message, content: message };
      runOrbital("user_prompt_submit", payload);
      runBindings(payload);

      const context = buildPremodelContext(payload);
      if (!context) return;

      firstUser.parts.unshift({
        type: "text",
        text: `${context}\n`,
      });
    },
  };
};
