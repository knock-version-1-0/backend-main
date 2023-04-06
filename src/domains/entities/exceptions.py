class NoteNameIntegrityError(Exception):
    message = "동일한 Author일 경우 Note.name을 중복해서 등록할 수 없습니다."
    def __init__(self, *args):
        super().__init__(self.message, *args)


class KeywordPositionOrderIntegrityError(Exception):
    message = "동일한 Keyword 내에서 Position.order는 중복될 수 없습니다."
    def __init__(self, *args):
        super().__init__(self.message, *args)
