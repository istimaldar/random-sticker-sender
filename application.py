import argparse
import random
from typing import List

from telethon import TelegramClient
from telethon.tl.functions.messages import GetAllStickersRequest, GetStickerSetRequest
from telethon.tl.types import StickerSet, InputStickerSetID
from telethon.tl.types.messages import AllStickers

from settings import Settings


class Application:
    def __init__(self, args: List[str]):
        self.settings = self.__parse_arguments(args)

    async def run(self):
        async with TelegramClient('anon', api_id=self.settings.app_id, api_hash=self.settings.app_hash) as client:  # type: TelegramClient
            sticker_sets = await client(GetAllStickersRequest(0))  # type: AllStickers
            stickers = []
            for sticker_set in sticker_sets.sets:  # type: StickerSet
                extracted_stickers = await client(GetStickerSetRequest(
                    stickerset=InputStickerSetID(id=sticker_set.id, access_hash=sticker_set.access_hash)
                ))
                stickers += extracted_stickers.documents

            await client.send_file(self.settings.login, random.choice(stickers))

    @staticmethod
    def __parse_arguments(args: List[str]) -> Settings:
        parser = argparse.ArgumentParser(description='Sends random sticker to telegram chat')

        parser.add_argument('--app-id', dest='app_id', required=True, type=int, help='id of user\'s application')
        parser.add_argument('--app-hash', dest='app_hash', required=True, type=str, help='hash of user\'s application')
        parser.add_argument('--login', dest='login', required=True, type=str,
                            help='login of the user to whom you want to send a random sticker')

        parsed_args = parser.parse_args(args)

        return Settings(
            app_id=parsed_args.app_id,
            app_hash=parsed_args.app_hash,
            login=parsed_args.login
        )
