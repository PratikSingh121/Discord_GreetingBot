import os
import discord
from discord.ext import commands
import asyncio
import pyttsx3
from config.data import target, token_id


TOKEN = token_id

client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_ready():
    print('Bot is up and running.')


@client.event
async def on_voice_state_update(member, before, after):
  if not before.channel and after.channel and member.id == target:
    print(f'{member} has joined the vc - {after.channel} :: {after.channel.id}')
    vc = await member.voice.channel.connect()
    vc.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe",source = 'marathi_long.mp3'), after=lambda e: print('done', e))
    while vc.is_playing():
        await asyncio.sleep(1)
    else:
        while vc.is_playing():
            break
        else:
            await vc.disconnect() 

stor = None
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!kirito'):
        global stor
        flag = 1
        if stor==None:
            vc = await message.author.voice.channel.connect()

        else:
            flag = 0
            vc = stor
        vc.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe",source = 'play.mp3'), after=lambda e: print('done', e))
        if flag:
            while vc.is_playing():
                await asyncio.sleep(1)
            else:
                while vc.is_playing():
                    break
                else:
                    await vc.disconnect()

    if message.content.startswith('!say'):
        try:
            vc2 = await message.author.voice.channel.connect()
            # global stor
            stor = vc2
        except:
            pass
        msg = (' '.join(message.content.split()[1:]))
        engine = pyttsx3.init()
        engine.setProperty('rate', 155)
        engine.setProperty('voice', engine.getProperty('voices')[1].id)
        engine.save_to_file(msg, 'temp.mp3')
        engine.runAndWait()
        engine.stop() 
        stor.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe",source = 'temp.mp3'), after=lambda e: print('done', e))

    if message.content.startswith('!byebye'):
        if message.content == '!byebye':
            if stor!=None:
                await stor.disconnect()
                stor = None
            else:
                await message.channel.send('Not in a Voice Channel Bro :)')
    
        if message.content == '!byebyeline':
            if stor!=None:
                stor.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe",source = 'exit.mp3'), after=lambda e: print('done', e))
                while stor.is_playing():
                    await asyncio.sleep(1)
                else:
                    while stor.is_playing():
                        break
                    else:
                        await stor.disconnect()
                stor = None
            else:
                await message.channel.send('Not in a Voice Channel Bro :)')

    if message.content == ('!sing'):
        if stor==None:
            stor = await message.author.voice.channel.connect()  
            stor.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe",source = 'sing.mp3'), after=lambda e: print('done', e))          
            while stor.is_playing():
                await asyncio.sleep(1)
            else:
                while stor.is_playing():
                    break
                else:
                    await stor.disconnect()
                stor = None 
        else:
            stor.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe",source = 'sing.mp3'), after=lambda e: print('done', e))          


client.run(TOKEN)