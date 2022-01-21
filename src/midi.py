from __future__ import annotations
import image
import pretty_midi as mid
from PIL import Image
from PIL import ImageOps
import util
import markov
import json
import itertools
import random

from music_chords import Chord


class MyTrack:
    # { start sec: Note object }
    messages: dict[float, list[mid.Note]] = {}
    min_messages = messages
    sorted_track = None

    def __init__(self) -> None:
        pass

    def add_msg(self, msg: mid.Note) -> None:
        self.messages.setdefault(msg.start, [])
        self.messages[msg.start].append(msg)

    def get_msgs(self, start_sec: float) -> list[mid.Note]:
        return self.messages[start_sec]

    def remove_msg(self, msg: mid.Note) -> None:
        self.messages[msg.start].remove(msg)

    def sorted(self) -> MyTrack:
        if not self.sorted_track or self.min_messages != self.messages:
            track = MyTrack()
            track.messages = dict(sorted(self.messages.items(), key=lambda x: x[0]))

            # Update
            self.min_messages = self.messages
            self.sorted_track = track
        return self.sorted_track

    def bar(self, bar_index: int, bar_duration: int = 4) -> list[list[mid.Note]]:
        return [
            self.messages[t]
            for t in list(self.sorted().messages.keys())[
                bar_index : bar_index + bar_duration
            ]
        ]

    def build_instrument(self) -> mid.Instrument:
        instrument = mid.Instrument(0)
        for msg_list in self.messages.values():
            for msg in msg_list:
                instrument.notes.append(msg)

        return instrument


class ImageToMidi:
    def __init__(self, img: Image.Image, duration: float = 0.25) -> None:
        self.img = img
        self.track = self.to_track(duration).sorted()
        self.duration = duration

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

    def get_track(self) -> MyTrack:
        return self.track

    def molding_to_chords(self, chord_order: list[str], bar_num: int = 8) -> MyTrack:
        cur_index = 0
        keys = list(self.track.messages.keys())
        for t_list in [keys[i : i + bar_num] for i in range(0, len(keys), bar_num)]:
            note_nums = Chord(chord_order[cur_index % len(chord_order)]).note_numbers()
            for t in t_list:
                use_note_num = []
                for note in self.track.messages[t]:
                    note.pitch = int(
                        util.get_nearest_value(note_nums, note.pitch % 12)
                        + (12 * (note.pitch // 12)),  # noqa
                    )
                    use_note_num.append(note.pitch)
                # 差分を確認
                diff = list(set(note_nums) - set(use_note_num))
                nums = [note.pitch for note in self.track.messages[t]]
                average = sum(nums) / len(nums)
                for pitch in diff:
                    self.track.messages[t].append(
                        mid.Note(
                            60,
                            int(
                                util.get_nearest_value(
                                    note_nums, (pitch + average) % 12
                                )
                                + (12 * (note.pitch // 12)),  # noqa
                            ),
                            t,
                            t + self.duration,
                        )
                    )
            cur_index += 1
        return self.track


if __name__ == "__main__":
    with open("dist/chords_data.json", "r") as f:
        data: list[list[str]] = json.load(f)
        molding_data = list(itertools.chain.from_iterable(data))
        model = markov.make_model(molding_data, order=4)
        root = random.choice(["C", "D", "E", "F", "G", "A", "B"])
        result = [
            elem
            for elem in markov.make_result(model, max_items=50, seed="C", num=1)[0]
            if elem != "[EOF]"
            and elem != "[BOF]"
            and "on" not in elem
            and "-" not in elem
        ]

        img = image.img_process(Image.open("image/text.png"))
        midi = mid.PrettyMIDI()

        track = ImageToMidi(img, 0.5).molding_to_chords(result, bar_num=2)
        midi.instruments.append(track.build_instrument())
        midi.write("dist/dist.mid")
        print(result)
