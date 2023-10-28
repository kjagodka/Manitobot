from typing import Union
import datetime as dt

import discord
from discord.ext import commands
import pytz

from settings import REFERENCE_TIMEZONE
from .my_checks import poll_channel_only
from .surveys import ankietka, deklaracje, WEEKD, ANKIETKA_PING

from .utility import get_marketer_role, get_admin_role, get_ankietawka_channel, get_ping_poll_role

WEEKD_MAP = {WEEKD[i]: i for i in range(7)}


class Marketing(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.last = {
            'ankietka': None,
            'deklaracje': None
        }

    async def cog_check(self, ctx: commands.Context):
        # TODO: add telemarketer role
        if ctx.author in get_admin_role().members:
            return True
        raise commands.MissingRole(get_marketer_role())

    @commands.command(name='ankietka')
    @poll_channel_only()
    async def survey(self, ctx, start: Union[int, str], koniec: Union[int, str]):
        """Wysyła na kanał #ankietawkowołacz ankietkę na podane dni tygodnia.
        Argumenty start i koniec należy podać jako dwuliterowe skróty dni tygodnia lub ich numery 1 (pn) - 7 (nd).
        """
        if isinstance(start, str):
            start = WEEKD_MAP.get(start.lower())
        else:
            start -= 1
        if isinstance(koniec, str):
            koniec = WEEKD_MAP.get(koniec.lower())
        else:
            koniec -= 1
        if start is None or koniec is None or start < 0 or koniec < 0 or start > 6 or koniec > 6:
            await ctx.send('Niepoprawne argumenty. Użyj pn, wt, śr, cz, pt, sb, nd lub ich numerów 1-7.')
            return

        text, emoji = ankietka(start, koniec, pytz.timezone(REFERENCE_TIMEZONE))

        msg = await get_ankietawka_channel().send(text)
        for e in emoji:
            await msg.add_reaction(e)

    @commands.command(name='deklaracje')
    @poll_channel_only()
    async def declarations(self, ctx, dzien: Union[int, str], *godziny: int):
        """Wysyła na kanał #ankietawkowołacz deklaracje na podany dzień tygodnia.
        Argument `dzien` należy podać jako dwuliterowy skrót dnia tygodnia lub jego numer 1 (pn) - 7 (nd).
        Argument `godziny` należy podać jako godziny rozdzielone spacjami.
        """
        if isinstance(dzien, str):
            dzien = WEEKD_MAP.get(dzien.lower())
        else:
            dzien -= 1
        if dzien is None or dzien < 0 or dzien > 6:
            await ctx.send('Niepoprawny dzień. Użyj pn, wt, śr, cz, pt, sb, nd lub ich numerów 1-7.')
            return
        if not all(0 <= g < 24 for g in godziny):
            await ctx.send('Niepoprawne godziny. Użyj liczb od 0 do 23.')
            return

        text, emoji = deklaracje(dzien, pytz.timezone(REFERENCE_TIMEZONE), godziny)

        msg = await get_ankietawka_channel().send(text)
        for e in emoji:
            await msg.add_reaction(e)

    @staticmethod
    async def _find_ping_in_messages_today(ping: discord.Role) -> bool:
        async for message in get_ankietawka_channel().history(
                after=dt.datetime.now(pytz.timezone(REFERENCE_TIMEZONE)).replace(
                    hour=0, minute=0, second=0, microsecond=0)):
            if ping in message.role_mentions:
                return True
        return False

    @commands.command(disabled=True)
    @poll_channel_only()
    async def ping(self, ctx, ping: str):
        """Wysyła ping podanego typu
        """
        if ping == 'ankietka' or ping == get_ping_poll_role().mention or ping == ANKIETKA_PING:
            if self.last['ankietka'] == dt.date.today() or self._find_ping_in_messages_today(get_ping_poll_role()):
                await ctx.send('Dzisiaj już był ping na ankietkę')
                return
            text = f'{ANKIETKA_PING} {get_ping_poll_role().mention}'
        await ctx.send('Pong!')
