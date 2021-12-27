import image
import pretty_midi as mid
from PIL import Image
from PIL import ImageOps


class MyTrack:
    # { start sec: Note object }
    messages: dict[float, list[mid.Note]] = {}

    def __init__(self) -> None:
        pass

    def add_msg(self, msg: mid.Note):
        self.messages.setdefault(msg.start, [])
        self.messages[msg.start].append(msg)

    def get_msgs(self, start_sec: float):
        return self.messages[start_sec]

    def remove_msg(self, msg: mid.Note):
        self.messages[msg.start].remove(msg)

    def sorted_track(self):
        track = MyTrack()
        for msg_list in self.messages.values():
            for msg in msg_list:
                track.add_msg(msg)

        track.messages = dict(sorted(track.messages.items(), key=lambda x: x[0]))
        return track

    def build_instrument(self):
        instrument = mid.Instrument(0)
        for msg_list in self.messages.values():
            for msg in msg_list:
                instrument.notes.append(msg)

        return instrument


class ImageToMidi:
    def __init__(self, img: Image.Image) -> None:
        self.img = img

    def to_track(self, duration: float = 0.25) -> MyTrack:
        """Convert images to MyTrack

        Args:
            duration (float, optional): Note duration. Defaults to 0.25.

        Returns:
            MyTrack: Converted mytrack
        """
        track = MyTrack()
        # Calc pitch offset
        offset = (127 - self.img.height) // 2
        img_data = ImageOps.flip(self.img).getdata()
        for y in range(self.img.height):
            y_cache = y * self.img.width
            for x in range(self.img.width):
                pixel = img_data[y_cache + x]
                if pixel != 0:
                    start = x * duration
                    end = start + duration
                    track.add_msg(mid.Note(60, y + offset, start, end))

        return track

    def molding_chords_bar(self):
        pass


if __name__ == "__main__":
    img = image.img_process(Image.open("TextToMidi/image/text.png"))
    midi = mid.PrettyMIDI()
    midi.instruments.append(ImageToMidi(img).to_track().build_instrument())
    midi.write("TextToMidi/dist/dist.mid")
