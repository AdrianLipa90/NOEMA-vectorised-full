#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include <string.h>
#include <pthread.h>
#include <unistd.h>
#include <sys/stat.h>
#include <errno.h>
#include <stdint.h>

#define N_OSCILLATORS 24
#define DT 1e-3
#define BASE_FREQ 7.83
#define FREQ_SPREAD 2.0
#define PI 3.14159265358979323846
#define TWOPI 6.28318530717958647692

static const char *RESULT_ROOT;
static const char *PROJECT_DIR = "kuramoto_substrate";
static const char *VERSION = "v1.0";

/* Results root, config-driven like ciel_geometry.paths.P.RESULTS.
 * Override with NOEMA_RESULTS env var; falls back to the canonical
 * repo's results/ dir (never Pulpit/Desktop). */
static const char *results_root(void) {
    const char *env = getenv("NOEMA_RESULTS");
    if (env && env[0]) return env;
    return "/media/adrian/New Volume1/CIEL_PROJECT_CANON/NOEMA/results";
}

typedef struct {
    double *R;
    double *psi;
    double *phases;
    double *dphi;
    int *windings;
    int steps;
    int n;
    double kappa;
    double R_final;
    double R_mean;
    double R_std;
} KuramotoResult;

static double lcg_next(uint64_t *state) {
    *state = *state * 6364136223846793005ULL + 1442695040888963407ULL;
    return (double)(*state >> 11) * 0x1p-53;
}

static double normal_sample(double mean, double stddev, uint64_t *state) {
    double u1, u2;
    do { u1 = lcg_next(state); } while (u1 <= 1e-15);
    u2 = lcg_next(state);
    return mean + sqrt(-2.0 * log(u1)) * cos(TWOPI * u2) * stddev;
}

static double uniform_sample(uint64_t *state) {
    return lcg_next(state);
}

static uint64_t splitmix64(uint64_t seed) {
    seed += 0x9E3779B97F4A7C15ULL;
    uint64_t z = seed;
    z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ULL;
    z = (z ^ (z >> 27)) * 0x94D049BB133111EBULL;
    return z ^ (z >> 31);
}

static void generate_omegas(double *omega, int n, double base, double spread, uint64_t seed) {
    uint64_t state = splitmix64(seed);
    for (int i = 0; i < n; i++)
        omega[i] = normal_sample(base, spread, &state);
}

static KuramotoResult *run_kuramoto(double kappa, int steps, const double *omega, int n, uint64_t seed) {
    KuramotoResult *res = calloc(1, sizeof(KuramotoResult));
    res->n = n;
    res->steps = steps;
    res->kappa = kappa;
    res->R = calloc(steps, sizeof(double));
    res->psi = calloc(steps, sizeof(double));
    res->phases = calloc(steps * n, sizeof(double));
    res->dphi = calloc(steps * n, sizeof(double));
    res->windings = calloc(steps * n, sizeof(int));

    double *phases = calloc(n, sizeof(double));
    int *winding_count = calloc(n, sizeof(int));
    uint64_t state = splitmix64(seed + 1);
    for (int i = 0; i < n; i++)
        phases[i] = uniform_sample(&state) * TWOPI;

    double *omega_rad = calloc(n, sizeof(double));
    for (int i = 0; i < n; i++)
        omega_rad[i] = TWOPI * omega[i];

    for (int t = 0; t < steps; t++) {
        double sum_re = 0.0, sum_im = 0.0;
        for (int i = 0; i < n; i++) {
            sum_re += cos(phases[i]);
            sum_im += sin(phases[i]);
        }
        double R = sqrt(sum_re * sum_re + sum_im * sum_im) / n;
        double psi = atan2(sum_im, sum_re);

        for (int i = 0; i < n; i++) {
            double dphi_i = omega_rad[i] + kappa * R * sin(psi - phases[i]);
            res->dphi[t * n + i] = dphi_i;
            phases[i] += dphi_i * DT;

            if (phases[i] >= TWOPI) {
                phases[i] -= TWOPI;
                winding_count[i]++;
            } else if (phases[i] < 0.0) {
                phases[i] += TWOPI;
                winding_count[i]--;
            }

            res->phases[t * n + i] = phases[i];
            res->windings[t * n + i] = winding_count[i];
        }

        res->R[t] = R;
        res->psi[t] = psi;
    }

    res->R_final = res->R[steps - 1];
    double sum = 0.0;
    int tail_start = (steps > 1000) ? steps - 1000 : 0;
    for (int t = tail_start; t < steps; t++) sum += res->R[t];
    res->R_mean = sum / (steps - tail_start);

    double var = 0.0;
    for (int t = tail_start; t < steps; t++) {
        double d = res->R[t] - res->R_mean;
        var += d * d;
    }
    res->R_std = sqrt(var / (steps - tail_start));

    free(phases);
    free(winding_count);
    free(omega_rad);
    return res;
}

static void free_result(KuramotoResult *res) {
    if (!res) return;
    free(res->R);
    free(res->psi);
    free(res->phases);
    free(res->dphi);
    free(res->windings);
    free(res);
}

static void ensure_dirs(const char *base) {
    const char *subdirs[] = {"raw_data", "plots", "configs", "logs", "archive"};
    for (int i = 0; i < 5; i++) {
        char path[1024];
        snprintf(path, sizeof(path), "%s/%s", base, subdirs[i]);
        mkdir(path, 0755);
    }
}

static void save_json_result(const KuramotoResult *res, const char *eid, const char *base) {
    char path[1024];
    snprintf(path, sizeof(path), "%s/raw_data/%s_raw.json", base, eid);
    FILE *f = fopen(path, "w");
    if (!f) { perror("fopen"); return; }

    fprintf(f, "{\n");
    fprintf(f, " \"experiment_id\": \"%s\",\n", eid);
    fprintf(f, " \"kappa\": %.6f,\n", res->kappa);
    fprintf(f, " \"n\": %d,\n", res->n);
    fprintf(f, " \"steps\": %d,\n", res->steps);
    fprintf(f, " \"R_final\": %.10f,\n", res->R_final);
    fprintf(f, " \"R_mean\": %.10f,\n", res->R_mean);
    fprintf(f, " \"R_std\": %.10f,\n", res->R_std);

    fprintf(f, " \"t\": [");
    for (int t = 0; t < res->steps; t++) {
        if (t > 0) fprintf(f, ",");
        fprintf(f, "%.6f", t * DT);
    }
    fprintf(f, "],\n");

    fprintf(f, " \"R\": [");
    for (int t = 0; t < res->steps; t++) {
        if (t > 0) fprintf(f, ",");
        fprintf(f, "%.10f", res->R[t]);
    }
    fprintf(f, "],\n");

    fprintf(f, " \"psi\": [");
    for (int t = 0; t < res->steps; t++) {
        if (t > 0) fprintf(f, ",");
        fprintf(f, "%.10f", res->psi[t]);
    }
    fprintf(f, "]\n");

    fprintf(f, "}\n");
    fclose(f);
}

static void log_experiment(const KuramotoResult *res, const char *eid, const char *base, const char *notes) {
    char path[1024];
    snprintf(path, sizeof(path), "%s/logs/experiments.csv", base);
    int exists = (access(path, F_OK) == 0);
    FILE *f = fopen(path, "a");
    if (!f) return;
    if (!exists)
        fprintf(f, "experiment_id,timestamp,kappa,n,steps,R_final,R_mean,R_std,notes\n");
    time_t now = time(NULL);
    char ts[64];
    strftime(ts, sizeof(ts), "%Y-%m-%dT%H:%M:%SZ", gmtime(&now));
    fprintf(f, "%s,%s,%.6f,%d,%d,%.6f,%.6f,%.6f,%s\n",
            eid, ts, res->kappa, res->n, res->steps,
            res->R_final, res->R_mean, res->R_std, notes ? notes : "");
    fclose(f);

    char global_path[1024];
    snprintf(global_path, sizeof(global_path), "%s/meta/global_experiments.csv", results_root());
    int gexists = (access(global_path, F_OK) == 0);
    f = fopen(global_path, "a");
    if (f) {
        if (!gexists)
            fprintf(f, "project_id,experiment_id,timestamp,kappa,n,steps,R_final,R_mean,R_std,notes\n");
        fprintf(f, "%s,%s,%s,%.6f,%d,%d,%.6f,%.6f,%.6f,%s\n",
                PROJECT_DIR, eid, ts, res->kappa, res->n, res->steps,
                res->R_final, res->R_mean, res->R_std, notes ? notes : "");
        fclose(f);
    }
}

static void experiment_id(char *buf, size_t sz) {
    time_t now = time(NULL);
    struct tm *gmt = gmtime(&now);
    strftime(buf, sz, "K%Y%m%d_%H%M%S", gmt);
}

typedef struct {
    int thread_id;
    int n_threads;
    int n_kappas;
    double *kappas;
    int steps;
    uint64_t seed;
    double *omega;
    char base[1024];
    char notes[256];
    int count;
} SweepThreadArg;

static void *sweep_worker(void *arg) {
    SweepThreadArg *a = (SweepThreadArg *)arg;
    for (int i = a->thread_id; i < a->n_kappas; i += a->n_threads) {
        double k = a->kappas[i];
        char eid[64];
        experiment_id(eid, sizeof(eid));
        char keid[128];
        snprintf(keid, sizeof(keid), "%s_K%.3f", eid, k);

        KuramotoResult *res = run_kuramoto(k, a->steps, a->omega, N_OSCILLATORS, a->seed + (uint64_t)(k * 1000));
        (void)a;
        save_json_result(res, keid, a->base);
        log_experiment(res, keid, a->base, a->notes);
        free_result(res);
        a->count++;
    }
    return NULL;
}

static void sweep_kappas(double *kappas, int n_kappas, int steps, uint64_t seed, const char *notes, int n_threads) {
    char base[1024];
    snprintf(base, sizeof(base), "%s/projects/%s/%s", results_root(), PROJECT_DIR, VERSION);
    ensure_dirs(base);

    double omega[N_OSCILLATORS];
    generate_omegas(omega, N_OSCILLATORS, BASE_FREQ, FREQ_SPREAD, seed);

    if (n_threads > n_kappas) n_threads = n_kappas;
    pthread_t *threads = calloc(n_threads, sizeof(pthread_t));
    SweepThreadArg *args = calloc(n_threads, sizeof(SweepThreadArg));

    for (int t = 0; t < n_threads; t++) {
        args[t].thread_id = t;
        args[t].n_threads = n_threads;
        args[t].n_kappas = n_kappas;
        args[t].kappas = kappas;
        args[t].steps = steps;
        args[t].seed = seed;
        args[t].omega = omega;
        snprintf(args[t].base, sizeof(args[t].base), "%s", base);
        snprintf(args[t].notes, sizeof(args[t].notes), "%s", notes ? notes : "");
        args[t].count = 0;
        pthread_create(&threads[t], NULL, sweep_worker, &args[t]);
    }

    for (int t = 0; t < n_threads; t++)
        pthread_join(threads[t], NULL);

    char sweep_id[64];
    experiment_id(sweep_id, sizeof(sweep_id));
    char sw_path[2048];
    snprintf(sw_path, sizeof(sw_path), "%s/raw_data/%s_SWEEP_sweep.json", base, sweep_id);
    FILE *f = fopen(sw_path, "w");
    if (f) {
        fprintf(f, "{\"sweep_id\":\"%s_SWEEP\",\"n\":%d,\"steps\":%d,\"kappas\":[", sweep_id, N_OSCILLATORS, steps);
        for (int i = 0; i < n_kappas; i++) {
            if (i > 0) fprintf(f, ",");
            fprintf(f, "%.6f", kappas[i]);
        }
        fprintf(f, "]}\n");
        fclose(f);
    }

    free(threads);
    free(args);
}

int main(int argc, char **argv) {
    char result_root[1024];
    snprintf(result_root, sizeof(result_root), "%s/projects/%s/%s", results_root(), PROJECT_DIR, VERSION);
    RESULT_ROOT = result_root;

    enum { MODE_SINGLE, MODE_SWEEP } mode = MODE_SWEEP;
    double kappa = 1.0;
    double kappa_lo = 0.0, kappa_hi = 2.0;
    int steps = 10000;
    int n_kappas = 21;
    uint64_t seed = 0;
    char notes[256] = "";
    int n_threads = 1;

    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "--mode") == 0 && i + 1 < argc) {
            if (strcmp(argv[++i], "single") == 0) mode = MODE_SINGLE;
        } else if (strcmp(argv[i], "--kappa") == 0 && i + 1 < argc) {
            kappa = atof(argv[++i]);
        } else if (strcmp(argv[i], "--kappas") == 0 && i + 2 < argc) {
            kappa_lo = atof(argv[++i]);
            kappa_hi = atof(argv[++i]);
        } else if (strcmp(argv[i], "--steps") == 0 && i + 1 < argc) {
            steps = atoi(argv[++i]);
        } else if (strcmp(argv[i], "--n-kappas") == 0 && i + 1 < argc) {
            n_kappas = atoi(argv[++i]);
        } else if (strcmp(argv[i], "--seed") == 0 && i + 1 < argc) {
            seed = (uint64_t)atol(argv[++i]);
        } else if (strcmp(argv[i], "--notes") == 0 && i + 1 < argc) {
            strncpy(notes, argv[++i], sizeof(notes) - 1);
        } else if (strcmp(argv[i], "--threads") == 0 && i + 1 < argc) {
            n_threads = atoi(argv[++i]);
        } else if (strcmp(argv[i], "--help") == 0 || strcmp(argv[i], "-h") == 0) {
            printf("Kuramoto %d-oscillator C simulation with pthreads\n", N_OSCILLATORS);
            printf("Usage: %s [options]\n", argv[0]);
            printf("  --mode single|sweep   (default: sweep)\n");
            printf("  --kappa K             coupling for single mode (default: 1.0)\n");
            printf("  --kappas LO HI        sweep range (default: 0.0 2.0)\n");
            printf("  --steps N             simulation steps (default: 10000)\n");
            printf("  --n-kappas N          sweep points (default: 21)\n");
            printf("  --seed N              RNG seed\n");
            printf("  --notes STR           experiment notes\n");
            printf("  --threads N           parallel sweep threads (default: 1)\n");
            printf("  --help                this message\n");
            return 0;
        }
    }

    if (seed == 0) seed = (uint64_t)time(NULL) % 100000ULL;
    n_threads = n_threads < 1 ? 1 : n_threads;

    ensure_dirs(RESULT_ROOT);

    double omega[N_OSCILLATORS];
    generate_omegas(omega, N_OSCILLATORS, BASE_FREQ, FREQ_SPREAD, seed);

    if (mode == MODE_SINGLE) {
        char eid[64];
        experiment_id(eid, sizeof(eid));
        char keid[128];
        snprintf(keid, sizeof(keid), "%s_K%.3f", eid, kappa);

        KuramotoResult *res = run_kuramoto(kappa, steps, omega, N_OSCILLATORS, seed);
        printf("  R_final=%.6f  R_mean=%.6f  R_std=%.6f\n",
               res->R_final, res->R_mean, res->R_std);
        save_json_result(res, keid, RESULT_ROOT);
        log_experiment(res, keid, RESULT_ROOT, notes);
        free_result(res);
    } else {
        double *kappas = calloc(n_kappas, sizeof(double));
        for (int i = 0; i < n_kappas; i++)
            kappas[i] = kappa_lo + (kappa_hi - kappa_lo) * i / (n_kappas - 1);
        sweep_kappas(kappas, n_kappas, steps, seed, notes, n_threads);
        free(kappas);
    }

    return 0;
}
