class Solution(object):
    def isValid(self, word):
        """
        :type word: str
        :rtype: bool
        """
        if not len(word) >= 3:
            return False
        vowel = False
        constant = False
        for i in range(len(word) ):
            if 65 <= ord(word[i]) <= 90 or 97 <= ord(word[i]) <= 122 or 48 <= ord(word[i]) <= 57:
                if word[i].lower() in ('a', 'e', 'i', 'o', 'u'):
                    vowel = True

                if word[i].lower() in ('b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y'):
                    constant = True
            else:
                return False
        if vowel and constant:
            return True
        else:
            return False


solution=Solution()
test_cases = ['234Adas', 'b3', 'bje2342', '234Adas', "aya", "Ya$"]
for word in test_cases:
    print(f"Is '{word}' valid? {solution.isValid(word)}")