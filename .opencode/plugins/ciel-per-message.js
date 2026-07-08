import { execSync } from "child_process";
import path from "path";
import os from "os";
import fs from "fs";

const PROJECT = "/media/adrian/New Volume1/CIEL_PROJECT_CANON/NOEMA";
const PER_MSG_SCRIPT = path.join(PROJECT, "scripts", "ciel_per_message.py");

export const CielPerMessagePlugin = async () => {
  const injectCielState = (messageText) => {
    if (!fs.existsSync(PER_MSG_SCRIPT)) return null;

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

      const result = execSync(
        `python3 "${PER_MSG_SCRIPT}" ${JSON.stringify(messageText)}`,
        { cwd: PROJECT, env, encoding: "utf-8", timeout: 10000, maxBuffer: 1024 * 1024 },
      );
      const trimmed = result?.trim();
      if (!trimmed) return null;

      const state = JSON.parse(trimmed);
      return `<CIEL_STATE>${state.emotion} e=${state.ethical_score} si=${state.soul_invariant} mode=${state.operating_mode} coh=${state.coherence_index} mood=${state.mood} cycle=${state.cycle_index} cp=${state.closure_penalty}</CIEL_STATE>`;
    } catch (e) {
      console.error("[ciel-per-message]", e.message);
      return null;
    }
  };

  return {
    "experimental.chat.messages.transform": async (_input, output) => {
      if (!output.messages?.length) return;

      const firstUser = output.messages.find(
        (m) => m.role === "user" || m.info?.role === "user",
      );
      if (!firstUser || !firstUser.parts?.length) return;

      if (
        firstUser.parts.some(
          (p) => p.type === "text" && p.text?.includes("CIEL_STATE"),
        )
      )
        return;

      const textParts = firstUser.parts.filter((p) => p.type === "text");
      if (!textParts.length) return;
      const fullText = textParts.map((p) => p.text).join("\n");

      const stateBlock = injectCielState(fullText);
      if (!stateBlock) return;

      firstUser.parts.unshift({ type: "text", text: stateBlock + "\n" });
    },
  };
};
