from dataclasses import dataclass
import batch

import action


class Version:
    # ints: tuple[int, int, int, int]

    def __init__(self, *args):
        assert len(args) == 4
        self.ints = tuple(args)

    @classmethod
    def from_str(cls, str_ver):
        assert str_ver.count(".") == 3
        assert str_ver.replace(".", "").isdigit()
        ints = tuple(int(i) for i in str_ver.split("."))
        return cls(*ints)

    def cmp(self, other):
        """
        returns:
        -1 if self < other
        1  if self > other
        0  if self == other
        """
        assert isinstance(other, Version), other

        # ver_tuple = lambda x: tuple(int(i) for i in x.split("."))

        # ver1_tup = ver_tuple(ver1)
        # ver2_tup = ver_tuple(ver2)
        for i, j in zip(self.ints, other.ints):
            if i < j:
                return -1
            if i > j:
                return 1

        return 0

    def __eq__(self, other):
        return self.cmp(other) == 0

    def __lt__(self, other):
        return self.cmp(other) == -1

    def __le__(self, other):
        return self < other or self == other

    def __ne__(self, other):
        return not (self == other)

    def __gt__(self, other):
        return not (self <= other)

    def __ge__(self, other):
        return not (self < other)

    def __repr__(self):
        return f"Version({', '.join(str(x) for x in self.ints)})"


@dataclass
class NoteChange:
    version: Version
    actions: list[action.Action]
    fields: list[str]


NOTE_CHANGES = [
    NoteChange(
        version=Version(0, 10, 0, 0),
        actions=[
            action.MoveField("PAShowInfo", 15 - 1),
            action.MoveField("PASeparateWordCard", 19 - 1),
            action.MoveField("PASeparateSentenceCard", 19 - 1),
            action.AddField("FrequencySort", 29 - 1),
        ],
        fields=[
            "Key",
            "Word",
            "WordReading",
            "WordPitch",
            "PrimaryDefinition",
            "Sentence",
            "SentenceReading",
            "AltDisplay",
            "AltDisplayPASentenceCard",
            "AdditionalNotes",
            "IsSentenceCard",
            "IsClickCard",
            "IsHoverCard",
            "IsTargetedSentenceCard",
            "PAShowInfo",
            "PATestOnlyWord",
            "PADoNotTest",
            "PASeparateWordCard",
            "PASeparateSentenceCard",
            "SeparateClozeDeletionCard",
            "Hint",
            "HintNotHidden",
            "Picture",
            "WordAudio",
            "SentenceAudio",
            "PAGraphs",
            "PASilence",
            "FrequenciesStylized",
            "FrequencySort",
            "SecondaryDefinition",
            "ExtraDefinitions",
            "UtilityDictionaries",
            "Comment",
        ]
    ),
    NoteChange(
        version=Version(0, 9, 0, 0),
        actions=[
            action.BatchUpdate(
                batch_func=batch.add_downstep_inner_span_tag,
                ankiconnect_actions={"findNotes", "notesInfo", "multi", "updateNoteFields"},
                description="Updates the WordPitch field to work with the new AJT Pitch "
                "Accent config settings",
            ),
            action.SetField("PASilence", "[sound:_silence.wav]"),
            action.AJTPitchAccentConfigChange("update the 'styles' -> '&#42780;' field"),
            action.YomichanTemplatesChange(),
            action.YomichanFormatChange("PASilence", "[sound:silence.wav]", "[sound:_silence.wav]"),
        ],
        fields=[
            "Key",
            "Word",
            "WordReading",
            "WordPitch",
            "PrimaryDefinition",
            "Sentence",
            "SentenceReading",
            "AltDisplay",
            "AltDisplayPASentenceCard",
            "AdditionalNotes",
            "IsSentenceCard",
            "IsClickCard",
            "IsHoverCard",
            "IsTargetedSentenceCard",
            "PASeparateWordCard",
            "PASeparateSentenceCard",
            "PAShowInfo",
            "PATestOnlyWord",
            "PADoNotTest",
            "SeparateClozeDeletionCard",
            "Hint",
            "HintNotHidden",
            "Picture",
            "WordAudio",
            "SentenceAudio",
            "PAGraphs",
            "PASilence",
            "FrequenciesStylized",
            "SecondaryDefinition",
            "ExtraDefinitions",
            "UtilityDictionaries",
            "Comment",
        ],
    ),
    NoteChange(
        version=Version(0, 0, 0, 0),
        actions=[],
        fields=[
            "Key",
            "Word",
            "WordReading",
            "WordPitch",
            "PrimaryDefinition",
            "Sentence",
            "SentenceReading",
            "AltDisplay",
            "AltDisplayPASentenceCard",
            "AdditionalNotes",
            "IsSentenceCard",
            "IsClickCard",
            "IsHoverCard",
            "IsTargetedSentenceCard",
            "PASeparateWordCard",
            "PASeparateSentenceCard",
            "PAShowInfo",
            "PATestOnlyWord",
            "PADoNotTest",
            "SeparateClozeDeletionCard",
            "Hint",
            "HintNotHidden",
            "Picture",
            "WordAudio",
            "SentenceAudio",
            "PAGraphs",
            "PASilence",
            "FrequenciesStylized",
            "SecondaryDefinition",
            "ExtraDefinitions",
            "UtilityDictionaries",
            "Comment",
        ],
    ),
]