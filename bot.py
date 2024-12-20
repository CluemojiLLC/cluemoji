
import discord
from discord.ext import commands, tasks
import random
from dotenv import load_dotenv
import os
import asyncio
import json

# Load .env file for secure bot token storage
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Define intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

# Initialize the bot
bot = commands.Bot(command_prefix="!", intents=intents)

# Predefined puzzles (Movies only, with genres)
puzzles = [
    {"emoji": "🚢💔🌊🎻🎥❄", "answer": "Titanic", "genre": "Romance/Drama"},
    {"emoji": "🔪📽👩‍🎤👊🎯🩸", "answer": "Kill Bill", "genre": "Action/Thriller"},
    {"emoji": "👠💖👱‍♀🛍🏡🎀", "answer": "Barbie", "genre": "Comedy/Adventure"},
    {"emoji": "☢💥🎩📖🧪🕰", "answer": "Oppenheimer", "genre": "Historical/Drama"},
    {"emoji": "⚔🏟👑🩸🎥🔥", "answer": "Gladiator", "genre": "Action/Drama"},
    {"emoji": "💍🌋🧙‍♂🗡🧝📜", "answer": "Lord of the Rings", "genre": "Fantasy/Adventure"},
    {"emoji": "🎶✨👠🎭🧙‍♀🌪", "answer": "Wicked", "genre": "Musical/Fantasy"},
    {"emoji": "🩰🎭🌆🩸🎶💄", "answer": "Chicago", "genre": "Musical/Drama"},
    {"emoji": "🦁🐧🦓🦒🚢🌴", "answer": "Madagascar", "genre": "Animation/Comedy"},
    {"emoji": "👹🧅🐴🐲🏰👑", "answer": "Shrek", "genre": "Animation/Comedy"},
    {"emoji": "🤖🌿📚🔍🌌🏞", "answer": "Wild Robot", "genre": "Sci-Fi/Adventure"},
    {"emoji": "🕷🧑🗼🕸🏙🎥", "answer": "Spiderman", "genre": "Action/Adventure"},
    {"emoji": "✒📝🎓📖🧑‍🏫🌟", "answer": "Dead Poets Society", "genre": "Drama"},
    {"emoji": "🤖❤📱🛋🏙🎥", "answer": "Her", "genre": "Romance/Sci-Fi"},
    {"emoji": "🏨🎨🛎🎩🎥🗝", "answer": "The Grand Budapest Hotel", "genre": "Comedy/Drama"},
    {"emoji": "🔪🎥🎭👩‍🎤🩸💃", "answer": "Pearl", "genre": "Horror/Thriller"},
    {"emoji": "🌌🌀💫🧪🎭👩‍👩‍👧‍👦", "answer": "Everything Everywhere All at Once", "genre": "Sci-Fi/Adventure"},
    {"emoji": "🌌🧝🌳🌀🏹💙", "answer": "Avatar", "genre": "Sci-Fi/Adventure"},
    {"emoji": "🎭💣🎩🗡🎥⚔", "answer": "V for Vendetta", "genre": "Action/Thriller"},
    {"emoji": "🐱👢🗡🐁🎭🐉", "answer": "Puss in Boots", "genre": "Animation/Adventure"},
    {"emoji": "🐉🎓🗡🌌🎥🔥", "answer": "How to Train Your Dragon", "genre": "Animation/Adventure"},
    {"emoji": "🦊🚔🌆🗞🎥🦓", "answer": "Zootopia", "genre": "Animation/Comedy"},
    {"emoji": "💀🎸🎨🌌🕯🧑‍🎤", "answer": "Coco", "genre": "Animation/Musical"},
    {"emoji": "💪👨‍👩‍👧‍👦🦸‍♂🌆🎥🔥", "answer": "The Incredibles", "genre": "Animation/Action"},
    {"emoji": "🐭🍳👨‍🍳🧀🎥🎶", "answer": "Ratatouille", "genre": "Animation/Comedy"},
    {"emoji": "🐼🥋🐉🛡🎥🔥", "answer": "Kung Fu Panda", "genre": "Animation/Action"},
    {"emoji": "🐟🔍🌊🏝🎥✨", "answer": "Finding Nemo", "genre": "Animation/Adventure"},
    {"emoji": "🦣❄⛄🍑🎥🌌", "answer": "Ice Age", "genre": "Animation/Adventure"},
    {"emoji": "😄🧠💡🏠🎥🌈", "answer": "Inside Out", "genre": "Animation/Adventure"},
    {"emoji": "🎈🏠👴👦🎥🌌", "answer": "Up", "genre": "Animation/Adventure"},
    {"emoji": "🐓🌌🛸🥚🎥✨", "answer": "Chicken Little", "genre": "Animation/Comedy"},
    {"emoji": "👑🦙🏔🧞‍♂🎥🌌", "answer": "The Emperor's New Groove", "genre": "Animation/Comedy"},
    {"emoji": "⚡🏛🗡👑🎥🔥", "answer": "Hercules", "genre": "Animation/Fantasy"},
    {"emoji": "🚗🏎🛣⛽🎥🏁", "answer": "Cars", "genre": "Animation/Comedy"},
    {"emoji": "🌧🍝🍔📖🎥✨", "answer": "Cloudy with a Chance of Meatballs", "genre": "Animation/Comedy"},
    {"emoji": "💀👰🕯🏰🎥🖤", "answer": "Corpse Bride", "genre": "Animation/Fantasy"},
    {"emoji": "👻🍹🎤📸🎥🧟‍♂", "answer": "Beetlejuice", "genre": "Comedy/Fantasy"},
    {"emoji": "🎀👧🧵🌌🎥🖤", "answer": "Coraline", "genre": "Animation/Fantasy"},
    {"emoji": "🧛‍♂🏠🦇🎩🎥🖤", "answer": "The Addams Family", "genre": "Comedy/Horror"},
    {"emoji": "👑🐾❄️🕯️🏰", "answer": "Anastasia", "genre": "Animation/Adventure"},
    {"emoji": "🏜️💨🌟🪐📖", "answer": "Dune", "genre": "Sci-Fi/Adventure"},
    {"emoji": "👸🏻🦎🌟🎨🏰", "answer": "Tangled", "genre": "Animation/Fantasy"},
    {"emoji": "🦌🌲🍂🦉💔", "answer": "Bambi", "genre": "Animation/Drama"},
    {"emoji": "🍎🪞🏰🌳👸", "answer": "Snow White", "genre": "Animation/Fantasy"},
    {"emoji": "🦁👑🌅🪔🐾", "answer": "The Lion King", "genre": "Animation/Drama"},
    {"emoji": "🐘🎪🎠🎩🪕", "answer": "Dumbo", "genre": "Animation/Adventure"},
    {"emoji": "🧝🌌🗡️🎠🚤", "answer": "Peter Pan", "genre": "Animation/Fantasy"},
    {"emoji": "🤥👃🐋🪵🎭", "answer": "Pinocchio", "genre": "Animation/Fantasy"},
    {"emoji": "👠🎃🕰️👸🏰", "answer": "Cinderella", "genre": "Animation/Fantasy"},
    {"emoji": "🐻🍯🎈🏡🍂", "answer": "Winnie the Pooh", "genre": "Animation/Family"},
    {"emoji": "🧞‍♂️🏺🐒🏰🌴", "answer": "Aladdin", "genre": "Animation/Adventure"},
    {"emoji": "🤠🚀🧸👦👩‍👩‍👦", "answer": "Toy Story", "genre": "Animation/Comedy"},
    {"emoji": "🛶🌲☀️💔🧑‍🤝‍🧑", "answer": "Pocahontas", "genre": "Animation/Adventure"},
    {"emoji": "🦍🌴🍃💪🌞", "answer": "Tarzan", "genre": "Animation/Adventure"},
    {"emoji": "🐒🐍🌴🪘🧔", "answer": "Jungle Book", "genre": "Animation/Adventure"},
    {"emoji": "👸🐸🎹🎷🕯️", "answer": "The Princess and the Frog", "genre": "Animation/Adventure"},
    {"emoji": "🤖🌌🪐💌🌱", "answer": "Wall-E", "genre": "Animation/Sci-Fi"},
    {"emoji": "🔍🕰️👨‍🔬👩‍👦👾", "answer": "Meet the Robinsons", "genre": "Animation/Adventure"},
    {"emoji": "🐻❄️🏔️🌄🧡", "answer": "Brother Bear", "genre": "Animation/Drama"},
    {"emoji": "🎤🎸🎵⛺💖", "answer": "Camp Rock", "genre": "Musical/Drama"},
    {"emoji": "🎸🎷🎵📚🏫", "answer": "Lemonade Mouth", "genre": "Musical/Drama"},
    {"emoji": "💍📖🕵️‍♀️❓🩸", "answer": "Gone Girl", "genre": "Mystery/Thriller"},
    {"emoji": "👛🐩📚⚖️💼", "answer": "Legally Blonde", "genre": "Comedy"},
    {"emoji": "🎨👩‍🎓👩‍👧🌹🌆", "answer": "Lady Bird", "genre": "Drama"},
    {"emoji": "🕶️🚗💣🔫🤵", "answer": "James Bond", "genre": "Action/Thriller"},
    {"emoji": "💻🕶️🔮🔗⏳", "answer": "Matrix", "genre": "Sci-Fi/Action"},
    {"emoji": "🎩🍸🎭💸🌟", "answer": "The Great Gatsby", "genre": "Drama/Romance"},
    {"emoji": "💌📖🌅💑🎐", "answer": "The Notebook", "genre": "Romance/Drama"},
    {"emoji": "👠👗👑📚🐀", "answer": "Mean Girls", "genre": "Comedy"},
    {"emoji": "👽🛸🧒🌲🚲", "answer": "E.T.", "genre": "Sci-Fi/Adventure"},
    {"emoji": "⚡🔨🌈🕶️👑", "answer": "Thor", "genre": "Action/Adventure"},
    {"emoji": "🦸‍♂️🛡️🌍🔴💚", "answer": "Avengers", "genre": "Action/Adventure"},
    {"emoji": "🤖🔧🔥🦸‍♂️💼", "answer": "Ironman", "genre": "Action/Sci-Fi"},
    {"emoji": "👛🎩💰🎲🚪", "answer": "Ocean's 8", "genre": "Heist/Comedy"},
    {"emoji": "🛸🗼🌧️🔮📡", "answer": "Arrival", "genre": "Sci-Fi/Drama"},
    {"emoji": "⚗️🧪👨‍🔬🎭📉", "answer": "The Substance", "genre": "Drama/Thriller"},
    {"emoji": "🧜‍♂️🌊⚓🏛️🐟", "answer": "Aquaman", "genre": "Action/Adventure"},
    {"emoji": "🐱🍕🛋️📺📚", "answer": "Garfield", "genre": "Comedy"},
    {"emoji": "👾🏢🔑🚪🎩", "answer": "Monsters Inc", "genre": "Animation/Comedy"},
    {"emoji": "🏹👑🗻🧝‍♀️🔥", "answer": "Brave", "genre": "Animation/Adventure"},
    {"emoji": "🧱🚀🛠️🤖🎵", "answer": "The Lego Movie", "genre": "Animation/Adventure"},
    {"emoji": "🐜🍂🛠️🏞️🚜", "answer": "A Bug's Life", "genre": "Animation/Adventure"},
    {"emoji": "🧜‍♀️🌊🐟🎶❤️", "answer": "The Little Mermaid", "genre": "Animation/Fantasy"},
    {"emoji": "⚔️🌺🐉🎵🏯", "answer": "Mulan", "genre": "Animation/Fantasy"},
    {"emoji": "❄️☃️👗🎶🕍", "answer": "Frozen", "genre": "Animation/Fantasy"},
    {"emoji": "👸🛌🕯️🌳💔", "answer": "Sleeping Beauty", "genre": "Animation/Fantasy"},
    {"emoji": "🖤🏰🐉🔥🪄", "answer": "Maleficent", "genre": "Fantasy/Adventure"},
    {"emoji": "🌹🐗🏰🎶👸", "answer": "Beauty and the Beast", "genre": "Animation/Fantasy"},
    {"emoji": "🌊🌺🌈🏝️🚤", "answer": "Moana", "genre": "Animation/Adventure"},
    {"emoji": "🤖❤️⚔️🎓🏙️", "answer": "Big Hero 6", "genre": "Animation/Action"},
    {"emoji": "🐶🌺🌴🧪👽", "answer": "Lilo and Stitch", "genre": "Animation/Adventure"},
    {"emoji": "🏹🪙🏰👒🐾", "answer": "Robin Hood", "genre": "Animation/Adventure"},
    {"emoji": "⚔️🩸💣💬🕶️", "answer": "Deadpool", "genre": "Action/Comedy"},
    {"emoji": "🏴‍☠️⚓🌊🔱💰", "answer": "Pirates of the Caribbean", "genre": "Action/Adventure"},
    {"emoji": "👗👜🖤🎨📂", "answer": "The Devil Wears Prada", "genre": "Drama/Comedy"},
    {"emoji": "🚗🏎️🛣️💨🏁", "answer": "Fast and Furious", "genre": "Action"},
    {"emoji": "🩸🧛‍♀️🌲💔🌙", "answer": "Twilight", "genre": "Romance/Fantasy"},
    {"emoji": "🧙‍♂️🪄⚡🏰📜", "answer": "Harry Potter", "genre": "Fantasy/Adventure"},
    {"emoji": "🏹🔥🍞🕊️🏛️", "answer": "The Hunger Games", "genre": "Action/Adventure"},
    {"emoji": "🦁🌌🏰⏳🎩", "answer": "Narnia", "genre": "Fantasy/Adventure"},
    {"emoji": "👗👰👠📅🎉", "answer": "27 Dresses", "genre": "Romantic Comedy"},
    {"emoji": "🌀🐇🎩🕰️🌸", "answer": "Alice in Wonderland", "genre": "Fantasy/Adventure"},
    {"emoji": "🛍️💄💳📚📉", "answer": "Confessions of a Shopaholic", "genre": "Comedy"},
    {"emoji": "💉💊📉🌀💔", "answer": "Requiem for a Dream", "genre": "Drama"},
    {"emoji": "🚂🏴‍☠️💊🎭🍻", "answer": "Trainspotting", "genre": "Drama"},
    {"emoji": "💄🧪🪞💔🎭", "answer": "Death Becomes Her", "genre": "Comedy"},
    {"emoji": "🍫🏭🎩👦👓", "answer": "Charlie and the Chocolate Factory", "genre": "Adventure"},
    {"emoji": "🎄🎁⛪🎩😠", "answer": "The Grinch", "genre": "Animation/Comedy"},
    {"emoji": "🌲🍃💡🎩🐸", "answer": "Lorax", "genre": "Animation/Family"},
    {"emoji": "🎲🐘🐍🏞️🌟", "answer": "Jumanji", "genre": "Adventure/Comedy"}
]

# Leaderboard stored in memory (you can connect it to a database for persistence)
leaderboard = {}

# Current game state
current_puzzle = None
current_channel = None
round_timer = None

def save_leaderboard():
    with open("leaderboard.json", "w") as f:
        json.dump(leaderboard, f)

def load_leaderboard():
    global leaderboard
    if os.path.exists("leaderboard.json"):
        with open("leaderboard.json", "r") as f:
            leaderboard = json.load(f)

# Load leaderboard on startup
load_leaderboard()

# Event: Bot is ready
@bot.event
async def on_ready():
    print(f"{bot.user} is connected and ready to play!")

# Command: Start a game
@bot.command(name="start")
async def start_game(ctx):
    global current_puzzle, current_channel, round_timer

    if current_puzzle is not None:
        await ctx.send("A game is already in progress. Please wait for it to finish!")
        return

    current_channel = ctx.channel
    current_puzzle = random.choice(puzzles)
    await ctx.send(f"🎮 New game started! Guess the movie: {current_puzzle['emoji']}\nType `!hint` for a hint.")

    # Start a timer for the round
    round_timer = bot.loop.create_task(round_timeout(ctx))

async def round_timeout(ctx):
    await asyncio.sleep(30)  # 30 seconds for the round
    global current_puzzle, current_channel, round_timer
    if current_puzzle:
        await ctx.send(f"⏰ Time's up! The correct answer was: {current_puzzle['answer']}\nStarting a new puzzle!")
        current_puzzle = None
        await start_game(ctx)

@bot.command(name="guess")
async def make_guess(ctx, *, guess: str):
    global current_puzzle, current_channel, round_timer

    if ctx.channel != current_channel:
        await ctx.send("There's no active game in this channel. Start a new game with `!start`.")
        return

    if not current_puzzle:
        await ctx.send("There's no active puzzle. Start a new game with `!start`.")
        return

    if guess.lower() == current_puzzle['answer'].lower():
        # Stop the timer
        if round_timer:
            round_timer.cancel()

        # Update leaderboard
        user = ctx.author.name
        leaderboard[user] = leaderboard.get(user, 0) + 1
        save_leaderboard()

        await ctx.send(f"🎉 Correct, {ctx.author.mention}! The answer was: {current_puzzle['answer']}\nYour score: {leaderboard[user]}\nStarting a new puzzle!")
        current_puzzle = None
        await start_game(ctx)
    else:
        await ctx.send("❌ Incorrect! Try again.")

@bot.command(name="hint")
async def give_hint(ctx):
    global current_puzzle

    if not current_puzzle:
        await ctx.send("There's no active puzzle to give a hint for. Start a new game with `!start`.")
        return

    await ctx.send(f"🕵️ Hint: The genre of the movie is **{current_puzzle['genre']}**.")

@bot.command(name="score")
async def show_score(ctx):
    if not leaderboard:
        await ctx.send("🏆 The leaderboard is empty. Be the first to score!")
        return

    sorted_leaderboard = sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)
    leaderboard_message = "\n".join([f"{idx + 1}. {user} - {score} points" for idx, (user, score) in enumerate(sorted_leaderboard)])
    await ctx.send(f"🏆 **Leaderboard:**\n{leaderboard_message}")

@bot.command(name="stop")
async def stop_game(ctx):
    global current_puzzle, current_channel, round_timer

    if current_channel != ctx.channel:
        await ctx.send("There's no active game in this channel to stop.")
        return

    if current_puzzle is None:
        await ctx.send("There's no active game to stop.")
        return

    if round_timer:
        round_timer.cancel()

    current_puzzle = None
    current_channel = None
    await ctx.send("🛑 The current game has been stopped.")

@bot.command(name="reset")
async def reset_scores(ctx):
    global leaderboard

    leaderboard.clear()
    save_leaderboard()
    await ctx.send("🔄 The leaderboard has been reset.")

@bot.command(name="instructions")
async def show_help(ctx):
    help_message = (
        "🎮 **Emoji Pictionary Commands**:\n"
        "`!start` - Start a new game.\n"
        "`!guess <your answer>` - Make a guess.\n"
        "`!hint` - Get a hint for the current puzzle.\n"
        "`!score` - Show the leaderboard.\n"
        "`!stop` - Stop the current game.\n"
        "`!reset` - Reset the leaderboard.\n"
        "`!help` - Show this message.\n"
    )
    await ctx.send(help_message)

bot.run(TOKEN)
