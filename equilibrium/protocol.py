import datetime

from construct import Struct, Int64ul, PascalString, Int32ul, Enum, Bytes, this, Default, len_, Float64l, Int8ul, \
    Float32l, ExprValidator, obj_, Adapter


class DatetimeSecondAdapter(Adapter):
    def _decode(self, obj, context, path):
        return datetime.datetime.fromtimestamp(obj)

    def _encode(self, obj, context, path):
        return int(obj.timestamp())


DatetimeSeconds = DatetimeSecondAdapter(Int32ul)

Hello = Struct(
    user_id=Int64ul,
    username=PascalString(Int32ul, "utf-8"),
    birthdate=DatetimeSeconds,
    gender=Enum(Bytes(1),
                male=b'm',
                female=b'f',
                other=b'o'),
)

Config = Struct(
    amount=Default(Int32ul, len_(this.fields)),
    fields=PascalString(Int32ul, "utf-8")[this.amount]
)


class DatetimeMilisecondAdapter(Adapter):
    def _decode(self, obj, context, path):
        return datetime.datetime.fromtimestamp(obj / 1000)

    def _encode(self, obj, context, path):
        return int(obj.timestamp() * 1000)


DatetimeMiliseconds = DatetimeMilisecondAdapter(Int64ul)

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
