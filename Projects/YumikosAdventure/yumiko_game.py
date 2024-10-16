from engine.game_context import GameContext, in_context
from engine.level_context import LevelContext


class YumikoGame(LevelContext):
    def __init__(self, game_context: GameContext) -> None:
        super().__init__()
        self.game_context = game_context
        self.inventory_visible = True

    @in_context
    def add_coins(self, coins: int) -> None:
        print(f"Adding {coins} coin{'s' if coins > 1 else ''}")
        self.game_context.player.coins += coins

    @in_context
    def set_inventory_visibility(self, visible: bool) -> None:
        self.inventory_visible = visible
