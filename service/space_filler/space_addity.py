import re
import json


class SpaceAddity:
    """Class for adding missed spaces into a given string.

    Attributes:
        word_freq (str): A dictionary with English valid words as a key and their probabilities as a value.
        min_prob (float): The minimum value from the word_freq dictionary.
        simplified_mode (bool): When True, the given string-word found in the word_freq dictionary won't be split into
        substrings and will be less time and space consuming.

    Methods:
        add_spaces(string): Adds spaces to the string and returns indices of missed spaces.
        split_string(word): Splits the string into valid words from the dictionary, iterates over all possible splits,
        and returns the one with the highest probability.
        postprocess(initial, modified): Performs postprocessing on the initial and modified strings.
    """

    def __init__(self, dict_path, simplified_mode=True):
        """
        Args:
            dict_path: (str) json path
            simplified_mode: (bool) controls word splitting
        """

        with open(dict_path) as f:
            self.word_freq = json.loads(f.read())
        print('Dictionary loaded..')
        self.min_prob = self.word_freq['_min_value']
        self.simplified_mode = simplified_mode

    def add_spaces(self, string):
        """
        The main function to add spaces into the string.
        Args:
            string: (str) input string with missed spaces

        Returns:
            Tuple , first item is the corrected string, second one the list of input string indices of missed spaces
        """

        # Split string by whitespace and punctuation signs
        _split_re = re.compile(r"[\s,.;!?-]+")
        split_strings = _split_re.split(string)
        punctuations = _split_re.findall(string)
        punctuations = [item[:-1] if item.endswith(' ') else item for item in punctuations]

        assert len(punctuations) + 1 == len(split_strings)

        # Get missed spaces of each split substring
        modified_substrings_list = []
        for substring in split_strings:
            modified_replaced = substring.replace("'", '')
            modified_substring = self.split_string(modified_replaced)
            modified_substrings_list.append(modified_substring)

        # Merge substrings and punctuations back into one list
        merged_list = [modified_substrings_list[i] + punctuations[i] for i in range(len(punctuations))]
        if modified_substrings_list[-1] != '':
            merged_list.append(modified_substrings_list[-1])

        # Preprocess the output and return indices and corrected string
        merged_string = ' '.join(merged_list)
        output = self.postprocess(string, merged_string)
        return output

    def split_string(self, word):
        """
        Splits a string into valid words using the English dictionary and
        chooses the segmentation with the highest probability.
        Args:
            word: (str)  string to split, without punctuations

        Returns:
            The split string with the highest probability
        """

        word = word.lower()
        if self.simplified_mode and (word in self.word_freq):
            # The word is already in the dictionary
            return word

        # Initialize the list of possible segmentations
        segmentations = [[] for _ in range(len(word) + 1)]
        segmentations[0] = [()]

        # Iterate over all possible positions to split the word
        for i in range(len(word)):
            for j in range(i + 1, len(word) + 1):
                if word[i:j] in self.word_freq:
                    for segment in segmentations[i]:
                        segmentations[j].append(segment + (word[i:j],))

        # Choose the segmentation with the highest probability
        max_prob = 0
        best_segmentation = []
        segmentations = segmentations[-1]
        for segmentation in segmentations:
            prob = 1
            for word in segmentation:
                prob *= self.word_freq.get(word, self.min_prob)
            if prob > max_prob:
                max_prob = prob
                best_segmentation = segmentation

        return ' '.join(list(best_segmentation))

    @staticmethod
    def postprocess(initial, modified):
        """
        Capitalizes the modified string,
        Adds apostrophes back to their positions if they were removed during preprocessing stage
        Returns indices of the added spaces (indices on initial string)
        Args:
            initial: (str) initial string with missed spaces
            modified: (str) final output obtained after splitting the string and adding spaces

        Returns:
            Post-processed string and list of added spaces
        """
        pointer = 0
        indices = []
        for i in range(len(initial)):
            # The position where space was added
            if (initial[i] != ' ') & (modified[pointer] == ' '):
                indices.append(i)
                pointer += 1

            # The position where character is uppercase
            if initial[i].isupper():
                modified = modified[:pointer] + initial[i] + modified[pointer + 1:]

            # The position of apostrophe
            if initial[i] == "'":
                modified = modified[:pointer] + "'" + modified[pointer:]
            pointer += 1
        return modified, indices
