import discord
import time
from discord.ext import commands
import random
import logging
import asyncio
from datetime import timezone
import re



intents = discord.Intents.all() # Подключаем "Разрешения"
intents.message_content = True
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
# Задаём префикс и интенты
bot = commands.Bot(command_prefix='>', intents=intents) 
client = discord.Client(intents=intents)
entry_times = {}
welcume = ['Привет','Приветствую','И тебе привет','q', 'q', 'q', 'qq', 'hello','хай','hi','здарова','дарова','здорова']


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('Грустно прожигаю жизнь, играя в кубики и смотря аниме'), )
    print('I am working')

@bot.command()
async def lol(ctx):
    await ctx.send('kek')
    print('эта часть кода работает 1')


@bot.command()
async def avatar(ctx, member: discord.Member = None):
    if member == None:
        member = ctx.author
    embed = discord.Embed(title= member).set_image(url=member.avatar)
    await ctx.send(embed=embed)
    
@bot.command(pass_context = True)
async def clear(ctx, amount = 1):
    bot_access_ids = [449240332102664212, 699294704252223668] #указывайте тут id пользователей, у кого будет возможность использовать >clear
    if ctx.message.author.id in bot_access_ids:
        await ctx.message.delete()
        await ctx.channel.purge(limit = amount)
        print('Удалено сообщений -',amount)
    else:
        await ctx.send('кек, у тебя мало прав')


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author == bot.user: return
    for i in welcume:
        if i.lower() in message.content.lower():
            try:
                await message.channel.send(random.choice(welcume))
            except:
                pass
            break
        elif re.fullmatch(r'\bку\b', message.content.lower()):
            await message.channel.send(random.choice(welcume))
            break
    if message.author == bot.user: return # если сообщение от бота - игнорируем
    banwords = ["фурри", "furry", "фурей", "фури","fury"] #простой фильтр слов
    for word in banwords:
        if word in message.content.lower():
            try:
                await message.delete()
            except:
                pass
            a = await message.channel.send(f'{message.author.mention}, мы тут фурри не любим!')
            await asyncio.sleep(6)
            await a.delete()
            break

@bot.event
async def on_member_join(member): #Приветствие при вступлении в дискорд сервер
    channel = bot.get_channel(1085870394940067901)#здесь указывайте id нужного канала
    await channel.send(f'>>> ## Привет, {member.mention}, вы попали в странное место, но тут норм вроде\n** Ты создал свой аккаунт: {member.created_at.replace(tzinfo=timezone.utc).strftime('%a, %#d, %B, %Y')} **')
    print(f"{member.name} joined to channel!")         
    
@bot.event 
async def on_member_remove(member): #Аналогично, прощание при выхода из дискорд сервера
    channel = bot.get_channel(1085870394940067901)#здесь указывайте id нужного канала
    await channel.send(f'>>> ## {member.global_name} вышел с сервера')
    
 
    
@bot.event #логирование входов/выходов в голосовые каналы
async def on_voice_state_update(member, before: discord.VoiceState, after: discord.VoiceState):
    channel = bot.get_channel(1256142206578982922)#здесь указывайте id нужного канала
    if before.channel is None and after.channel is not None:
        # Пользователь зашел в канал
        entry_time = time.strftime('%H:%M')
        entry_times[member.id] = entry_time
        await channel.send(f'>>> ### {member.global_name} зашёл в канал {after.channel.mention} в {entry_time}')
    elif after.channel is None and before.channel is not None:
        # Пользователь вышел из канала
        exit_time = time.strftime('%H:%M')
        entry_time = entry_times.pop(member.id, None)  # Извлекаем и удаляем время входа
        if entry_time:
            entry_hour, entry_minute = map(int, entry_time.split(':'))
            exit_hour, exit_minute = map(int, exit_time.split(':'))
            total_hours = exit_hour - entry_hour
            total_minutes = exit_minute - entry_minute
            if total_minutes < 0:
                total_hours -= 1
                total_minutes += 60
            await channel.send(f'>>> ### {member.global_name} вышел из канала {before.channel.mention} в {exit_time}, спустя {total_hours} часа(ов), {total_minutes} минут(ы)')
    elif before.channel != after.channel:
        # Пользователь перешел из одного канала в другой
        transition_time = time.strftime('%H:%M')
        await channel.send(f'>>> ### {member.global_name} перешёл из канала {before.channel.mention} в канал {after.channel.mention} в {transition_time}')

        
@bot.command(pass_context = True) #функция входа бота в голосовой канал в котором находится пользователь    
async def join(ctx):              #>join для подключения бота
    while True:
        await ctx.author.voice.channel.connect()
        await ctx.message.delete()

if 1 == 1:            
    bot.run('token(logger)', log_handler=handler, log_level=logging.DEBUG)