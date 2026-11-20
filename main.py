import discord
from discord.ext import commands


# ------------------------------------------------

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='-', intents=intents)

# ------------------------iniciamento-------------------------------

@bot.event
async def on_ready():
    print("Bot online")
    print("Comandos carregados:", [c.name for c in bot.commands])

    for servidor in bot.guilds:
        canal = servidor.system_channel

        if canal is not None:
            await canal.send("Bot ligado!")

@bot.command()
async def teste(ctx):
    await ctx.send("ligado, digite '-ajuda' para receber instruções")

# ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-

# Comandos:

#----------------------------------- Ajuda:


@bot.command()
async def ajuda(ctx):
    await ctx.send("""Comandos: \n
    #  -juros: {valor1 = capital}; {valor2 = juros (em inteiro)}; {valor3 = tempo(em anos)}\n
    #  -porcentagem: {valor1: percentual de...}; {valor2: ... de valor (total)}\n
    #  -area: {valor1: raio}\n
    #  -tempo: {valor1: distancia (em kilometros)}; {valor2: tempo (em horas)}
    #  -ajuda: informações e comandos""")


#------------------------------ porcentagem:


@bot.command()
async def porcentagem(ctx, valor1: float, valor2: float):
    print("ativado: porcentagem")
    resultado = (valor1 * valor2) / 100
    await ctx.send(f"{valor1}% de {valor2} é igual a {resultado:.2f}.")


# ---------------------------------- Juros:


@bot.command()
async def juros(ctx, valor1: float, valor2: float, valor3: float):
    print("ativado: juros")
    montante = (valor1 * (1 + (valor2 / 100) ** valor3)) + valor2 # juros compostos: M = C * (1 + i)^n
    await ctx.send(f"Com capital {valor1} e taxa {valor2}%, o montante é {montante:.2f}.")


# ----------------------------------- area:


@bot.command()
async def area(ctx, valor1: float):
    area = 3.14159 * (valor1 ** 2) # área do círculo: A = π * r²
    await ctx.send(f"A área do círculo com raio {valor1} é {area:.2f}.")


# ---------------------------------- tempo:


@bot.command()
async def tempo(ctx, valor1: float, valor2: float):
    # valor1 = velocidade, valor2 = tempo
    tempo = valor1 / valor2
    await ctx.send(f"A velocidade a se percorrer em distancia de {valor1} kilometros com o tempo de {valor2} é de {tempo:.0f}km/h") 


# -------------------------------------------------------------------------------------------------------------------------

# -------------------------- ERROR:

    
@bot.event
async def on_command_error(ctx, erro):
    if isinstance(erro, commands.CommandNotFound):
        await ctx.send("Comando inválido.")

    elif isinstance(erro, commands.MissingRequiredArgument):
        await ctx.send("Faltam argumentos. Use apenas números.")

    elif isinstance(erro, commands.BadArgument):
        await ctx.send("Você digitou um valor inválido.")

    else:
        await ctx.send("Ocorreu um erro ao executar o comando.")
        print(erro)


bot.run("TOKEN")
