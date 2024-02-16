from typing import Optional

import discord

from .bot_basics import bot
from .errors import GameEnd
from .f_database import FACTION_FEATURES
from .postacie import give_faction
from .utility import send_to_manitou, get_town_channel, get_manitou_notebook


class Statue:
    def __init__(self):
        self.holder: Optional[discord.Member] = None
        self.faction_holder = FACTION_FEATURES['START_WITH_STATUE']
        self.planted = False
        self.last_change = -1
        self.followed = {}

    def follow(self, author, member):
        self.followed[author] = member

    def unfollow(self, author):
        try:
            del self.followed[author]
        except KeyError:
            pass

    async def if_followed(self, member):
        for auth, mem in self.followed.items():
            if mem == member and member != self.holder:
                self.last_change = bot.game.day_num
                self.planted = False
                self.holder = auth
                role = bot.game.player_map[auth].role
                faction = give_faction(role)
                self.faction_holder = faction
                c = "{} przejmuje(-ą) posążek w wyniku śledzenia".format(bot.game.player_map[auth].role)
                await send_to_manitou(c)
                await get_manitou_notebook().send(c)
                return c[:-19]
        return False

    async def plant(self, member):
        f = await self.if_followed(member)
        if not f:
            self.planted = True
            self.holder = member
        else:
            bot.game.nights[-1].output += f

    async def unplant(self, member):
        f = await self.if_followed(member)
        if not f:
            self.planted = False
            self.holder = member
        else:
            bot.game.nights[-1].output += f

    async def manitou_plant(self, member):
        prev = self.holder
        self.holder = member
        self.planted = True
        await bot.game.panel.statue_change(prev, member, self.faction_holder, planted=True)

    async def give(self, member):
        """For manitou giving
        """
        prev = self.holder
        self.holder = member
        self.planted = False
        role = bot.game.player_map[member].role
        faction = give_faction(role)
        self.faction_holder = faction
        await bot.game.panel.statue_change(prev, member, faction)

    def day_search(self, member):
        if self.holder == member:
            raise GameEnd("**{}** został(a) przeszukany(-a) i ma posążek".format(member.display_name), "Miasto")
        else:
            return "**{}** nie ma posążka".format(member.display_name)

    async def search(self, author, role, member, info=True):
        if self.holder == member:
            f = await self.if_followed(author)
            if not f:
                self.last_change = bot.game.day_num
                c = "{} przejmuje posążek".format(role)
                await send_to_manitou(c)
                await get_manitou_notebook().send(c)
                bot.game.nights[-1].output = c
                self.holder = author
                faction = give_faction(role)
                self.faction_holder = faction
                self.planted = False
                return "Przejmujesz posążek"
            else:
                bot.game.nights[-1].output = f
                return "Przejmujesz posążek i go tracisz"
        if info:
            c = "{} nie przejmuje posążka".format(role)
            await send_to_manitou(c)
            await get_manitou_notebook().send(c)
            if not bot.game.nights[-1].output:
                bot.game.nights[-1].output += c
        return "Nie przejmujesz posążka"

    async def special_search(self, author, role, member, info=True):
        if self.holder == member:
            f = await self.if_followed(author)
            if not f:
                self.last_change = bot.game.day_num
                c = "{} przejmuje posążek".format(role)
                await send_to_manitou(c)
                await get_manitou_notebook().send(c)
                await get_town_channel().send(c)
                self.holder = author
                faction = give_faction(role)
                self.faction_holder = faction
                self.planted = False
                return "Przejmujesz posążek"
            else:
                await get_town_channel().send(f)
                return "Przejmujesz posążek i go tracisz"
        if info:
            c = "{} nie przejmuje posążka".format(role)
            await send_to_manitou(c)
            await get_manitou_notebook().send(c)
            await get_town_channel().send(c)
            return "Nie przejmujesz posążka"

    async def present(self, member, role):
        f = await self.if_followed(member)
        if not f:
            c = "{} przejmuje posążek".format(role)
            await send_to_manitou(c)
            self.holder = member
            self.planted = False
            faction = give_faction(role)
            self.faction_holder = faction
            bot.game.nights[-1].output = "{} przejmuje(-ą) posążek".format(faction)
        else:
            bot.game.nights[-1].output = f

    async def faction_search(self, faction, member, info=True):
        if self.holder == member:
            self.last_change = bot.game.day_num
            c = "{} przejmuje(-ą) posążek".format(faction)
            await send_to_manitou(c)
            await get_manitou_notebook().send(c)
            await get_town_channel().send(c)
            self.planted = False
            self.faction_holder = faction
            self.holder = None
            return "Przejmujecie posążek"
        if info:
            c = "{} nie przejmuje(-ą) posążka".format(faction)
            await send_to_manitou(c)
            await get_manitou_notebook().send(c)
            await get_town_channel().send(c)
            return "Nie przejmujecie posążka"

    async def change_holder(self, member):
        f = await self.if_followed(member)
        if not f:
            self.holder = member
        else:
            await get_town_channel().send(f)
