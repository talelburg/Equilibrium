from construct import Struct, Long, PascalString, Int, Enum, Bytes, GreedyRange, Double, Byte, this, Single

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
    )),
)
