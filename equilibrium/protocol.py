from construct import Struct, Long, PascalString, Int, Enum, Bytes, this, Default, len_, Double, Byte, Single

Hello = Struct(
    user_id=Long,
    username=PascalString(Int, "utf-8"),
    birthdate=Int,
    gender=Enum(Bytes(1),
                MALE=b'm',
                FEMALE=b'f',
                OTHER=b'o'),
)

Config = Struct(
    amount=Default(Int, len_(this.fields)),
    fields=PascalString(Int, "urf-8")[this.amount]
)

Snapshot = Struct(
    timestamp=Long,
    translation=Struct(
        x=Double,
        y=Double,
        z=Double,
    ),
    rotation=Struct(
        x=Double,
        y=Double,
        z=Double,
        w=Double,
    ),
    color_image=Struct(
        width=Int,
        height=Int,
        data=Byte[3][this.width * this.height],
    ),
    depth_image=Struct(
        width=Int,
        height=Int,
        data=Single[this.width * this.height],
    ),
    feelings=Struct(
        hunger=Single,
        thirst=Single,
        exhaustion=Single,
        happiness=Single,
    )
)
