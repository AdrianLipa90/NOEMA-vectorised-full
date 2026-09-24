// PhaseNav Linux scheduler eBPF — Kuramoto per-PID phase tracking
// Uses kprobe on finish_task_switch.isra.0 (Kernel 6.17.x)
#include <uapi/linux/ptrace.h>
#include <linux/sched.h>

#define TWO_PI_SCALE 1000000

// Per-PID phase accumulator (0..TWO_PI_SCALE)
BPF_HASH(pid_phase, u32, u64, 8192);

// Per-PID runtime counter
BPF_HASH(pid_runtime, u32, u64, 8192);

int trace_finish_task_switch(struct pt_regs *ctx) {
    struct task_struct *prev = (struct task_struct *)PT_REGS_PARM1(ctx);
    if (!prev) return 0;
    u32 pid = prev->pid;
    if (pid == 0) return 0;

    u64 *phase = pid_phase.lookup(&pid);
    if (phase) {
        *phase = (*phase + 100) % TWO_PI_SCALE;
    } else {
        u64 init = 1;
        pid_phase.update(&pid, &init);
    }

    u64 *rt = pid_runtime.lookup(&pid);
    if (rt) {
        *rt += 1;
    } else {
        u64 init = 1;
        pid_runtime.update(&pid, &init);
    }
    return 0;
}
