import asyncio
from typing import Callable, Any, Awaitable, Union, Dict, List

from aiogram import BaseMiddleware
from aiogram.types import Message


class AlbumMiddleware(BaseMiddleware):
    album_data: Dict[str, List[Message]] = {}
    timers: Dict[str, asyncio.TimerHandle] = {}

    def __init__(self, latency: Union[int, float] = 0.5):
        self.latency = latency

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        message: Message,
        data: Dict[str, Any]
    ) -> Any:
        if not message.media_group_id or not message.photo:
            await handler(message, data)
            return

        media_group_id = message.media_group_id

        if media_group_id not in self.album_data:
            self.album_data[media_group_id] = []

        self.album_data[media_group_id].append(message)

        if media_group_id in self.timers:
            self.timers[media_group_id].cancel()

        self.timers[media_group_id] = asyncio.get_event_loop().call_later(
            self.latency,
            lambda: asyncio.create_task(self.process_album(media_group_id, handler, data))
        )

    async def process_album(
        self,
        media_group_id: str,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        data: Dict[str, Any]
    ):
        album = self.album_data.pop(media_group_id, [])
        if album:
            data['album'] = album
            await handler(album[-1], data)
        self.timers.pop(media_group_id, None)