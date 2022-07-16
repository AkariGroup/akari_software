from akari_controller.color import Color, Colors


def test_color() -> None:
    color = Color(12, 34, 56)
    assert color.red == 12
    assert color.green == 34
    assert color.blue == 56

    color2 = Color(12, 34, 56)
    assert color == color2

    greenyellow = Color(173, 255, 47)
    greenyellow2 = Color(168, 252, 40)

    assert greenyellow != greenyellow2

    rgb565 = greenyellow.as_rgb565()
    converted = Color.from_rgb565(rgb565)
    assert greenyellow != converted
    assert greenyellow2 == converted


def test_colors() -> None:
    mapping = [
        ("black", 0x0000),
        ("navy", 0x000F),
        ("darkgreen", 0x03E0),
        ("darkcyan", 0x03EF),
        ("maroon", 0x7800),
        ("purple", 0x780F),
        ("olive", 0x7BE0),
        ("lightgrey", 0xC618),
        ("darkgrey", 0x7BEF),
        ("blue", 0x001F),
        ("green", 0x07E0),
        ("cyan", 0x07E0),
        ("red", 0xF800),
        ("magenta", 0xF81F),
        ("yellow", 0xFFE0),
        ("white", 0xFFFF),
        ("orange", 0xFD20),
        ("greenyellow", 0xAFE5),
        ("pink", 0xF81F),
    ]

    for name, expected in mapping:
        color = Colors[name.upper()]
        assert color.as_rgb565() == expected, name
