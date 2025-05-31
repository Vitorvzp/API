import discord
from discord.ext import commands, tasks
from datetime import datetime, time
import asyncio
import requests
from dotenv import load_dotenv
import os
import pytz
import json

load_dotenv()

# --- Função para obter geo info pelo IP ---
def get_geo_info(ip: str):
    url = f"http://ip-api.com/json/{ip}?fields=status,message,country,regionName,city,lat,lon,isp,query"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        if data['status'] == 'success':
            return {
                "ip": data.get("query"),
                "country": data.get("country"),
                "region": data.get("regionName"),
                "city": data.get("city"),
                "latitude": data.get("lat"),
                "longitude": data.get("lon"),
                "isp": data.get("isp"),
            }
        else:
            return {"error": data.get("message", "Falha ao obter dados")}
    except Exception as e:
        return {"error": str(e)}

# --- Cria o embed do log ---
def create_log_embed(title: str, description: str, ip: str, user_agent: str = None, geo: dict = None) -> discord.Embed:
    embed = discord.Embed(
        title=title,
        description=description,
        color=discord.Color.dark_theme(),
        timestamp=datetime.now()
    )

    embed.add_field(name="🖥️ IP do visitante", value=ip, inline=True)

    if user_agent:
        embed.add_field(name="📱 User Agent", value=user_agent, inline=True)

    if geo and "error" not in geo:
        location = f"{geo['city']}, {geo['region']}, {geo['country']}"
        coords = f"{geo['latitude']}, {geo['longitude']}"
        embed.add_field(name="🌍 Localização", value=location, inline=False)
        embed.add_field(name="🗺️ Coordenadas", value=coords, inline=True)
        embed.add_field(name="🛰️ ISP", value=geo['isp'], inline=True)
    elif geo and "error" in geo:
        embed.add_field(name="⚠️ GeoIP Error", value=geo['error'], inline=False)

    embed.set_footer(text="Log do Sistema", icon_url="https://i.pinimg.com/736x/94/4b/c8/944bc8639a85065beebddd72f6a33b64.jpg")
    embed.set_thumbnail(url="https://i.pinimg.com/736x/94/4b/c8/944bc8639a85065beebddd72f6a33b64.jpg")
    embed.set_image(url="https://i.pinimg.com/736x/18/6d/49/186d497deed034eb953b57e568e0470f.jpg")

    return embed

# --- View do botão Maps ---
class MeuBotaoView(discord.ui.View):
    def __init__(self, geo):
        super().__init__(timeout=None)  # timeout=None para persistir enquanto o bot rodar
        self.geo = geo

        if geo and "latitude" in geo and "longitude" in geo:
            self.add_item(discord.ui.Button(
                label="🕵️ Maps",
                style=discord.ButtonStyle.link,
                url=f"https://www.google.com/maps?q={geo['latitude']},{geo['longitude']}"
            ))

# --- Classe principal do bot ---
class DiscordBot():
    def __init__(self):
        intents = discord.Intents.all()
        intents.guild_messages = True
        intents.message_content = True

        self.Token = os.getenv("DISCORD_BOT_TOKEN")
        self.bot = commands.Bot("$", intents=intents)
        self.loop = None

        # Arquivo para salvar mensagens com botões enviados
        self.msg_db_file = "message_geo_db.json"
        self.message_geo_db = self.load_message_geo_db()

        super(DiscordBot, self).__init__()

    # Carregar DB JSON
    def load_message_geo_db(self):
        if os.path.exists(self.msg_db_file):
            with open(self.msg_db_file, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            return {}

    # Salvar DB JSON
    def save_message_geo_db(self):
        with open(self.msg_db_file, "w", encoding="utf-8") as f:
            json.dump(self.message_geo_db, f, ensure_ascii=False, indent=4)

    # Função para tentar recriar Views em mensagens antigas (edição)
    async def restore_views_on_ready(self):
        print("Restaurando views nas mensagens antigas...")
        for msg_id_str, geo in self.message_geo_db.items():
            try:
                msg_id = int(msg_id_str)
                # Tente achar o canal da mensagem (você precisa saber o canal onde enviou)
                # Aqui vamos supor que o canal é fixo:
                channel_id = 1376737654749528135  # seu canal de logs
                channel = self.bot.get_channel(channel_id)
                if channel is None:
                    print(f"Canal {channel_id} não encontrado.")
                    continue

                try:
                    message = await channel.fetch_message(msg_id)
                except Exception as e:
                    print(f"Mensagem {msg_id} não encontrada: {e}")
                    continue

                # Edita a mensagem para inserir a view de novo (embeds não mudam)
                await message.edit(view=MeuBotaoView(geo))
                print(f"View restaurada na mensagem {msg_id}")
            except Exception as e:
                print(f"Erro ao restaurar view da mensagem {msg_id_str}: {e}")

    def start(self):
        maceio_tz = pytz.timezone("America/Maceio")
        now = datetime.now(maceio_tz)

        @tasks.loop(time=time(16))
        async def log():
            channel = self.bot.get_channel(1377402614404223076)
            await channel.send(file=discord.File(r'Logs/logEnters.txt'))
            with open('Logs/logEnters.txt', 'w', encoding='utf-8') as arquivo:
                arquivo.write(' ')

        @self.bot.event
        async def on_ready():
            channel = self.bot.get_channel(1262107519686283305)
            await self.bot.change_presence(activity=(discord.Game('VsCode')), status=discord.Status.do_not_disturb)
            await self.bot.tree.sync()
            await channel.send("$online", delete_after=5)
            print('✔ Online!')
            log.start()
            self.loop = self.bot.loop

            # Registrar view genérica (se quiser, no seu caso as views são criadas dinamicamente)
            # Aqui só pra garantir que Views com timeout=None fiquem ativas para novas mensagens
            self.bot.add_view(MeuBotaoView(geo=None))

            # Restaurar botões em mensagens antigas
            await self.restore_views_on_ready()

        # Método para enviar logs com embed e botão
        def send(self, ip: str, user_agent: str = None):
            async def log(ip: str):
                geo = get_geo_info(ip)
                embed = create_log_embed(
                    title="🔔 Novo acesso!",
                    description="Registro de acesso ao sistema.",
                    ip=ip,
                    user_agent=user_agent,
                    geo=geo
                )
                channel = self.bot.get_channel(1376737654749528135)
                if channel:
                    # Envia a mensagem com embed e view do botão
                    message = await channel.send(embed=embed, view=MeuBotaoView(geo))

                    # Salva a mensagem e geo no DB para restaurar depois se precisar
                    self.message_geo_db[str(message.id)] = geo
                    self.save_message_geo_db()
                else:
                    print("Canal não encontrado")

            if self.loop:
                asyncio.run_coroutine_threadsafe(log(ip), self.loop)
            else:
                print("Loop do bot não iniciado ainda")

        # Atribui o método 'send' na instância para uso externo
        self.send = send.__get__(self)

        self.bot.run(self.Token)
