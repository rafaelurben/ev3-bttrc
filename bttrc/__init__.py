#!/usr/bin/env python3
#
# Back To The Roots Communication
#
# 2020 - Rafael Urben
#

import os as _os
from .chat import Chat

if not _os.getenv("EV3_PC", False):
    print("[BTTRC] - Lade Module...")
    from .morse import Morse
    from .printer import Printer

