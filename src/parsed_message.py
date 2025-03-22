# this is resulting struct of message, parsed from vk and passed then to
# telegram bridge
class ParsedMessage:
    text = ""

    # operator +=
    def __iadd__(self, other):
        self.text += other.text
        return self
