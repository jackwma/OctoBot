#  Drakkar-Software OctoBot
#  Copyright (c) Drakkar-Software, All rights reserved.
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3.0 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library.
import asyncio
from abc import ABCMeta
from asyncio import Task
from queue import Queue
from typing import List

from tools import get_logger


class Producer:
    __metaclass__ = ABCMeta

    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)

        # List of consumer queues to be fill
        self.consumer_queues: List[Queue] = []
        self.produce_task: Task = None
        self.should_stop: bool = False

    async def send(self, **kwargs):
        """
        Send to each consumer data though its queue
        :param data:
        :return:
        """
        for queue in self.consumer_queues:
            await queue.put(kwargs)

    async def receive(self, **kwargs):
        """
        Receive notification that new data should be sent implementation
        When nothing should be done on data : self.send()
        :return:
        """
        pass

    async def start(self):
        """
        Should be implemented for producer's non-triggered tasks
        :return:
        """
        pass

    async def perform(self, **kwargs):
        """
        Should implement producer's non-triggered tasks
        Can be use to force producer to perform tasks
        :return:
        """
        pass

    async def stop(self):
        """
        Stops non-triggered tasks management
        :return:
        """
        self.should_stop = True

    def create_task(self):
        self.produce_task = asyncio.create_task(self.receive())

    def new_consumer(self, size=0):
        consumer_queue = Queue(size)
        self.consumer_queues.append(consumer_queue)
        return consumer_queue

    async def run(self):
        await self.start()
        self.create_task()
