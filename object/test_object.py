from pyreto.object import Object


def test_init():
    o = Object(x=1, y=2)
    assert o.x == 1
    assert o.y == 2


def test_str():
    o = Object(x=1, y=2)
    assert any([
        str(o) == '{x: 1, y: 2}',
        str(o) == '{y: 2, x: 1}',
    ])
