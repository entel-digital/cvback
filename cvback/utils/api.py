#from cvback.events.models import APIToken
from secrets import choice
from zxcvbn import zxcvbn


class Generator:
    def __init__(self):
        """
        Initializes the Generator object with an empty list of passwords.
        """
        self.passlist = []

    def _generate_password(self, length):
        """
        Generates a random password of the given length using a combination of alphabets and symbols.

        :param length: The length of the password to generate
        :type length: int
        :return: The generated password
        :rtype: str
        """

        # Define the character sets to be used in the password generation
        alphabets = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
        symbols = '`1234567890-=[]\\;\',./~!@#$%^&*()_+{}|:"<>?'

        # Calculate the number of symbols to be used
        num_symbols = int(length * 0.1)  # 10% of password length

        # Randomly choose alphabets and symbols to form the password
        password = [choice(alphabets) for _ in range(length - num_symbols)]
        password += [choice(symbols) for _ in range(num_symbols)]

        # Shuffle the password characters
        password = self._jumble_string(password)

        return ''.join(password)

    def _jumble_string(self, string):
        """
        Shuffles the characters in a given string.

        :param string: The string to shuffle
        :type string: str
        :return: The shuffled string
        :rtype: str
        """

        chars = list(string)
        jumbled_string = ''
        l = len(chars)

        for i in range(l):
            c = choice(chars)
            chars.remove(c)
            jumbled_string = jumbled_string + c

        return jumbled_string

    def generator(self, n, password_length):
        """
        Generates n passwords of the given length using the _generate_password method.

        :param n: The number of passwords to generate
        :type n: int
        """
        if not isinstance(n, int):
            raise TypeError("n must be an integer.")
        if not isinstance(password_length, int):
            raise TypeError("password_length must be an integer.")
        if password_length < 11:
            return []  # Return an empty list if the password length is less than 11
        self.__init__()  # Clear memory to clear out previously generated suggestions
        num_generated = 0  # Counter for the number of generated passwords with score 4
        while num_generated < n:
            password = self._generate_password(password_length)
            insights = zxcvbn(password)
            if insights['score'] == 4:
                self.passlist.append(
                    [password, insights['crack_times_seconds']['offline_fast_hashing_1e10_per_second']])
                num_generated += 1

    def get_top_N_passwords(self, N):
        """Returns a subset of the original self.passlist containing the top 'n' suggestions sorted by longest crack times.
        :param n: The upper bound to the number of top passwords to filter out.
        :type n: int
        """
        sorted_passwords = sorted(self.passlist, key=lambda p: p[1], reverse=True)
        return sorted_passwords[:N]




def api_key_generator(n_generated=12, top_selected=8):
    generator = Generator()
    generator.generator(n_generated, 32)  # Generate 12 password suggestions of length 32
    top_passwords = generator.get_top_N_passwords(top_selected)  # Retrieve the top 5 password suggestions
    for password in top_passwords:
        # existing_keys = APIToken.objects.filter(key=password['suggested password'])
        # if existing_keys.len() == 0:
        if True:
            return password[0]
    else:
        raise Exception(f'All of the {top_selected} top passwords where existing API keys!')
