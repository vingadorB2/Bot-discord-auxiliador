import discord
from discord.ext import commands
import asyncio
from dotenv import load_dotenv
import os
from functools import partial
# ------------------------------------------------

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='-', intents=intents)



def local_resposta(ctx, mensagem):
    return mensagem.author == ctx.author and mensagem.channel == ctx.channel


async def controle_tempo(ctx, opcoes):
    opcoes = {opcao.lower() for opcao in opcoes}

    while True:
        try:
            cronometro = await bot.wait_for("message", timeout=12, check=partial(local_resposta,ctx))

        except TimeoutError:
            await ctx.send("Tempo esgotado")
            return

        resposta_verificacao = cronometro.content.strip().lower()

        if resposta_verificacao == "sair":
            await ctx.send("Comando cancelado")
            return

        if resposta_verificacao in opcoes:
            return cronometro

        await ctx.send(
            f'Resposta inválida. Digite uma destas opções: '
            f'{", ".join(opcoes)} ou "sair".')

# ------------------------iniciamento-------------------------------

@bot.event
async def on_ready():
    print("Bot online")
    print("Comandos carregados:", [c.name for c in bot.commands])

    for servidor in bot.guilds:
        canal = servidor.system_channel

        if canal is not None:
            await canal.send("Bot ligado!, digite '-ajuda' para informações")

@bot.command()
async def teste(ctx):
    await ctx.send("ligado, digite '-ajuda' para receber instruções")


# ~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-

# Comandos:

#----------------------------------- Ajuda:

@bot.command()
async def ajuda(ctx):
    await ctx.send("""Comandos: \n
    #  -juros: Calcula o valor final de um capital entre juros simples e composto;\n
    #  -porcentagem: ao digitar 'valor', mostrará o percentual de uma fração de um inteiro, ao digitar 'porcentagem', dará o valor da fração da porcentagem desejada;\n
    #  -area: calcula a aréa (até então) do circulo, triangulo e quadrado\n
    #  -ajuda: informações e comandos""")


#----------------------------------------- Juros:

@bot.command()
async def juros(ctx):
    print("ativado: juros")
    await asyncio.sleep(1)
    await ctx.send(f"deseja juros simples ou composto? para isso, digite 'simples' ou 'composto'")

    resposta = await controle_tempo(ctx, ("simples", "composto"))
    if resposta is None:
        return
    resposta_verificacao = resposta.content.strip().lower()

    if resposta_verificacao == "simples":

        await ctx.send("Digite o valor do capital inicial:")
        capital = await bot.wait_for("message", timeout=12, check=partial(local_resposta,ctx))
        await ctx.send("Digite o valor dos juros (em inteiro, ex: 10% = 10; 1% = 1):")
        taxa = await bot.wait_for("message", timeout=12, check=partial(local_resposta,ctx))
        await ctx.send("Digite o tempo desejado (de preferência, anos):")
        tempo = await bot.wait_for("message", timeout=12, check=partial(local_resposta,ctx))

        capital_num = float(capital.content)
        taxa_num = float(taxa.content)
        tempo_num = float(tempo.content)
 
        decimal = taxa_num / 100
        valor = capital_num * (1 + decimal * tempo_num)

        await ctx.send(f'O valor final é {float(valor):.2f}')


    elif resposta_verificacao == 'composto':

        await ctx.send("Digite o valor do capital inicial:")
        capital = await bot.wait_for("message", timeout=12, check=partial(local_resposta,ctx))
        await ctx.send("Digite o valor dos juros (em inteiro, ex: 10% = 10; 1% = 1):")
        taxa = await bot.wait_for("message", timeout=12, check=partial(local_resposta,ctx))
        await ctx.send("Digite o tempo desejado (de preferência, anos):")
        tempo = await bot.wait_for("message", timeout=12, check=partial(local_resposta,ctx))

        capital_num = float(capital.content)
        taxa_num = float(taxa.content)
        tempo_num = float(tempo.content)

        decimal = taxa_num / 100
        valor = capital_num * (1 + decimal)**tempo_num

        await ctx.send(f'O valor final é {float(valor):.2f}')

# ---------------------------------- Porcentagem:

@bot.command()
async def porcentagem(ctx):
    print("Ativado: porcentagem")
    await asyncio.sleep(1)
    await ctx.send(f"""Deseja descobrir o valor de uma porcentagem de um valor [porcentagem], ou quanto de um valor cobre de um total [valor]?: """)


    resposta = await controle_tempo(ctx, ("valor", "porcentagem"))
    if resposta is None:
        return
    resposta_verificacao = resposta.content.strip().lower()


    if resposta_verificacao == 'valor':

        await ctx.send("Digite a parte do total:")
        valor1 = await bot.wait_for("message", timeout=12, check=partial(local_resposta,ctx))
        await ctx.send("Digite o valor total:")
        valor2 = await bot.wait_for("message", timeout=12, check=partial(local_resposta,ctx))

        divisao = float(valor1.content) / float(valor2.content)
        total = divisao * 100

        await ctx.send(f"A porcentagem da parte {valor1.content} em relação ao total de {valor2.content} é de {total:.2f}%.")


    elif resposta_verificacao == 'porcentagem':

        await ctx.send("Digite o valor total:")
        valor = await bot.wait_for("message", timeout=12, check=partial(local_resposta,ctx))
        await ctx.send("Digite a porcentagem que será aplicada (em inteiro: 10% = 10; 1% = 1)")
        porcentagem = await bot.wait_for("message", timeout=12, check=partial(local_resposta,ctx))

        decimal = float(porcentagem.content) / 100
        final = decimal * float(valor.content)

        await ctx.send(f"{porcentagem.content}% de {valor.content} é igual a {final:0.2f}")


# ----------------------------------- area:

@bot.command()
async def areas(ctx):
    print('Ativado: Areas')
    await asyncio.sleep(1)
    await ctx.send("""Opções de áreas:\n
# Quadrado
# Retangulo
# triângulo
# cilindro
# Trapézio
# Circulo
                    
    (OBS: O calculo é a base de figuras em 2 dimenção [2D])""")


    resposta = await controle_tempo(ctx, ("quadrado", "circulo", "triangulo", "triângulo"))
    if resposta is None:
        return
    resposta_verificacao = resposta.content.strip().lower()

    
    if resposta_verificacao == "circulo":

        await ctx.send('Digite o raio do circulo:')
        raio = await bot.wait_for("message", timeout=12, check=partial(local_resposta,ctx))

        valor = 3.1415 * float(raio.content)**2

        await ctx.send(f"A área de um circulo com raio {raio.content} é {valor:.4f}")


    elif resposta_verificacao == 'quadrado':

        await ctx.send('Digite o lado do quadrado:')
        lado = await bot.wait_for("message", timeout=12, check=partial(local_resposta,ctx))

        valor = float(lado.content)**2

        await ctx.send(f"A área de um quadrado com o lado valendo  {lado.content} é de {valor}")


    elif resposta_verificacao == 'triângulo' or resposta_verificacao == 'triangulo':

        await ctx.send('Digite a base do triângulo:')
        base = await bot.wait_for("message", timeout=12, check=partial(local_resposta,ctx))
        await ctx.send('Digite a altura do triângulo:')
        altura = await bot.wait_for("message", timeout=12, check=partial(local_resposta,ctx))

        valor = float(base.content) * float(altura.content) / 2
        
        await ctx.send(f"A área de um triângulo de base {base.content} e altura {altura.content} é de {valor}")


# --------------------------------- tempo:

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


load_dotenv()
bot.run(os.getenv("DISCORD_TOKEN"))
