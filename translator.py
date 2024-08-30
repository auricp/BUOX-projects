import sys

# translation table for English to Braile directly from alphabet posted on github
ENGLISH_TO_BRAILE = {
    'a': 'O.....',
    'b': 'O.O...',
    'c': 'OO....',
    'd': 'OO.O..',
    'e': 'O..O..',
    'f': 'OOO...',
    'g': 'OOOO..',
    'h': 'O.OO..',
    'i': '.OO...',
    'j': '.OOO..',
    'k': 'O...O.',
    'l': 'O.O.O.',
    'm': 'OO..O.',
    'n': 'OO.OO.',
    'o': 'O..OO.',
    'p': 'OOO.O.',
    'q': 'OOOOO.',
    'r': 'O.OOO.',
    's': '.OO.O.',
    't': '.OOOO.',
    'u': 'O...OO',
    'v': 'O.O.OO',
    'w': '.OOO.O',
    'x': 'OO..OO',
    'y': 'OO.OOO',
    'z': 'O..OOO',
    ' ': '......',
    '.': '..OO.O',
    '1': 'O.....',
    '2': 'O.O...',
    '3': 'OO....',
    '4': 'OO.O..',
    '5': 'O..O..',
    '6': 'OOO...',
    '7': 'OOOO..',
    '8': 'O.OO..',
    '9': '.OO...',
    '0': '.OOO..',
}


# Create the braile to english dict by reversing the english to braile dict and not including numbers
BRAILE_TO_ENGLISH = {braile : english for english,braile in ENGLISH_TO_BRAILE.items() if not english.isdigit()}

# Create the braile to english digit dict in a similar way as above
BRAILE_TO_ENGLISH_DIGIT = {braile : english for english,braile in ENGLISH_TO_BRAILE.items() if english.isdigit()}

def englishToBraile(s):
    result = ''
    
    for i,char in enumerate(s):
        
        # check if character is a letter
        if char.isalpha():
            
            # if its a letter, first check if its a capital
            if char.isupper():
                
                # if its a capital, add the capital comes next to the string and then the character
                result += '.....O'
            
            # then append the proper alphabet character to the result
            result += ENGLISH_TO_BRAILE[char.lower()]
        
        # other cases are if its a digit, a space, or a period
        
        # need to add case for number
        
        elif char.isdigit():
            # first append digit identifier only if its the first digit
            if i == 0 or not s[i-1].isdigit():
                result += '.O.OOO'
            
            # then append digit
            result += ENGLISH_TO_BRAILE[char]
            
            
        else:
            result += ENGLISH_TO_BRAILE[char]
            
    return result


def braileToEnglish(s):
    string = ''
    # make s a list
    # parse 6 characters at a time and then delete them
    
    while s:
        current = s[:6]
        #print(current)
        
        # need to check if a capital follows, or a number follows (maybe decimal but have it already in dict)
        
        # check if a capital follows
        if current == '.....O':
            
            # delete the 6 that notify of a capital
            s = s[6:]
            
            # find the next 6 and translate
            current = s[:6]
            
            string += BRAILE_TO_ENGLISH[current].upper()
        
        # check if a number follows
        elif current == '.O.OOO':
            # assume all are numbers until the next space
            # delete current
            s = s[6:]
            
            # get next digit
            current = s[:6]
            
            # while current is not a space
            while current != '......' and current != '':

                # use alternative dict to add number
                string += BRAILE_TO_ENGLISH_DIGIT[current]
                
                # delete added number
                s = s[6:]
                
                # get new current
                current = s[:6]
        
        else:
            # just do it normally
            string += BRAILE_TO_ENGLISH[current]
        
        s = s[6:]
        
        
    return string



def main():
    if len(sys.argv) != 2:
        print('Need a string')
        return
    
    string = sys.argv[1]
    #print(englishToBraile(string))
    print(braileToEnglish(string))

if __name__ == '__main__':
    main()


# .....OO.....O.O...OO...........O.OOOO.....O.O...OO....