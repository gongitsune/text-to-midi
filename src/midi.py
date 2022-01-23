from __future__ import annotations

import itertools
import json
import random

import pretty_midi as mid
from PIL import Image, ImageOps

import image
import markov
import util
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

    def molding_to_chords(
        self, chord_order: list[str], bar_num: int = 8
    ) -> ImageToMidi:
        keys = list(self.track.messages.keys())
        for cur_index, t_list in enumerate(
            [keys[i : i + bar_num] for i in range(0, len(keys), bar_num)]
        ):
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
        return self

    def molding_volume(self) -> ImageToMidi:
        for msgs in self.track.messages.values():
            for msg in random.sample(msgs, int(len(msgs) / 2)):
                msg.velocity = random.randint(40, 120)

        return self

    def change_duration(self, pos: float, duration: float, offset: float = 0) -> None:
        for msg in self.track.messages[pos]:
            msg.end = msg.start + duration
        diff = None
        for key, msgs in self.track.messages.items():
            if key <= pos:
                continue
            if not diff:
                diff = msgs[0].start - self.track.messages[pos][0].end
            for msg in msgs:
                msg.start = msg.start - diff + offset
                msg.end = msg.end - diff + offset

    def molding_duration(self) -> ImageToMidi:
        durations = {self.duration: 1, self.duration * 0.5: 1}
        state = {self.duration: 1, self.duration / 2: 1, self.duration * 1.5: 0.5}
        current_state = [list(state.keys())[0], 0]
        for key in self.track.messages.keys():
            if random.randint(0, 1) != 1:
                continue
            if random.random() < current_state[1] / 10:
                current_state = [
                    random.choices(
                        list(state.keys()), weights=list(state.values()), k=1
                    )[0],
                    0,
                ]

            current_state[1] += 1
            duration = (
                random.choices(
                    list(durations.keys()), weights=list(durations.values()), k=1
                )[0]
                if current_state[0] == self.duration
                else current_state[0]
            )
            self.change_duration(
                key,
                duration,
                self.duration / 2 if random.random() < 0.3 else 0.0,
            )

        return self

    def molding_rhythm(self, max_note: int = 3) -> ImageToMidi:
        # min_bar: None | list[list[mid.Note]] = None
        for index in range(int(len(self.track.messages.keys()))):
            try:
                bar = self.track.bar(index)
            except Exception:
                break
            for msgs in bar:
                if len(msgs) < max_note:
                    continue
                for msg in random.sample(msgs, k=len(msgs) - max_note):
                    self.track.remove_msg(msg)

        return self


if __name__ == "__main__":
    with open("dist/chords_data.json", "r") as f:
        data: list[list[str]] = json.load(f)
        molding_data = list(itertools.chain.from_iterable(data))
        model = markov.make_model(molding_data, order=4)
        # root = random.choice(["C", "D", "E", "F", "G", "A", "B"])
        result = [
            elem
            for elem in markov.make_result(model, max_items=50, seed="A", num=1)[0]
            if elem != "[EOF]"
            and elem != "[BOF]"  # noqa
            and "on" not in elem  # noqa
            and "-" not in elem  # noqa
        ]

        img = image.img_process(Image.open("image/paint_line.png"))
        midi = mid.PrettyMIDI()

        track = (
            ImageToMidi(img, 0.5)
            .molding_to_chords(result, bar_num=2)
            .molding_rhythm()
            .molding_volume()
            .molding_duration()
            .get_track()
        )
        midi.instruments.append(track.build_instrument())
        midi.write("dist/dist.mid")
        print(result)
