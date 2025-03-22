# this is resulting struct of message, parsed from vk and passed then to
# telegram bridge
class ParsedMessage:
    text = ""
    video_downloaded_file = None

    # operator +=
    def __iadd__(self, other):
        self.text += other.text
        # TODO: now this only honors latest attached video. Possible cases:
        # multiple videos attached; message contained video which is itself a
        # reply by another message contained video (this case can be ignored, I
        # think); multiple forwarded messages each with video
        if other.video_downloaded_file:
            self.video_downloaded_file = other.video_downloaded_file
        return self
