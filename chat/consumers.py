import json
import asyncio
from time import sleep
from asgiref.sync import async_to_sync
from channels.consumer import SyncConsumer,AsyncConsumer
from channels.exceptions import StopConsumer


class MyConsumer(SyncConsumer):
    def websocket_connect(self, event):
        print('websocket connected',event)
        self.send({
            'type':'websocket.accept'
        })
    
    def websocket_receive(self, event):
        print('websocket received',event)
    
    def websocket_disconnect(self, event):
        print('websocket disconnected',event)
        raise StopConsumer()
    
    def websocket_send(self, event):
        print('websocket send',event)
        
class MyUpdatedConsumer(SyncConsumer):
    def websocket_connect(self, event):
        print('websocket connected',event)
        self.send({'type':'websocket.accept'})
        
    def websocket_receive(self, event):
        print('websocket received',event)
        print(event['text'])
        for i in range(1,11):    
            self.send({
                'type':'websocket.send',
                'text':"message received"
            })
    
    def websocket_disconnect(self, event):
        print('websocket disconnected',event)
        raise StopConsumer()
    
class MyUpdatedConsumerAC(AsyncConsumer):
    async def websocket_connect(self, event):
        print('websocket connected',event)
        await self.send({'type':'websocket.accept'})
        
    async def websocket_receive(self, event):
        print('websocket received',event)
        print(event['text'])
        first=0
        last=0
        for i in range(1,11):
            last=i
            sum=first+last    
            await self.send({
                'type':'websocket.send',
                'text':f'{first}+{last} ={sum}'
            })
            first=last
            await asyncio.sleep(1)
    
    def websocket_disconnect(self, event):
        print('websocket disconnected',event)
        raise StopConsumer()
    
    
    ############## MY Chat ##############
    
class MyChatConsumerAC(AsyncConsumer):
    async def websocket_connect(self, event):
        self.group=self.scope['url_route']['kwargs'] ['groupName']
        print('gorup name',self.group)
        await self.channel_layer.group_add(self.group,self.channel_name)
        await self.send({'type':'websocket.accept'})
        
    async def websocket_receive(self, event):
        await self.channel_layer.group_send(self.group,{
            'type':'chat.message',
            'message':event['text']
        })
    async def chat_message(self,event):
        await self.send({
            'type':'websocket.send',
            'text':event['message']
        })
        
    async def websocket_disconnect(self, event):
        await self.channel_layer.group_discard(self.group,self.channel_name)
        raise StopConsumer()
   
   
    
class MyChatConsumerSC(SyncConsumer):
     def websocket_connect(self, event):
        async_to_sync(self.channel_layer.group_add)('teambha',self.channel_name)
        self.send({'type':'websocket.accept'})
        
     def websocket_receive(self, event):
        print('websocket received...',event)
        print(event['text'])
        async_to_sync(self.channel_layer.group_send)('teambha',{
            'type':'chat.message',
            'message':event['text']
        })
     def chat_message(self,event):
        print('chat message...',event)
        self.send({
            'type':'websocket.send',
            'text':event['message']
        })
 
        
     def websocket_disconnect(self, event):
        async_to_sync(self.channel_layer.group_discard)('teambha',self.channel_name)
        raise StopConsumer()