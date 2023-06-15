from pagerank import transition_model


def test_transition_model():
    #quick test since I had difficulty with this function
    corpus = {
        "1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}
        }
    page = "1.html"
    damping_factor = 0.85

    prob = transition_model(corpus, page, damping_factor)
    print(prob)
    assert sum(prob.values()) == 1
    assert abs(prob["1.html"] - 0.05) < 0.001
    assert abs(prob["2.html"] - 0.475) < 0.001
    assert abs(prob["3.html"] - 0.475) < 0.001


if __name__ == "__main__":
    test_transition_model()
