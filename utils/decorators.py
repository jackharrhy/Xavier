from functools import wraps


def cozy(f):
    """Wraps a discord command in a typing context, and spits out errors on them occuring"""

    @wraps(f)
    async def inner(self, ctx, *args, **kwargs):
        async with ctx.channel.typing():
            try:
                return await f(self, ctx, *args, **kwargs)
            except Exception as e:
                await ctx.send(f"Something is borked!:```{e}```")
                raise e

    return inner
