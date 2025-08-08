import json
import datetime
import interactions
import random
from logger import logger
from data.impl import basic

config = json.load(open("config.json"))

data_handler = basic.BasicDataHandler("storage")

bot = interactions.Client(intents=interactions.Intents.DEFAULT)

flavor_texts = {
    "self_goon": [
        "You sure do love yourself, literally."
    ],
    "goon": [
        "There's supposed to be a random flavor text here, but instead you ran into this placeholder text lol",
        "Experiencing post-nut clarity."
    ]
}

@interactions.listen()
async def on_ready():
    logger.info("bot is ready!")

@interactions.slash_command(name="goon",
                            description="Goon to someone",
                            scopes=[config['server_id']])
@interactions.slash_option(name="user",
                           description="User to goon to",
                           required=True,
                           opt_type=interactions.OptionType.USER)
async def goon_command(ctx: interactions.SlashContext, user: interactions.Member):
    logger.info(f"/goon invoked by {ctx.user.id} ({ctx.user.display_name})")
    if not ctx.user.id in data_handler.data['users'].keys():
        logger.verbose(f"creating new /goon data for {ctx.user.id}")
        data_handler.init_user(ctx.user.id)
    user_raw_data = data_handler.data['users'][ctx.user.id]
    user_data = user_raw_data['goon']
    goon_desc = f"{ctx.user.mention} ***gooned to*** {user.mention}!"
    flavor_text = flavor_texts['goon'][random.randrange(0, len(flavor_texts['goon']))]
    user_data['total_count'] += 1
    exp_gained = round(data_handler.data['server']['goon_exp_gain'] * user_data['exp_gain_multiplier'])
    if user.id == ctx.user.id:
        exp_gained = round(exp_gained / data_handler.data['server']['goon_self_goon_divisor'])
        flavor_text = flavor_texts['self_goon'][random.randrange(0, len(flavor_texts['self_goon']))]
    goon_desc += f"\n\n*{flavor_text}*"
    user_data['exp'] += exp_gained
    user_data['goon_history'].append({
        "time": round(datetime.datetime.now().timestamp()),
        "partner": user.id
    })
    if user_data['exp'] >= user_data['exp_next']:
        user_data['level'] += 1
        user_data['exp'] = user_data['exp'] - user_data['exp_next']
        user_data['exp_next'] = round(user_data['exp_next'] * data_handler.data['server']['goon_exp_next_multiplier'])
        goon_desc += f"\n\n**You leveled up! (LV {user_data['level'] - 1} -> {user_data['level']})**"
    fancy_embed = interactions.Embed(title="Gooned!",
                                     description=goon_desc,
                                     footer=f"LV: {user_data['level']} | EXP: {user_data['exp']} (next: {user_data['exp_next']})")
    data_handler.data['users'][ctx.user.id] = user_raw_data
    data_handler.write_to_disk()
    user_raw_data = {}
    user_data = {}
    await ctx.send(embed=fancy_embed)

if __name__ == '__main__':
    bot.start(config['token'])