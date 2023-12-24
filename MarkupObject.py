class MarkupObject:
    def __init__(self, word: str, offset: int):
        self.word: str = word
        self.offset: int = offset

    def __str__(self):
        return f'{self.word} {self.offset}'

    @staticmethod
    def from_string(string: str):
        chunks = string.split(' ')
        return MarkupObject(chunks[0], int(chunks[1]))
