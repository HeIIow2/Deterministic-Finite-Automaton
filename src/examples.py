from automaton import Automaton


def test(test_cases: tuple, automaton: Automaton):
    print(automaton)
    print()
    for test_case in test_cases:
        print(test_case.ljust(15), automaton.run(test_case))


def a_before_b():
    """
    alle A's müssen vor B's sein
    :return:
    """

    automaton = Automaton(
        alphabet="AB",
        number_of_states=3,
        initial_state=0,
        accepted_states={0, 1},
        transition_table={
            0: {"B": 1},
            1: {"A": 2},
            2: {"A": 2, "B": 2}
        }
    )

    test((
        "",
        "AAAAAAAAAA",
        "BBBBBBBBBB",
        "AAABBBAAAA",
        "BBBBBAAAAA",
    ), automaton)


def get_automaton_contains_the_word(word: str) -> Automaton:
    alphabet: set = set(char for char in word)
    start_node = 0
    transition_table = {}

    i = 0
    for i, char in enumerate(word):
        transition_table[i] = {}

        transition_table[i][char] = i + 1
        for _char in alphabet:
            if _char == char:
                continue

            transition_table[i][_char] = start_node

    return Automaton(
        alphabet=word,
        number_of_states=i+2,
        transition_table=transition_table,
        accepted_states={i+1, },
        initial_state=start_node
    )


def contains_the_word():
    print("helloworld")
    test(("helloworld", "helloworldhldl", "hellloworldhldl"), get_automaton_contains_the_word("helloworld"))


if __name__ == "__main__":
    contains_the_word()
