import os
import aiohttp
import io, base64
from discord import Webhook, SyncWebhook, File
from twitchio.ext import commands
from dotenv import load_dotenv
from simpleobsws import WebSocketClient, Request, RequestResponse, RequestStatus

load_dotenv()


INITIAL_CHANNELS = [
    "",
]


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            token=os.environ.get("BOT_TOKEN"),
            prefix="!",
            initial_channels=INITIAL_CHANNELS,
            nick="YAB",
        )

    async def event_ready(self):
        print(f"Logged in as | {self.nick}")
        data = {
            "ip": os.environ.get("OBS_IP"),
            "port": os.environ.get("OBS_PORT"),
            "password": os.environ.get("OBS_PASSWORD"),
            "source": os.environ.get("SOURCE_NAME"),
        }
        self.ws = WebSocketClient(
            url=f"ws://{data['ip']}:{data['port']}", password=data["password"]
        )
        await self.ws.connect()
        await self.ws.wait_until_identified()

    @commands.command()
    async def sc(self, ctx: commands.Context):
        name = os.environ.get("SOURCE_NAME")
        async with aiohttp.ClientSession() as session:
            req_data = {
                "sourceName": name,
                "imageFormat": "jpg",
            }
            req = await self.ws.call(
                Request("GetSourceScreenshot", requestData=req_data)
            )
            if not req.ok:
                return
            img = req.responseData["imageData"]
            img = img[img.find("/9") :]
            tmp = File(io.BytesIO(base64.b64decode(img)), filename=f"{name}.png")
            webhook = Webhook.from_url(
                os.environ.get("DISCORD_WEBHOOK"),
                session=session,
            )
            await webhook.send(f"Screenshot from {ctx.author.name}:", file=tmp)
            await ctx.send(f"{ctx.author.name}'s screenshot has been sent!")
            # await ctx.send(resp)
            # discord_re = await session.post("https://discord.com/api/webhooks/931496554462855198/NaHuG4ybtglHPCxAuZccF6RF7h5-4ZU-pQXutffJP5f6i7ZXaD5S4e6_yYw1focFGs6J",
            #                     json={'content': resp['img']},)
            # resp = await discord_re.text()


bot = Bot()
bot.run()
