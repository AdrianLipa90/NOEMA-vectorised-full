from ciel_sot_agent.cuda_probe import probe_cuda


def test_probe_cuda_has_required_keys() -> None:
    payload = probe_cuda()
    for key in (
        "cuda_available",
        "nvcc",
        "nvidia_smi",
        "cupy_installed",
        "cupy_import_ok",
        "cuda_runtime_ok",
        "device_count",
        "reason",
    ):
        assert key in payload
    assert isinstance(payload["reason"], list)
