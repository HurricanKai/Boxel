from twisted.internet import defer
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from .service import stream, website, picture
from urlparse import urlparse
from twisted.application import internet

import txredisapi as txredis
import cStringIO
import base64
import ujson
import os
import ujson
import requests
import uuid

class BoxelComponent(ApplicationSession):
    def __init__(self, config=None):
        ApplicationSession.__init__(self, config)
        if self.config.extra['redis']:
            # parsed = urlparse(self.config.extra['redis'])
            parsed = urlparse(os.getenv('REDIS_PORT_6379_TCP') + '/0')
            host = parsed.hostname
            port = parsed.port
            db = int(parsed.path.replace('/', ''))

            self.config.extra['redis'] = txredis.lazyConnectionPool(
                    host=host, port=port, dbid=db)
        self.user_hisory = {}
        print("component created")

    def onConnect(self):
        print("transport connected")
        self.join(self.config.realm)

    def onChallenge(self, challenge):
        print("authentication challenge received")

    @defer.inlineCallbacks
    def onJoin(self, details):
        try:
            yield self.register(self.handleStream,      u'com.boxel.stream')
            yield self.register(self.handle_website,    u'com.boxel.website')
            yield self.register(self.handle_mms,        u'com.boxel.mms')
            print('procedures registered')
        except Exception as e:
            print('could not register procedure: {0}'.format(e))

    def onDisconnect(self):
        print("transport disconnected")

    def handleStream(self, room, payload):
        msg = payload.decode('utf8')
        img, boxels = stream(
                self.config.extra['boxel_width'], msg,
                self._update_dims(uuid), self.config.extra['palette'])
        if self.config.extra['redis'] and self.config.extra['palette']:
            self.push_frame(room, boxels)

        img_buffer = cStringIO.StringIO()
        img.save(img_buffer, format='JPEG')
        imgStr = base64.b64encode(img_buffer.getvalue())
        return imgStr

    def handle_website(self, data):
        uuid, url = data
        self.user_hisory[uuid] = 'website'
        img, boxels = website(
                self.config.extra['boxel_width'], url,
                self.config.extra['palette'])
        flat = boxels.flatten().tolist()
        return ujson.dumps({'rows': boxels.shape[0], 'columns': boxels.shape[1],
            'colors': flat })

    def handle_mms(self, data):
        uuid, url = data
        self.user_hisory[uuid] = 'mms'
        img, boxels = picture(
                self.config.extra['boxel_width'], url,
                media='mms', palette=self.config.extra['palette'])
        flat = boxels.flatten().tolist()
        return ujson.dumps({'rows': boxels.shape[0], 'columns': boxels.shape[1],
            'colors': flat })

    def _update_dims(self, uuid):
        if self.user_hisory.get(uuid) == 'website' or \
        self.user_hisory.get(uuid) == 'mms':
            del self.user_hisory[uuid]
            return True
        else:
            return False

    def push_frame(self, uid, boxels):
        data =  {'rows': boxels.shape[0], 'columns': boxels.shape[1],
                 'colors': boxels.flatten().tolist()}
        return self.publish_redis('{0}'.format(uid), ujson.dumps(data))

    @defer.inlineCallbacks
    def list_users(self):
        data = []
        redis_client = self.config.extra['redis']
        if redis_client:
            keys = yield redis_client.keys('PLAYERS:*')

            for key in [k for k in keys if k.count(":") == 1]:
                player_data = yield redis_client.hgetall(key)
                data.append(player_data)
        defer.returnValue(data)

    def publish_redis(self, channel, message):
        redis_client = self.config.extra['redis']
        if redis_client:
            return redis_client.publish(channel, message)


def start(websocket, boxel_width, redis=None, palette=None, realm=None):
    runner = ApplicationRunner(
            url=websocket, realm=realm,
            extra={'boxel_width': boxel_width, 'redis': redis,
                'palette': palette})
    runner.run(BoxelComponent)
