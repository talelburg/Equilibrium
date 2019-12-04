from construct import Struct, Long, PascalString, Int, Enum, Bytes, GreedyRange, Double, Byte, this, Single


def image(data_format):
    return Struct(
        width=Int,
        height=Int,
        data=data_format[this.width * this.height],
    )


Sample = Struct(
    user_information=Struct(
        user_id=Long,
        username=PascalString(Int, "utf-8"),
        birthdate=Int,
        gender=Enum(Bytes(1),
                    MALE=b'm',
                    FEMALE=b'f',
                    OTHER=b'o'),
    ),
    snapshots=GreedyRange(Struct(
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
        color_image=image(Byte[3]),
        depth_image=image(Single),
        feelings=Struct(
            hunger=Single,
            thirst=Single,
            exhaustion=Single,
            happiness=Single,
        )
    )),
)
