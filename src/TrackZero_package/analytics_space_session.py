class space_session:
    def __init__(self, is_success: bool, url: str, session_key: str) -> None:
        self.is_success = is_success
        self.url = url
        self.session_key = session_key