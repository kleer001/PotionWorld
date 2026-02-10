import sys
from pathlib import Path

# Ensure project root is on path for ESENS_Parser import
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import arcade

from grammar_mvp.views import SCREEN_HEIGHT, SCREEN_WIDTH, BattleView

SCREEN_TITLE = "Potion Primer"


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.show_view(BattleView())
    arcade.run()


if __name__ == "__main__":
    main()
