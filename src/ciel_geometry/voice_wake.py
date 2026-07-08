"""Wake word detector — MFCC template + cosine similarity. ~5MB RAM."""

import numpy as np

SR = 16000
FRAME = 512
HOP = 256
N_MFCC = 13


def mfcc_mean(audio: np.ndarray) -> np.ndarray:
    """Audio → mean MFCC vector (13D, normalized)."""
    frames = []
    n = len(audio)
    for i in range(0, n - FRAME + 1, HOP):
        seg = audio[i:i+FRAME] * np.hanning(FRAME)
        spec = np.abs(np.fft.rfft(seg))
        n_fft = len(spec)
        mel = np.zeros(N_MFCC, np.float32)
        freqs = np.linspace(0, SR/2, n_fft)
        mel_pts = np.linspace(0, SR/2, N_MFCC + 2)
        for m in range(N_MFCC):
            lo, hi = mel_pts[m], mel_pts[m+2]
            mid = (lo + hi) / 2
            mask = (freqs >= lo) & (freqs <= hi)
            if not mask.any(): continue
            w = 1.0 - np.abs(freqs[mask] - mid) / (mid - lo + 1e-10)
            mel[m] = np.dot(spec[mask], w)
        frames.append(np.log1p(mel * 1e5))
    if not frames:
        return np.zeros(N_MFCC, np.float32)
    vec = np.mean(frames, axis=0)
    n = np.linalg.norm(vec)
    return vec / n if n > 0 else vec


def record_template(duration: float = 1.5) -> np.ndarray:
    """Record → mean MFCC template vector."""
    import subprocess
    n = int(SR * duration)
    cmd = ["arecord", "-q", "-t", "raw", "-f", "S16_LE",
           "-r", str(SR), "-c", "1", "-d", str(int(duration)),
           "--buffer-size=4096"]
    raw = subprocess.check_output(cmd)
    audio = np.frombuffer(raw, dtype=np.int16).astype(np.float32)
    return mfcc_mean(audio)


class WakeWordDetector:
    """Cosine-similarity wake word detector."""

    def __init__(self, template: np.ndarray, threshold: float = 0.85):
        self.template = template
        self.threshold = threshold
        self.buffer = np.zeros(0, np.float32)

    def feed(self, chunk: bytes) -> float:
        """Return similarity score (0-1). > threshold = wake word."""
        audio = np.frombuffer(chunk, dtype=np.int16).astype(np.float32)
        self.buffer = np.concatenate([self.buffer, audio])
        max_n = int(SR * 2.0)
        if len(self.buffer) > max_n:
            self.buffer = self.buffer[-max_n:]

        win_n = int(SR * 0.8)  # 0.8s window
        if len(self.buffer) < win_n:
            return 0.0

        best = 0.0
        for start in range(0, len(self.buffer) - win_n + 1, HOP):
            seg = self.buffer[start:start + win_n]
            rms = np.sqrt(np.mean(seg**2))
            if rms < 4000:  # above fan noise floor
                continue
            vec = mfcc_mean(seg)
            sim = float(np.dot(vec, self.template))
            if sim > best:
                best = sim

        return best
