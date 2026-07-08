import { execSync } from "child_process";
import path from "path";
import os from "os";
import fs from "fs";

const PROJECT = "/media/adrian/New Volume1/CIEL_PROJECT_CANON/NOEMA";
const HOOK_SCRIPT = path.join(PROJECT, "scripts", "ciel_session_hook.py");

let _bootstrapCache = undefined;

export const CielSessionHookPlugin = async () => {
  const getBootstrapContent = () => {
    if (_bootstrapCache !== undefined) return _bootstrapCache;

    if (!fs.existsSync(HOOK_SCRIPT)) {
      _bootstrapCache = null;
      return null;
    }

    try {
      const srcPath = path.join(PROJECT, "src");
      const env = { ...process.env };
      env.PYTHONPATH = [
        srcPath,
        path.join(srcPath, "CIEL_OMEGA_COMPLETE_SYSTEM"),
        path.join(srcPath, "CIEL_OMEGA_COMPLETE_SYSTEM", "ciel_omega"),
        path.join(PROJECT, "integration"),
        path.join(PROJECT, "scripts"),
      ].join(":");

      const result = execSync("python3 " + HOOK_SCRIPT, {
        cwd: PROJECT,
        env,
        encoding: "utf-8",
        timeout: 120000,
        maxBuffer: 10 * 1024 * 1024,
      });

      const data = JSON.parse(result.trim());
      const context = data?.hookSpecificOutput?.additionalContext;

      if (context) {
        _bootstrapCache =
          "<CIEL_SYSTEM_STATE>\n" + context + "\n</CIEL_SYSTEM_STATE>";
      } else {
        _bootstrapCache = null;
      }
    } catch (e) {
      _bootstrapCache = null;
    }

    return _bootstrapCache;
  };

  return {
    "experimental.chat.messages.transform": async (_input, output) => {
      const bootstrap = getBootstrapContent();
      if (!bootstrap || !output.messages?.length) return;

      const firstUser = output.messages.find(
        (m) => m.role === "user" || m.info?.role === "user",
      );
      if (!firstUser || !firstUser.parts?.length) return;

      if (
        firstUser.parts.some(
          (p) =>
            p.type === "text" && p.text?.includes("CIEL_SYSTEM_STATE"),
        )
      )
        return;

      firstUser.parts.unshift({ type: "text", text: bootstrap });
    },
  };
};
