
import os
import sys
from dotenv import load_dotenv, find_dotenv

if find_dotenv():
    load_dotenv(find_dotenv())

_PATH_ = os.path.dirname(os.path.dirname(__file__))
print(_PATH_)

if _PATH_ not in sys.path:
    sys.path.append(_PATH_)
    print(sys.path)
    sys.path.append("src") # fixing path issues


if __name__ == "__main__":
    from conniption_zero import manager
    manager.start()
