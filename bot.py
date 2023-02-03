import os
import sys
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
        self.password = sys.argv[1]
        self.source = sys.argv[2]
        self.webhook = sys.argv[3]
        self.ws = None
        super().__init__(
            token=sys.argv[5],
            prefix="!",
            initial_channels=[sys.argv[4]],
            nick="YAB",
        )

    async def identify_obs(self):
        data = {
            "ip": "localhost",
            "port": os.environ.get("OBS_PORT"),
            "password": self.password,
            "source": self.source,
        }
        self.ws = WebSocketClient(
            url=f"ws://{data['ip']}:{data['port']}", password=data["password"]
        )
        await self.ws.connect()
        identified = await self.ws.wait_until_identified()

    async def event_ready(self):
        print(f"Logged in as | {self.nick}", flush=True)
        await self.identify_obs()

    @commands.command()
    async def sc(self, ctx: commands.Context):
        name = self.source
        print(f"{ctx.author.name} has issued a screenshot command!", flush=True)
        async with aiohttp.ClientSession() as session:
            req_data = {
                "sourceName": name,
                "imageFormat": "jpg",
            }
            await self.identify_obs()
            req = await self.ws.call(
                Request("GetSourceScreenshot", requestData=req_data)
            )
            if not req.ok:
                return
            img = req.responseData["imageData"]
            img = img[img.find("/9") :]
            tmp = File(io.BytesIO(base64.b64decode(img)), filename=f"{name}.png")
            webhook = Webhook.from_url(
                self.webhook,
                session=session,
            )
            await webhook.send(f"Screenshot from {ctx.author.name}:", file=tmp)
            await ctx.send(f"{ctx.author.name}'s screenshot has been sent!")


print("Running bot")
bot = Bot()
bot.run()
