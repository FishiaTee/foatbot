import json
import datetime
import interactions
from data.impl import basic

config = json.load(open("config.json"))

data_handler = basic.BasicDataHandler("storage")

bot = interactions.Client(intents=interactions.Intents.DEFAULT)

@interactions.listen()
async def on_ready():
    print("bot is ready!")

@interactions.slash_command(name="goon",
                            description="Goon to someone",
                            scopes=[config['server_id']])
@interactions.slash_option(name="user",
                           description="User to goon to",
                           required=True,
                           opt_type=interactions.OptionType.USER)
async def goon_command(ctx: interactions.SlashContext, user: interactions.Member):
    if not ctx.user.id in data_handler.data['users'].keys():
        data_handler.init_user(ctx.user.id)
    user_raw_data = data_handler.data['users'][ctx.user.id]
    user_data = user_raw_data['goon']
    goon_desc = f"{ctx.user.mention} ***gooned to*** {user.mention}!"
    user_data['total_count'] += 1
    user_data['exp'] += round(data_handler.data['server']['goon_exp_gain'] * user_data['exp_gain_multiplier'])
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