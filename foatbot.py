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
        "You sure do love yourself, literally.",
        "I LOVE MYSELF"
    ],
    "goon": [
        "Experiencing post-nut clarity.",
        "IM COMMMING!!!!!!!!!!!!!!",
        ":eggplant: :stuck_out_tongue:"
    ]
}

goon_specific_data = {
    "level_milestones": [5, 10, 15, 20, 25, 30],
    "milestone_titles": [
        {
            "title": "Potential Gooner"
        },
        {
            "title": "Amateur Gooner"
        },
        {
            "title": "Average Gooner"
        },
        {
            "title": "Experienced Gooner"
        },
        {
            "title": "Freaky"
        },
        {
            "title": "King of the Freaks"
        }
    ],
    "gifs": [
        "https://media.tenor.com/2UqiZdxuRvcAAAAC/fox-girl-anime-girl.gif",
        "https://media.tenor.com/4j--36pffcEAAAAd/anis-euphie.gif",
        "https://media.tenor.com/dCBeOkxsWdoAAAAd/tiredness.gif"
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
        data_handler.init_user(ctx.user.id)
    user_raw_data = data_handler.data['users'][ctx.user.id]
    user_data = user_raw_data['goon']
    goon_desc = f"{ctx.user.mention} ***gooned to*** {user.mention}!"
    flavor_text = flavor_texts['goon'][random.randrange(0, len(flavor_texts['goon']))]
    user_data['total_count'] += 1
    exp_gained = round(data_handler.data['server']['goon_exp_gain'] * data_handler.data['server']['goon_exp_gain_multiplier'])
    if user.id == ctx.user.id:
        exp_gained = round(exp_gained * data_handler.data['server']['goon_self_goon_multiplier'])
        flavor_text = flavor_texts['self_goon'][random.randrange(0, len(flavor_texts['self_goon']))]
    for m in user_data['effects']['exp_multipliers']:
        exp_gained += round(exp_gained * m)
    goon_desc += f"\n\n*{flavor_text}*"
    user_data['exp'] += exp_gained
    user_data['goon_history'].append({
        "time": round(datetime.datetime.now().timestamp()),
        "partner": user.id
    })
    if user.id not in user_data['stats']['partners'].keys():
        user_data['stats']['partners'][user.id] = 1
    else:
        user_data['stats']['partners'][user.id] += 1
    if user_data['exp'] >= user_data['exp_next']:
        user_data['level'] += 1
        user_data['exp'] = user_data['exp'] - user_data['exp_next']
        user_data['exp_next'] = round(user_data['exp_next'] * data_handler.data['server']['goon_exp_next_multiplier'])
        goon_desc += f"\n\n**:fire: You leveled up! (LV {user_data['level'] - 1} -> {user_data['level']})**"
    if user_data['level'] in goon_specific_data['level_milestones']:
        new_title = goon_specific_data['milestone_titles'][goon_specific_data['level_milestones'].index(user_data['level'])]['title']
        goon_desc += f"\n\nNew level milestone reached (LV {user_data['level']})!\nYour title has been changed from {user_data['title']} -> {new_title}"
        user_data['title'] = new_title
    fancy_embed = interactions.Embed(title="Gooned!",
                                     description=goon_desc,
                                     footer=f"LV: {user_data['level']} | EXP: {user_data['exp']} (next: {user_data['exp_next']}) | {user_data['title']}",
                                     images=[goon_specific_data['gifs'][random.randrange(0, len(goon_specific_data['gifs']))]])
    data_handler.data['users'][ctx.user.id] = user_raw_data
    data_handler.write_to_disk()
    user_raw_data = {}
    user_data = {}
    await ctx.send(embed=fancy_embed)

if __name__ == '__main__':
    bot.start(config['token'])