import discord
import random
from discord.ext import commands
import requests

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'Estamos logados como {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Olá! eu sou um bot {bot.user}!')

@bot.command()
async def heh(ctx, count_heh = 15):
    await ctx.send("he" * count_heh)

@bot.command()
async def feio(ctx):
    await ctx.send(f'Esse mlk (dudu) é muito feio kkkkkk')

@bot.command()
async def pokemon(ctx, pokename):
    url = 'https://pokeapi.co/api/v2/pokemon/' + pokename + '/'
    res = requests.get(url)
    data = res.json()
    poke_image = data['sprites']['front_default']
    await ctx.send(f'{poke_image}')

@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)


def classificar_imagem(imagem):
    from keras.models import load_model  # TensorFlow is required for Keras to work
    from PIL import Image, ImageOps # Install pillow instead of PIL
    import numpy as np


    # Disable scientific notation for clarity
    np.set_printoptions(suppress=True)
 

    # Load the model
    model = load_model("keras_Model.h5", compile=False)

    # Load the labels
    class_names = open("labels.txt", "r").readlines()

    # Create the array of the right shape to feed into the keras model
    # The 'length' or number of images you can put into the array is
    # determined by the first position in the shape tuple, in this case 1
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    # Replace this with the path to your image
    image = Image.open(imagem).convert("RGB")
 
    # resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

    # turn the image into a numpy array
    image_array = np.asarray(image)

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

    # Load the image into the array
    data[0] = normalized_image_array

    # Predicts the model
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    # Print prediction and confidence score
    print("Class:", class_name[2:], end="")
    print("Confidence Score:", confidence_score)

    return class_name[2:]
    
@bot.command()
async def receber(ctx):
    if ctx.message.attachments:
        for image in ctx.message.attachments:
            nome_imagem = image.filename
            url_imagem = image.url
            await image.save(f'{nome_imagem}')
            await ctx.send(f'Sua imagem é: {classificar_imagem(nome_imagem)}')
    else:
        await ctx.send('N tem link')

bot.run('SEU TOKEN AQUI')
