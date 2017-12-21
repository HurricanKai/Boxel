import txredisapi
from twisted.application import internet


class BoxelRedisSubscriber(txredisapi.SubscriberProtocol):
    def connectionMade(self):
        self.psubscribe("CALLS:STOP:*")
        self.psubscribe("CALLS:OUT:*")
        self.psubscribe("ACK:OUT:*")

        print("subscribed to redis patterns for calls and acks")

    def messageReceived(self, pattern, channel, message):
        parts = channel.split(":")

        if parts[0] == 'CALLS':
            if parts[1] == 'OUT':
                self.factory.boxel_component.handle_receive_call(parts[2], message)
            elif parts[1] == 'STOP':
                self.factory.boxel_component.handle_stop_call(parts[2], message)
        elif parts[0] == 'ACK':
            self.factory.boxel_component.handle_ack(parts[2], message)


class BoxelListenerFactory(txredisapi.SubscriberFactory):
    maxDelay = 10
    continueTrying = True
    protocol = BoxelRedisSubscriber

    def __init__(self, boxel_component):
        txredisapi.SubscriberFactory.__init__(self)
        self.boxel_component = boxel_component
