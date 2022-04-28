class Subscriber:
    def __init__(self, name):
        self.name = name

    # def update(self, data):
    #     print('{} got message "{}"'.format(self.name, data))


class Publisher:
    def __init__(self, events):
        self.events = {event: dict() for event in events}

    def add_event(self, event) -> None:
        if event not in self.events:
            self.events[event] = dict()

    def get_subscribers(self, event) -> dict:
        return self.events[event]

    def register(self, event, who, callback=None) -> None:
        if callback is None:
            callback = getattr(who, 'update')
        self.get_subscribers(event)[who] = callback

    def unregister(self, event, who):
        del self.get_subscribers(event)[who]

    def dispatch(self, event, data):
        for subscriber, callback in self.get_subscribers(event).items():
            callback(data)


if __name__ == '__main__':
    pass
