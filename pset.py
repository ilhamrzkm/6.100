"""
6.100 Fall 2025
Problem Set 1

Fill out the following info:
Name: Sana Shah 
Kerberos: sanashah
Approximate time spent (HH:MM): 04:00 
"""

import string
# NO OTHER IMPORTS ALLOWED


############################################################
# supplied helper functions -- DO NOT MODIFY
############################################################


global all_words
global all_contractions


def collect_file_entries(filename):
    with open(filename) as file:
        return [line.strip() for line in file]


def initialize_words():
    global all_words
    global all_contractions
    all_words = set(collect_file_entries("words.txt"))
    all_contractions = set(collect_file_entries("contractions.txt"))


def is_possessive_word(text):
    global all_words
    return (
        text[-2:] == "'s" and text[:-2] in all_words
        or text[-1:] == "'" and text[:-1] in all_words
    )


def is_word(text):
    """
    Determine whether or not a given string is a word (as defined by its
    presence in words.txt or contractions.txt).

    Parameters:
        text (str): The text to be tested. Has no punctuation or
            whitespaces and only consists of lowercase characters.

    Return True if text is a valid word, False otherwise.
    """
    if not hasattr(is_word, "executed"):
        initialize_words()
        is_word.executed = True
    global all_words
    global all_contractions
    return (
        text in all_words
        or text in all_contractions
        or is_possessive_word(text)
    )


############################################################
# encryption and decryption for Beaver ciphers
############################################################


def crypt_char(char, alphabet, shift, encrypt):
    """
    Encrypt or Decrypt a character   
    
    Parameters: 
        char (str): The character that is being encrypted 
        alphabet (str): The ordered alphabet which we are doing the ceaser cipher 
        shift (int): The number of positions to shift the character by  
        encrypt (bool): Specifying encrypt vs decrypt (true vs false)
    
    Return the encrypted value based on the shift 
    """
    i_shift = shift 

    if not encrypt:
        i_shift *= -1   #checks for encrypt or decrypt 
    
    index = alphabet.find(char)
    new_index = (index + i_shift) % len(alphabet)   #creates new index number based on shift 
    return alphabet[new_index]  # new index is put back in the alphabet 

def encrypt_char(char, alphabet, shift):
    """
    Encrypt a character using ceaser cipher   
    Parameters: 
        char (str): The character that is being encrypted 
        alphabet (str): The ordered alphabet which we are doing the ceaser cipher 
        shift (int): The number of positions to shift the character by  
    
    Return the encrypted value based on the shift 
    """
    encrypt = True 
    return crypt_char(char, alphabet, shift, encrypt) # return crypt_char with encrypt as True 


def decrypt_char(char, alphabet, shift):
    """
    Decrypt a character using ceaser cipher   

    Parameters: 
        char (str): The character that is being encrypted 
        alphabet (str): The ordered alphabet which we are doing the ceaser cipher 
        shift (int): The number of positions to shift the character by   

    Returns the decrypted value based on the shift 
    """

    encrypt = False 
    return crypt_char(char, alphabet, shift, encrypt) # return crypt_char with encrypt as False (decrypt)
    


def encrypt(plaintext, alphabet, initial_shift, magic_number):
    """
    Encrypt a plaintext using a specified Beaver cipher.

    Parameters:
        plaintext (str): The message to be encrypted.
        alphabet (str): The ordered alphabet within which to perform the
            Beaver cipher.
        initial_shift (int): The number of positions in alphabet to
            shift forward the first character of plaintext.
        magic_number (int): The magic number to be used in the Beaver
            cipher. It should be positive and smaller than the length
            of alphabet.

    Return the encrypted ciphertext str corresponding to plaintext.
    """
    
    shift = initial_shift

    shifted = ""    # will be the encrypted cypher 

    for c in plaintext:     # loops through every character in (str) plaintext 
        if c in alphabet:       # checks that character is in alphabet 
            index = alphabet.find(c)
            new_index = (index + shift) % len(alphabet)
            shifted += alphabet[new_index]
            if new_index % magic_number == 0:   # checks if a multiple of magic number 
                shift +=1
        else: 
                shifted += c
    return shifted      # returns encrypted string 


def decrypt(ciphertext, alphabet, initial_shift, magic_number):
    """
    Decrypt a ciphertext according to a specified Beaver cipher.

    Parameters:
        ciphertext (str): The encrypted text to be decrypted.
        alphabet (str): The same as in encrypt().
        initial_shift (int): The same as in encrypt().
        magic_number (int): The same as in encrypt().

    Return the decrypted plaintext str corresponding to ciphertext.
    """
    shift = initial_shift

    shifted = ""    # will be the decrypted cypher 

    for c in ciphertext:     # loops through every character in (str) ciphertext 
        if c in alphabet:      # checks that character is in alphabet 
            index = alphabet.find(c)
            new_index = (index - shift) % len(alphabet) #subtract the shift 
            shifted += alphabet[new_index]
            if index % magic_number == 0: # checks if orginal index is a multiple of magic number 
                shift += 1

        else: 
                shifted += c
    return shifted  # returns decrypted string


############################################################
# breaking the Beaver cipher
############################################################


whitespace = " \n"
links = "-/"
pauses = ",;:.?!"
double_quote = '"'
separators = whitespace + links + pauses + double_quote


def count_words(text):
    """
    Return the number of valid English words in a given string.

    Valid English words are those on which is_word() returns True.
    Candidate words are the sequences of characters between valid
    separators.
    """
    temp = ""       # temporarily stores characters for the current word 
    count = 0  # number of valid english words 
    text = text.lower()     # convert text to lowercase 
    text = text + " "
    
    for c in text:  # loop through every character in (str) test 
        if c in separators: # if the character is a separtor, the current word has ended 
            if is_word(temp):  # check if all the current characters form an english word 
                count +=1 
            temp = ""   # reset for next word 
        else: # else add another character to the current word 
            temp += c 
    return count    #returns total number of valid english words 


def break_cipher(ciphertext, alphabet):
    """
    Decode a message encrypted by a Beaver cipher into its likely
    original source, without prior knowledge of the key.

    Parameters:
        ciphertext (str): The encrypted text.
        alphabet (str): The alphabet under which the Beaver cipher
            encryption was performed.

    Return a plaintext str that contains the most English words out of
    all possible plaintexts. If there is more than one such plaintext,
    return any of them.
    """
    plaintext = ""
    count = -1      # start at -1 so that solution is in range 

    for magic_number in range(1, 100):  # checks for magix numbers between 1 and 99 
        for initial_shift_base in range(87):    # size of alphabet is 86 characters so shift is in that range
            temp = decrypt(ciphertext, alphabet, initial_shift_base, magic_number)
            num = count_words(temp)

            if num>count:  # if number of words is greater than a prev count, stores best answer 
                plaintext = temp 
                count = num
    return plaintext    # returns most English words out of all possible plaintexts


############################################################
# manual testing code
############################################################


def test_decrypt_char():
    alphabet = string.ascii_lowercase + string.ascii_uppercase

    result = decrypt_char("c", alphabet, 2)
    print(f"Expected char:  a")
    print(f"Decrypted char: {result}")
    print()

    result = decrypt_char("a", alphabet, 5)
    print(f"Expected char:  V")
    print(f"Decrypted char: {result}")
    print()


alphabet_1 = string.ascii_lowercase + string.ascii_uppercase
plaintext_1 = "easy"
ciphertext_1 = "gcuA"

alphabet_2 = alphabet_1 + string.punctuation
plaintext_2 = "This is a simple test."
ciphertext_2 = "Vjku ku c ukorng vguv:"

alphabet_3 = alphabet_2 + string.digits
plaintext_3 = "Without a doubt, 6.100 is the best subject ever! And the staff just amazing!!"
ciphertext_3 = "Ykvjqxw d grxew/ 9;445 nx ynk hkyA zBirmkB mDmz) Ivl Bpm ABioo sDBC jvjIrwp**"


def try_encrypt_decrypt(
    plaintext, ciphertext, alphabet, initial_shift, magic_number
):
    encrypted = encrypt(plaintext, alphabet, initial_shift, magic_number)
    decrypted = decrypt(encrypted, alphabet, initial_shift, magic_number)
    print(f"Original plaintext:  {plaintext}")
    print(f"Expected ciphertext: {ciphertext}")
    print(f"Encrypted text:      {encrypted}")
    print(f"Decrypted text:      {decrypted}")
    print()


def test_encrypt_decrypt():
    initial_shift = 2
    magic_number = 8
    print(f"{initial_shift = }, {magic_number = }")
    print()

    try_encrypt_decrypt(
        plaintext_1, ciphertext_1, alphabet_1, initial_shift, magic_number
    )
    try_encrypt_decrypt(
        plaintext_2, ciphertext_2, alphabet_2, initial_shift, magic_number
    )
    try_encrypt_decrypt(
        plaintext_3, ciphertext_3, alphabet_3, initial_shift, magic_number
    )


def test_count_words():
    text = "hello world"
    print(text)
    print(f"found {count_words(text)} words")
    print()

    text = 'Hello, "World\'s Fair"!'
    print(text)
    print(f"found {count_words(text)} words")
    print()


def try_break_cipher(ciphertext, alphabet, expected):
    decrypted = break_cipher(ciphertext, alphabet)
    print(f"Ciphertext:  {ciphertext}")
    print(f"Expected:    {expected}")
    print(f"Best guess:  {decrypted}")
    print()


def test_break_cipher():
    try_break_cipher(ciphertext_1, alphabet_1, plaintext_1)
    try_break_cipher(ciphertext_2, alphabet_2, plaintext_2)
    try_break_cipher(ciphertext_3, alphabet_3, plaintext_3)


if __name__ == "__main__":
    pass

    # Uncomment the function calls below to test manually.
    # Note these are not comprehensive tests.
    # Feel free to modify or extend them when debugging your code.
    # Run test.py to make sure your code passes all our test cases.

    # test_decrypt_char()
    # test_encrypt_decrypt()
    # test_count_words()
    # test_break_cipher()
