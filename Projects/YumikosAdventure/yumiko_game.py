import math

from typing import Union, Optional, ChainMap, Sized, Mapping, Iterator

import time
from pygame.font import Font

import pygame
from engine.level import Level
from engine.tmx import TiledObject
from game.top_down_game_context import TopDownGameContext
from pygame import Surface, Color, Rect

from engine.game_context import in_context, GameContext

COLOUR_WHITE = pygame.Color("white")
COLOUR_BLACK = pygame.Color("black")
COLOUR_BROWN = pygame.Color("burlywood4")
COLOUR_BROWN_TRANSPARENT = pygame.Color(COLOUR_BROWN.r, COLOUR_BROWN.g, COLOUR_BROWN.b, 128)


def sgn(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    d = a - b
    return -1 if d < 0 else (1 if d > 0 else 0)


class Inventory(Mapping[str, TiledObject], Sized):
    def __init__(self, game_context: GameContext, small_font: Font) -> None:
        self.game_context = game_context
        self.small_font = small_font
        self.dict: dict[str, list[TiledObject]] = {}
        self.entry_images: dict[str, Surface] = {}
        self._free_entry_images: list[Surface] = []
        self.image_size: tuple[int, int] = (32, 32)

    @staticmethod
    def _init_image(image: Surface) -> None:
        image.fill(COLOUR_BROWN_TRANSPARENT)
        # pygame.draw.rect(image, COLOUR_BROWN, image.get_rect().inflate(-2, -2), width=2)
        pygame.draw.rect(image, COLOUR_BROWN, image.get_rect(), width=2)

    def _stamp_object(self, image: Surface, obj: TiledObject) -> Surface:
        tile = self.game_context.level.map.images[obj.gid]
        r = tile.get_rect().copy()
        r.center = image.get_rect().center
        image.blit(tile, r)
        return image

    def _new_image(self) -> Surface:
        if len(self._free_entry_images) > 0:
            image = self._free_entry_images[0]
            del self._free_entry_images[0]
        else:
            image = Surface(self.image_size, pygame.SRCALPHA, 32).convert_alpha()
            self._init_image(image)
        return image

    def set_size(self, size: tuple[int, int]) -> bool:
        changed = False
        if self.image_size[0] != size[0] and self.image_size[1] != size[1]:
            del self._free_entry_images[:]
            changed = True
        self.image_size = size
        return changed

    def count(self, key: str) -> int:
        if key in self.dict:
            return len(self.dict[key])
        return 0

    def __getitem__(self, key: str) -> TiledObject:
        return self.dict[key][0]

    def __setitem__(self, key: str, obj: TiledObject) -> None:
        if key in self.dict:
            self.dict[key].append(obj)
            image = self.entry_images[key]
            image_rect = image.get_rect()
            self._init_image(image)
            self._stamp_object(image, obj)
            text_white = self.small_font.render(str(len(self.dict[key])), True, COLOUR_WHITE).convert_alpha()
            text_black = self.small_font.render(str(len(self.dict[key])), True, COLOUR_BROWN).convert_alpha()
            text_rect = text_white.get_rect()
            image.blit(text_black, (image_rect.right - text_rect.width - 2, image_rect.bottom - text_rect.height - 2))
            image.blit(text_black, (image_rect.right - text_rect.width - 2, image_rect.bottom - text_rect.height))
            image.blit(text_black, (image_rect.right - text_rect.width, image_rect.bottom - text_rect.height - 2))
            image.blit(text_black, (image_rect.right - text_rect.width, image_rect.bottom - text_rect.height))
            image.blit(text_white, (image_rect.right - text_rect.width - 1, image_rect.bottom - text_rect.height - 1))

        else:
            self.dict[key] = [obj]
            image = self._new_image()
            self._stamp_object(image, obj)
            self.entry_images[key] = image

    def __delitem__(self, key: str) -> None:
        if key not in self.dict:
            raise KeyError(key)

        l = self.dict[key]
        del l[0]
        if len(l) == 0:
            del self.dict[key]
            if key in self.entry_images:
                image = self.entry_images[key]
                self._init_image(image)
                self._free_entry_images = image
                del self.entry_images[key]

    def __contains__(self, key: str) -> bool:
        return key in self.dict

    def __len__(self) -> int:
        return len(self.dict)

    def __iter__(self) -> Iterator[str]:
        return iter(self.dict)


class SayThing:
    def __init__(self, text: str, colour: Color = COLOUR_WHITE, expires_in: float = 0) -> None:
        self.text = text
        self.colour = colour
        self.expires_at = time.time() + expires_in
        self.surface: Optional[Surface] = None

    def invalidate(self) -> None:
        self.surface = None

    def is_expired(self) -> bool:
        return False if self.expires_at == 0 else time.time() >= self.expires_at


class YumikoGame(TopDownGameContext):
    def __init__(self, levels: dict[Union[str, int], Level], font: Font, small_font: Font) -> None:
        super().__init__(levels)
        self.font = font
        self.font_height = font.get_linesize()
        self.small_font = small_font
        self.say_spacing = 2
        self.inventory_visible = True
        self.say_things = []
        self._inventory: Inventory = Inventory(self, small_font)
        self.hello = "hello"
        self._add_attribute_name("hello")
        self._inventory_box: Optional[Surface] = None

    def set_level(self, level: Level) -> None:
        super().set_level(level)

        tiled_map = self.level.map

        width = max(tiled_map.images[gid].get_rect().width + 1 for gid in range(tiled_map.maxgid) if tiled_map.images[gid]) + 8
        height = max(tiled_map.images[gid].get_rect().width + 1 for gid in range(tiled_map.maxgid) if tiled_map.images[gid]) + 8

        if not self._inventory_box or width != self._inventory.image_size[0] or height != self._inventory.image_size[1]:
            self._inventory_box = Surface((width, height), pygame.SRCALPHA, 32).convert_alpha()
            # self._inventory_box.set_alpha(128)
            self._inventory_box.fill(COLOUR_BROWN_TRANSPARENT)
            pygame.draw.rect(self._inventory_box, COLOUR_BROWN, self._inventory_box.get_rect().inflate(-2, -2), width=2)

        self._inventory.set_size((width, height))

    def _display_say_things(self, screen: Surface) -> None:
        screen_rect = screen.get_rect()
        line_height = len(self.say_things) + self.say_spacing
        y = screen_rect.height - self.font_height * line_height
        for say_thing in self.say_things:
            if say_thing.surface is None:
                say_thing.surface = Surface((screen_rect.width - 20, self.font_height + line_height), pygame.SRCALPHA, 32).convert_alpha()
                say_thing.surface.fill((0, 0, 0, 0))
                black_text = self.font.render(say_thing.text, True, COLOUR_BLACK).convert_alpha()
                colour_text = self.font.render(say_thing.text, True, say_thing.colour).convert_alpha()
                say_thing.surface.blit(black_text, (0, 0))
                say_thing.surface.blit(black_text, (2, 0))
                say_thing.surface.blit(black_text, (2, 2))
                say_thing.surface.blit(black_text, (0, 2))
                say_thing.surface.blit(black_text, (3, 3))
                say_thing.surface.blit(black_text, (2, 3))
                say_thing.surface.blit(colour_text, (1, 1))
            screen.blit(say_thing.surface, (10, y))
            y += line_height + self.font_height

    def _display_inventory(self, screen: Surface) -> None:
        if len(self._inventory) == 0:
            return

        rect = Rect(screen.get_rect().right - self._inventory.image_size[0], 50, self._inventory.image_size[0], self._inventory.image_size[1])
        for key in self._inventory:
            screen.blit(self._inventory.entry_images[key], rect)
            rect.y += self._inventory.image_size[1]

    def after_map(self, screen: Surface) -> None:
        self._display_say_things(screen)
        self._display_inventory(screen)

    @property
    @in_context
    def tiles_by_name(self) -> ChainMap[str, int]:
        return self.level.map.tiles_by_name

    @in_context
    @property
    def inventory(self) -> Inventory:
        return self._inventory

    @in_context
    def add_coins(self, coins: int) -> None:
        # self.player.coins += coins
        if "coin" in self._inventory:
            coin_obj = self._inventory["coin"]
            for _ in range(coins):
                self._inventory["coin"] = coin_obj

    @in_context
    def set_inventory_visibility(self, visible: bool) -> None:
        self.inventory_visible = visible

    @in_context
    def say(self, text: str, colour: Color = COLOUR_WHITE, expires_in: float = 0.0) -> None:
        self.say_things.append(SayThing(text, colour=colour, expires_in=expires_in))

    @in_context
    def say_once(self, text: str, colour: Color = COLOUR_WHITE, expires_in: float = 0.0) -> None:
        if len(self.say_things) == 0 or self.say_things[-1].text != text:
            self.say_things.append(SayThing(text, colour=colour, expires_in=expires_in))
        elif self.say_things[-1].colour != colour:
            self.say_things[-1].colour = colour
            self.say_things[-1].invalidate()

    @in_context
    def distance_from_player(self, obj: TiledObject) -> float:
        dx = self.player.rect.x - obj.rect.x
        dy = self.player.rect.y - obj.rect.y
        return math.sqrt(dx * dx + dy * dy)

    @in_context
    def move_object_away(self, this: TiledObject, obj: TiledObject) -> None:
        dx = sgn(this.rect.x, obj.rect.x) * max(4, abs(obj.next_rect.x - obj.rect.x))
        dy = sgn(this.rect.y, obj.rect.y) * max(4, abs(obj.next_rect.y - obj.rect.y))
        self.move_object(this, dx, dy)

    @in_context
    def add_object_to_inventory(self, obj: TiledObject) -> None:
        self.remove_object(obj)
        k = obj.name
        self.inventory[k] = obj
        self.prevent_colliding()

    @in_context
    def give_object(self, obj_name: str) -> None:
        for o in self.level.objects:
            if o.name == obj_name:
                self.remove_object(o)
                self.add_object_to_inventory(o)
                return
