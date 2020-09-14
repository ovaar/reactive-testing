from typing import Dict, Optional
import rx.subject as RxSubject


class Lightbulb(object):
    uuid: str
    state: Optional[str] = None
    light_state: RxSubject.Subject

    def __init__(self, uuid: str):
        self.uuid = uuid
        self.light_state = RxSubject.Subject()

    def complete(self):
        self.light_state.on_completed()


class TestContext(object):
    lightbulbs: Dict[str, Lightbulb]

    def __init__(self):
        self.lightbulbs = dict()
