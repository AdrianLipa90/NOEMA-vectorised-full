import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from ciel_sot_agent.gh_coupling import main


if __name__ == '__main__':
    raise SystemExit(main())
