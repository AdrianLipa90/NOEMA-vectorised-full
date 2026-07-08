/* NOEMA eBPF Sensor — real-time system → 36 oscillator surface.
 * Authors: Ciel Apocalyptos & NOEMA (2026)
 *
 * Hooks:
 *   sched_switch          → CPU utilization, context switches
 *   sys_enter_openat      → filesystem pressure
 *   irq_handler_entry     → I/O interrupts
 *   page_fault_user       → memory pressure
 *   block_rq_complete     → disk I/O
 *
 * Simple counter maps allow Python (BCC) to snapshot and phi-map.
 */
#include <uapi/linux/ptrace.h>
#include <linux/sched.h>

#define N_OSCILLATORS 36

/* Counter arrays */
BPF_PERCPU_ARRAY(cpu_util, u64, 8);           /* per-core sched switches */
BPF_ARRAY(ctx_switches, u64, 1);              /* global context switches */
BPF_ARRAY(syscall_count, u64, 1);             /* openat syscalls         */
BPF_ARRAY(irq_count, u64, 1);                 /* IRQ handlers            */
BPF_PERCPU_ARRAY(page_faults, u64, 8);        /* per-core page faults    */
BPF_ARRAY(block_io_count, u64, 1);            /* block I/O completions   */

/* ── sched_switch ────────────────────────────────────────────────*/
int trace_sched_switch(struct tracepoint__sched__sched_switch *ctx)
{
    u32 cpu = bpf_get_smp_processor_id();
    if (cpu >= 8) return 0;

    u32 key = cpu;
    u64 *val = cpu_util.lookup(&key);
    if (val) lock_xadd(val, 1);

    u32 zero = 0;
    u64 *cs = ctx_switches.lookup(&zero);
    if (cs) lock_xadd(cs, 1);

    return 0;
}

/* ── sys_enter_openat ────────────────────────────────────────────*/
int trace_sys_enter_openat(struct tracepoint__syscalls__sys_enter_openat *ctx)
{
    u32 zero = 0;
    u64 *val = syscall_count.lookup(&zero);
    if (val) lock_xadd(val, 1);
    return 0;
}

/* ── irq_handler_entry ───────────────────────────────────────────*/
int trace_irq_handler_entry(struct tracepoint__irq__irq_handler_entry *ctx)
{
    u32 zero = 0;
    u64 *val = irq_count.lookup(&zero);
    if (val) lock_xadd(val, 1);
    return 0;
}

/* ── page_fault_user ─────────────────────────────────────────────*/
int trace_page_fault_user(struct tracepoint__exceptions__page_fault_user *ctx)
{
    u32 cpu = bpf_get_smp_processor_id();
    if (cpu >= 8) return 0;

    u32 key = cpu;
    u64 *val = page_faults.lookup(&key);
    if (val) lock_xadd(val, 1);
    return 0;
}

/* ── block_rq_complete ───────────────────────────────────────────*/
int trace_block_rq_complete(struct tracepoint__block__block_rq_complete *ctx)
{
    u32 zero = 0;
    u64 *val = block_io_count.lookup(&zero);
    if (val) lock_xadd(val, 1);
    return 0;
}
