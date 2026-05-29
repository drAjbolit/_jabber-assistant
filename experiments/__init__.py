# experiments/chatgpt_inspect.py

import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from assistant.cdp import ChromeCDP