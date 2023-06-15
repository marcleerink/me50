from shopping import load_data


def test_load_data():
    evidence, labels = load_data("shopping.csv")
    assert len(evidence) == 12330
    assert len(labels) == 12330

    assert len(evidence[0]) == 17
    assert evidence[0] == [
        0,
        0.0,
        0,
        0.0,
        1,
        0.0,
        0.2,
        0.2,
        0.0,
        0.0,
        1,
        1,
        1,
        1,
        1,
        1,
        0,
    ]

    assert labels[0] is False
