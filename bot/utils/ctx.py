from typing import Optional

import discord
from discord.ext.commands import Context

from bot.models.translation import Translation


class CustomContext(Context):
    """Custom context class to provide extra helper methods and multi-language support"""

    def __init__(self, *args, embed_color: discord.Color = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.embed_color = embed_color  # used in send_embed(...) and reply_embed(...)
        self.l: Translation = None  # the translation of the bot text for the current context
        self.failure_reason: Optional[
            str
        ] = None  # failure reason used in some command error handling
        self.custom_error: Optional[Exception] = None

    async def send_embed(self, message: str, *, ignore_exceptions: bool = False) -> None:
        embed = discord.Embed(color=self.embed_color, description=message)

        try:
            await self.send(embed=embed)
        except discord.errors.HTTPException:
            if not ignore_exceptions:
                raise

    async def reply_embed(
        self, message: str, ping: bool = False, *, ignore_exceptions: bool = False
    ) -> None:
        embed = discord.Embed(color=self.embed_color, description=message)

        try:
            await self.reply(embed=embed, mention_author=ping)
        except discord.errors.HTTPException as e:
            if (
                e.code == 50035
            ):  # invalid form body, happens sometimes when the message to reply to can't be found?
                await self.send_embed(message, ignore_exceptions=ignore_exceptions)
            elif not ignore_exceptions:
                raise


Ctx = CustomContext
