from typing import Iterable, Union


class TransitionTable(dict):
    def __init__(self, alphabet: set, *args, **kwargs):
        self.alphabet: set = alphabet
        super().__init__(*args, **kwargs)

    def __getitem__(self, item):
        transitions = super().__getitem__(item)
        complete_transitions = self.__missing__(item)
        complete_transitions.update(transitions)

        return complete_transitions

    def __missing__(self, key) -> dict:
        return {_char: key for _char in self.alphabet}

    def __repr__(self):
        fill = " "
        join_at = "|"
        width = 3

        ordered_alphabet = tuple(self.alphabet)

        header = fill*width + join_at + join_at.join(f"{transition:{fill}>{width}}" for transition in ordered_alphabet)
        rows = [header]
        for key in self:
            values = self.__getitem__(key)
            rows.append(str(key).rjust(width, fill) + join_at + join_at.join(f"{values[char]:{fill}>{width}}" for char in ordered_alphabet))

        return "\n".join(rows)


class Automaton:
    def __init__(
            self,
            alphabet: Iterable = "",
            number_of_states: int = 1,
            initial_state: int = 0,
            accepted_states: set = None,
            transition_table: dict = None
    ):
        self.alphabet: set = set(_char for _char in alphabet)
        self.states: set = set(i for i in range(number_of_states))

        self.initial_state: int = initial_state
        if self.initial_state not in self.states:
            raise ValueError(f"q₀ = {self.initial_state} ∉ Q = {self.states}")

        self.accepted_states = accepted_states if accepted_states is not None else set()
        if not self.accepted_states.issubset(self.states):
            raise ValueError(f"F = {self.accepted_states} ⊄ Q = {self.states}")

        self.transition_table: TransitionTable = TransitionTable(self.alphabet, transition_table or {})

    def __repr__(self):
        return f"Q = {self.states}\n" \
               f"Σ = {self.alphabet}\n" \
               f"q₀ = {self.initial_state} ∈ Q\n" \
               f"F = {self.accepted_states} ⊂ Q\n" \
               f"δ is defined by the following state transition table:\n" \
               f"{self.transition_table.__repr__()}"

    def run(self, expression: Union[tuple, list, str]) -> bool:
        """
        :param expression:
        :return accepted:
        """
        # check if every letter of the expression is in the alphabet
        temp_set: set = set(expression)
        if not temp_set.issubset(self.alphabet):
            raise ValueError(f"e = {temp_set} ⊄ Σ = {self.alphabet} (the expression contains foreign letters)")

        current_state = self.initial_state
        for letter in expression:
            current_state = self.transition_table[current_state][letter]

        return current_state in self.accepted_states
