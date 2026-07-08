# Security & Secrets Management

## Principle

NOEMA stores **zero secrets in source code**. All credentials, API keys, and tokens
are loaded from environment variables at runtime. The system provides a single
loader module (`ciel_secret_loader.py` excluded from version control) that
reads from environment and optionally from `~/.ciel/secrets/`.

## Required Environment Variables

| Variable | Purpose | Required |
|----------|---------|----------|
| `ANTHROPIC_API_KEY` | Claude API access for memory consolidation | No (local mode works without) |
| `CIEL_CONSOLIDATOR_ANTHROPIC_MODEL` | Model override (default: `claude-haiku-4-5-20251001`) | No |
| `CIEL_MEMORIES_PASSWORD` | Access password for memory folder | No (default: `memoriesciel`) |

## Setup

```bash
# Create environment file (never commit!)
cp .env.example .env
# Edit .env with your keys
nano .env

# Source it before running
export $(grep -v '^#' .env | xargs)
```

## Memory Folder Access

The CIEL memories folder (`~/CIEL_memories/`) is protected by a `.access_token`
file containing a simple password. Create it with:

```bash
echo -n "your_password" > ~/CIEL_memories/.access_token
chmod 600 ~/CIEL_memories/.access_token
```

## Public Release Checklist

- [ ] `ciel_secret_loader.py` is in `.gitignore`
- [ ] No API keys in any `.py`, `.json`, `.yaml`, `.md` files
- [ ] No absolute paths referencing `$HOME` or usernames
- [ ] `.env.example` contains placeholder values only
- [ ] `CIEL_memories/` directory is excluded
- [ ] All `.db` and `.h5` files are excluded
