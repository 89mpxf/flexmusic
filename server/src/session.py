class SessionManager:
    def __init__(self):
        self._sessions = []

    @property
    def sessions(self) -> list:
        return self._sessions

    def add_session(self, session):
        self._sessions.append(session)

    def remove_session(self, session):
        self._sessions.remove(session)