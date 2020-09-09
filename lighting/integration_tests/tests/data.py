from typing import Dict, Optional
import rx.subject as RxSubject


class Observables(object):
    light_state: RxSubject.Subject

    def __init__(self):
        self.light_state = RxSubject.Subject()

    def complete(self):
        self.light_state.on_completed()


class Lightbulb(object):
    uuid: str
    state: Optional[str] = None
    observables: Observables

    def __init__(self, uuid: str, observables: Observables):
        self.uuid = uuid
        self.observables = observables


class TestContext(object):
    lightbulbs: Dict[str, Lightbulb]

    def __init__(self):
        self.lightbulbs = dict()
