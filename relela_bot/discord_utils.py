import discord
from datetime import datetime

async def send_embed_message(ctx, title, description, image_path=None, color=discord.Color.blue()):
    embed = discord.Embed(title=title, description=description, color=color)
    if image_path:
        image_extension = image_path.split(".")[-1]
        file = discord.File(image_path, filename=f"thumbnail.{image_extension}")
        embed.set_thumbnail(url=f"attachment://thumbnail.{image_extension}")
        await ctx.send(file=file, embed=embed)
    else:
        await ctx.send(embed=embed)

async def send_gpu_usage_embed_message(channel, user):
    title = "GPU Usage Alert"
    description = f"El usuario **{user}** ha comenzado a utilizar una GPU."
    color = discord.Color.orange()
    embed = discord.Embed(title=title, description=description, color=color)
    embed.set_thumbnail(url="attachment://thumbnail.gif")
    embed.set_footer(text=f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    image_path = "./relela_bot/bot_images/bird.gif" 
    file = discord.File(image_path, filename="thumbnail.gif")
    
    await channel.send(file=file, embed=embed)

async def send_gpu_alert_embed_message(channel, user, hours):
    title = "GPU Usage Alert"
    description = f"¿**{user}** aún sigues utilizando la gpu?. Has utilizado las GPU por {round(hours, 3)} horas."
    color = discord.Color.red()
    embed = discord.Embed(title=title, description=description, color=color)
    embed.set_thumbnail(url="attachment://thumbnail.gif")
    embed.set_footer(text=f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    image_path = "./relela_bot/bot_images/check.gif" 
    file = discord.File(image_path, filename="thumbnail.gif")
    
    await channel.send(file=file, embed=embed)

async def send_gpu_not_usage_embed_message(channel, user):
    title = "GPU Usage Alert"
    description = f"El usuario **{user}** ha dejado de utilizar una GPU."
    color = discord.Color.green()
    embed = discord.Embed(title=title, description=description, color=color)
    embed.set_thumbnail(url="attachment://thumbnail.gif")
    embed.set_footer(text=f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    image_path = "./relela_bot/bot_images/finished.gif" 
    file = discord.File(image_path, filename="thumbnail.gif")
    
    await channel.send(file=file, embed=embed)
