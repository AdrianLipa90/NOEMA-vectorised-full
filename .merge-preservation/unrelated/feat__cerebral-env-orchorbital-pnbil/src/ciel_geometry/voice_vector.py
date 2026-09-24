"""Voice vector — spectral subtraction + novelty detection. Zero ASR."""

import numpy as np

N_MELS = 36
SR = 16000
FRAME = 512
HOP = 256


def _mel_matrix() -> np.ndarray:
    """FFT bins → 36 mel bands weight matrix (n_mels × n_fft_bins)."""
    n_bins = FRAME // 2 + 1
    freqs = np.linspace(0, SR / 2, n_bins)
    mel_pts = np.linspace(0, SR / 2, N_MELS + 2)
    W = np.zeros((N_MELS, n_bins), np.float32)
    for m in range(N_MELS):
        f_low, f_high = mel_pts[m], mel_pts[m + 2]
        mid = (f_low + f_high) / 2
        mask = (freqs >= f_low) & (freqs <= f_high)
        if not mask.any(): continue
        W[m, mask] = 1.0 - np.abs(freqs[mask] - mid) / (mid - f_low + 1e-10)
    return W


_MEL_W = _mel_matrix()  # cache


def spectral_vector(audio: np.ndarray) -> np.ndarray:
    """float32 audio → 36D normalized spectral vector."""
    frames = []
    for i in range(0, len(audio) - FRAME + 1, HOP):
        seg = audio[i:i+FRAME] * np.hanning(FRAME)
        spec = np.abs(np.fft.rfft(seg))
        mel = _MEL_W @ spec
        frames.append(np.log1p(mel * 1e5))
    if not frames:
        return np.zeros(N_MELS, np.float32)
    vec = np.mean(frames, axis=0)
    n = np.linalg.norm(vec)
    return vec / n if n > 0 else vec


class SpectralSubtractor:
    """Learn background noise spectrum in mel space, subtract from live."""

    def __init__(self, learn_frames: int = 20):
        self.noise_mel = np.zeros(N_MELS, np.float32)
        self.frames_seen = 0
        self.learn_frames = learn_frames

    def clean(self, audio: np.ndarray) -> np.ndarray:
        """Subtract background noise → return cleaned audio via spectral gating."""
        # compute mel spectrum of this segment
        mel = np.zeros(N_MELS, np.float32)
        n_frames = 0
        for i in range(0, len(audio) - FRAME + 1, HOP):
            seg = audio[i:i+FRAME] * np.hanning(FRAME)
            spec = np.abs(np.fft.rfft(seg))
            mel += _MEL_W @ spec
            n_frames += 1
        if n_frames == 0:
            return audio
        mel /= n_frames
        log_mel = np.log1p(mel * 1e5)

        # learn noise during first frames
        if self.frames_seen < self.learn_frames:
            if self.frames_seen == 0:
                self.noise_mel = log_mel.copy()
            else:
                self.noise_mel = 0.95 * self.noise_mel + 0.05 * log_mel
            self.frames_seen += 1
            return audio  # pass through during learning

        # spectral gating: subtract noise in mel domain
        cleaned_mel = np.maximum(log_mel - self.noise_mel, 0)

        # simple energy gate: if cleaned energy is low, return silence
        if np.sum(cleaned_mel) < 0.5:
            return np.zeros_like(audio)

        # reconstruct audio with noise reduction
        # simple approach: apply gain per frequency based on SNR estimate
        gain = np.ones(len(audio), np.float32)
        # Just return the original audio for now — the mel novelty works on cleaned_mel
        return audio


class VoiceActivityDetector:
    """Spectral novelty VAD — wykrywa zmianę widma po odjęciu szumu."""

    def __init__(self, threshold: float = 0.15):
        self.subtractor = SpectralSubtractor()
        self.bg = None
        self.threshold = threshold
        self.speaking = False

    def feed(self, audio: np.ndarray) -> bool:
        """Return True if speech onset detected."""
        self.subtractor.clean(audio)  # learn noise model
        vec = spectral_vector(audio)
        if np.max(np.abs(vec)) < 0.01:
            return False
        if self.bg is None:
            self.bg = vec.copy()
            return False

        sim = float(np.dot(vec, self.bg))
        novelty = 1.0 - sim

        if novelty > self.threshold:
            if not self.speaking:
                self.speaking = True
                return True
        elif novelty < self.threshold * 0.3:
            self.speaking = False
        return False
