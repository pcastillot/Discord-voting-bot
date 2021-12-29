import discord
import asyncio

client = discord.Client()

TOKEN='TOKEN BOT DISCORD' # Actualizar con el token del bot
PORCENTAJE_OK = 0.75 # Porcentaje minimo necesario para validar la solicitud
TIEMPO_VOTACION = 30 # Segundos

# Emojis votacion
EMOJI_A_FAVOR = '👍'         
EMOJI_EN_CONTRA = '👎'

# Prefijo y comandos
PREFIJO = "-"
MUTE = PREFIJO + "mute"     # -mute
UNMUTE = PREFIJO + "unmute" # -unmute
KICK = PREFIJO + "kick"     # -kick


# Funcion para comprobar si dos usuarios estan en el mismo canal de voz
def users_mismo_canal(user1, user2):
    return user1.voice is not None and user2.voice is not None \
            and user1.voice.channel is user2.voice.channel

@client.event
async def on_message(message):
    # Comprobamos que no es el bot quien envio el mensaje
    if message.author == client.user:
        return

    msg = message.content
    
    # Comprobamos que el mensaje empieza por los comandos establecidos para el bot
    if msg.startswith(MUTE) or msg.startswith(KICK) or msg.startswith(UNMUTE):
        # Comprobamos que hay alguien mencionado en el mensaje
        if len(message.mentions) > 0:
            # Creamos el id con el formato necesario para la mención en el mensaje
            id = "<@" + str(message.mentions[0].id) + ">"
        else:
            await message.channel.send("Debes mencionar al usuario")
        
    # MUTEAR
    if msg.startswith(MUTE):
        # Comprobamos que ambos usuarios estan en el mismo canal de voz
        if users_mismo_canal(message.author, message.mentions[0]):
                
            # Mandamos el mensaje, añadimos las reacciones y esperamos a que acabe la votacion
            mensaje = await message.channel.send("@everyone Solicitud para mutear a " + id)
            await mensaje.add_reaction(EMOJI_A_FAVOR)
            await mensaje.add_reaction(EMOJI_EN_CONTRA)
            await asyncio.sleep(TIEMPO_VOTACION)
            
            # Obtenemos el numero de votos y restamos los votos iniciales del bot
            mensaje = await message.channel.fetch_message(mensaje.id)
            reacciones_up = mensaje.reactions[0].count - 1
            reacciones_down = mensaje.reactions[1].count - 1
            total = reacciones_up + reacciones_down
            
            if reacciones_up >= total * PORCENTAJE_OK:
                await message.channel.send("Solicitud para mutear a " + id + " ACEPTADA")
                await message.mentions[0].edit(mute=True)
            else:
                await message.channel.send("Solicitud para mutear a " + id + " RECHAZADA")
        else:
            await message.channel.send("Para hacer una solicitud ambos debeis estar en el mismo canal")

    # DESMUTEAR
    elif msg.startswith(UNMUTE):
        # Comprobamos que ambos usuarios estan en el mismo canal de voz
        if users_mismo_canal(message.author, message.mentions[0]):
                
            # Mandamos el mensaje, añadimos las reacciones y esperamos a que acabe la votacion
            mensaje = await message.channel.send("@everyone Solicitud para desmutear a " + id)
            await mensaje.add_reaction(EMOJI_A_FAVOR)
            await mensaje.add_reaction(EMOJI_EN_CONTRA)
            await asyncio.sleep(TIEMPO_VOTACION)
            
            # Obtenemos el numero de votos y restamos los votos iniciales del bot
            mensaje = await message.channel.fetch_message(mensaje.id)
            reacciones_up = mensaje.reactions[0].count - 1
            reacciones_down = mensaje.reactions[1].count - 1
            total = reacciones_up + reacciones_down
            
            if reacciones_up >= total * PORCENTAJE_OK:
                await message.channel.send("Solicitud para desmutear a " + id + " ACEPTADA")
                await message.mentions[0].edit(mute=False)
            else:
                await message.channel.send("Solicitud para desmutear a " + id + " RECHAZADA")

        else:
            await message.channel.send("Para hacer una solicitud ambos debeis estar en el mismo canal")

    # ECHAR DEL CANAL
    elif msg.startswith(KICK):
        # Comprobamos que ambos usuarios estan en el mismo canal de voz
        if users_mismo_canal(message.author, message.mentions[0]):
            
            # Mandamos el mensaje, añadimos las reacciones y esperamos a que acabe la votacion
            mensaje = await message.channel.send("@everyone Solicitud para desconectar a " + id + " del canal")
            await mensaje.add_reaction(EMOJI_A_FAVOR)
            await mensaje.add_reaction(EMOJI_EN_CONTRA)
            await asyncio.sleep(TIEMPO_VOTACION)
            
            # Obtenemos el numero de votos y restamos los votos iniciales del bot
            mensaje = await message.channel.fetch_message(mensaje.id)
            reacciones_up = mensaje.reactions[0].count - 1
            reacciones_down = mensaje.reactions[1].count - 1
            total = reacciones_up + reacciones_down
            
            if reacciones_up >= total * PORCENTAJE_OK:
                await message.channel.send("Solicitud para desconectar a " + id + " ACEPTADA")
                await message.mentions[0].edit(voice_channel=None)
            else:
                await message.channel.send("Solicitud para desconectar a " + id + " RECHAZADA")

        else:
            await message.channel.send("Para hacer una solicitud ambos debeis estar en el mismo canal")
            
    # AYUDA
    elif msg.startswith(HELP):
        await message.channel.send(MUTE + " @usuario : Mutear en el canal de voz al user mencionado\n" +
                                   UNMUTE + " @usuario : Desmutear en el canal de voz al user mencionado\n" +
                                   KICK + " @usuario : Echar del canal de voz al user mencionado")

client.run(TOKEN)