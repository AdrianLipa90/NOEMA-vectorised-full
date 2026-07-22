#!/usr/bin/env python3
"""Debug eBPF map reads."""
import sys, time, ctypes
from bcc import BPF

if __name__ == "__main__":
    bpf_text = """
    #include <uapi/linux/ptrace.h>
    BPF_PERCPU_ARRAY(cpu_util, u64, 8);
    BPF_ARRAY(ctx_switches, u64, 1);
    BPF_ARRAY(syscall_count, u64, 1);
    BPF_ARRAY(irq_count, u64, 1);
    int trace_sched_switch(struct tracepoint__sched__sched_switch *ctx) {
        u32 cpu = bpf_get_smp_processor_id();
        if (cpu >= 8) return 0;
        u32 key = cpu;
        u64 *val = cpu_util.lookup(&key);
        if (val) { lock_xadd(val, 1); }
        u32 zero = 0;
        u64 *cs = ctx_switches.lookup(&zero);
        if (cs) { lock_xadd(cs, 1); }
        return 0;
    }
    int trace_sys_enter_openat(struct tracepoint__syscalls__sys_enter_openat *ctx) {
        u32 zero = 0;
        u64 *val = syscall_count.lookup(&zero);
        if (val) { lock_xadd(val, 1); }
        return 0;
    }
    int trace_irq_handler_entry(struct tracepoint__irq__irq_handler_entry *ctx) {
        u32 zero = 0;
        u64 *val = irq_count.lookup(&zero);
        if (val) { lock_xadd(val, 1); }
        return 0;
    }
    """

    b = BPF(text=bpf_text)
    b.attach_tracepoint(tp="sched:sched_switch", fn_name="trace_sched_switch")
    b.attach_tracepoint(tp="syscalls:sys_enter_openat", fn_name="trace_sys_enter_openat")
    b.attach_tracepoint(tp="irq:irq_handler_entry", fn_name="trace_irq_handler_entry")

    print("Collecting...", flush=True)
    time.sleep(3)

    # Try items()
    for name in ["cpu_util", "ctx_switches", "syscall_count", "irq_count"]:
        try:
            m = b[name]
            print(f"{name} type: {type(m).__name__}")
            # items
            try:
                items = list(m.items())
                print(f"  items: {items[:5]}")
            except Exception as e:
                print(f"  items error: {e}")
            # read with key
            try:
                val = m.read(ctypes.c_uint32(0))
                print(f"  read(0): {val} type={type(val).__name__}")
            except Exception as e:
                print(f"  read(0) error: {e}")
            # for arrays, try __getitem__
            try:
                val = m[0]
                print(f"  [0]: {val} type={type(val).__name__}")
            except Exception as e:
                print(f"  [0] error: {e}")
        except Exception as e:
            print(f"{name}: {e}")

    print("Done")
