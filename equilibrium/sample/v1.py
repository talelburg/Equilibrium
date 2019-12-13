import datetime

from construct import Struct, Int64ul, PascalString, Int32ul, Enum, Bytes, GreedyRange, Float64l, Int8ul, this, \
    Float32l, Adapter, ExprValidator, obj_


class DatetimeSecondAdapter(Adapter):
    def _decode(self, obj, context, path):
        return datetime.datetime.fromtimestamp(obj)

    def _encode(self, obj, context, path):
        return int(obj.timestamp())


DatetimeSeconds = DatetimeSecondAdapter(Int32ul)


class DatetimeMilisecondAdapter(Adapter):
    def _decode(self, obj, context, path):
        return datetime.datetime.fromtimestamp(obj / 1000)

    def _encode(self, obj, context, path):
        return int(obj.timestamp() * 1000)


DatetimeMiliseconds = DatetimeMilisecondAdapter(Int64ul)

UserInformation = Struct(
    user_id=Int64ul,
    username=PascalString(Int32ul, "utf-8"),
    birthdate=DatetimeSeconds,
    gender=Enum(Bytes(1),
                male=b'm',
                female=b'f',
                other=b'o'),
)

Snapshot = Struct(
    timestamp=DatetimeMiliseconds,
    translation=Struct(
        x=Float64l,
        y=Float64l,
        z=Float64l,
    ),
    rotation=Struct(
        x=Float64l,
        y=Float64l,
        z=Float64l,
        w=Float64l,
    ),
    color_image=Struct(
        height=Int32ul,
        width=Int32ul,
        data=Struct(
            blue=Int8ul,
            green=Int8ul,
            red=Int8ul,
        )[this.width * this.height],
    ),
    depth_image=Struct(
        height=Int32ul,
        width=Int32ul,
        data=Float32l[this.width * this.height],
    ),
    feelings=Struct(
        hunger=ExprValidator(Float32l, -1 < obj_ < 1),
        thirst=ExprValidator(Float32l, -1 < obj_ < 1),
        exhaustion=ExprValidator(Float32l, -1 < obj_ < 1),
        happiness=ExprValidator(Float32l, -1 < obj_ < 1),
    )
)


def Sample(hook=None):
    """
    Return a ``construct`` Struct to parse the sample format.

    When invoked with no argument, the Struct holds a list of all snapshots parsed.
    
    When invoked with an argument, it is assumed to be a processing hook, called on each snapshot as it is parsed.
    Each snapshot is then discarded (the list returned is empty).
    :param hook: The hook to called on each snapshot, or None
    """
    if hook is not None:
        return Struct(
            user_information=UserInformation,
            snapshots=GreedyRange(Snapshot * hook, discard=True),
        )
    else:
        return Struct(
            user_information=UserInformation,
            snapshots=GreedyRange(Snapshot),
        )


class Adapter:
    def parse(self, path: str):
        return Sample().parse_file(path)

    def build(self, obj):
        return Sample().build(obj)
