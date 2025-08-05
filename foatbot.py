import json
import interactions

bot = interactions.Client(intents=interactions.Intents.DEFAULT)

@interactions.listen()
async def on_ready():
    print("bot is ready!")

@interactions.slash_command(name="goon",
                            description="Goon to someone")
@interactions.slash_option(name="user",
                           description="User to goon to",
                           required=True,
                           opt_type=interactions.OptionType.USER)
async def goon_command(ctx: interactions.SlashContext, user: interactions.Member):
    await ctx.send(f"{ctx.user.display_name} gooned to {user.display_name}!")

if __name__ == '__main__':
    config = json.load(open("config.json"))
    bot.start(config['token'])