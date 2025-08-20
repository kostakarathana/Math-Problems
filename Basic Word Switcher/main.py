SYNONYMS = {
    "complex": "complicated",
    "happy": "joyful",
    "sad": "sorrowful",
    "angry": "irate",
    "fast": "swift",
    "slow": "sluggish",
    "smart": "intelligent",
    "dumb": "stupid",
    "easy": "effortless",
    "hard": "difficult",
    "strong": "sturdy",
    "weak": "frail",
    "big": "enormous",
    "small": "tiny",
    "old": "ancient",
    "new": "novel",
    "rich": "wealthy",
    "poor": "destitute",
    "tired": "exhausted",
    "energetic": "vigorous",
    "hungry": "famished",
    "thirsty": "parched",
    "clean": "immaculate",
    "dirty": "filthy",
    "beautiful": "gorgeous",
    "ugly": "hideous",
    "brave": "courageous",
    "cowardly": "timid",
    "hot": "scorching",
    "cold": "freezing",
    "funny": "humorous",
    "serious": "solemn",
    "quiet": "silent",
    "loud": "boisterous",
    "calm": "tranquil",
    "nervous": "anxious",
    "important": "crucial",
    "unimportant": "trivial",
    "famous": "renowned",
    "unknown": "obscure",
    "true": "genuine",
    "false": "phony",
    "correct": "accurate",
    "wrong": "erroneous",
    "lucky": "fortunate",
    "unlucky": "unfortunate",
    "interesting": "fascinating",
    "boring": "tedious",
    "friendly": "amiable",
    "unfriendly": "hostile",
    "kind": "benevolent",
    "mean": "malicious",
    "honest": "truthful",
    "dishonest": "deceitful",
    "brilliant": "ingenious",
    "stupid": "idiotic",
    "richness": "affluence",
    "poverty": "impoverishment",
    "begin": "commence",
    "end": "terminate",
    "buy": "purchase",
    "sell": "vend",
    "give": "donate",
    "take": "seize",
    "love": "adore",
    "hate": "detest",
    "think": "contemplate",
    "know": "understand",
    "see": "perceive",
    "hear": "listen",
    "say": "utter",
    "speak": "converse",
    "walk": "stroll",
    "run": "sprint",
    "jump": "leap",
    "sit": "perch",
    "stand": "arise",
    "sleep": "slumber",
    "eat": "consume",
    "drink": "imbibe",
    "write": "compose",
    "read": "peruse",
    "build": "construct",
    "destroy": "annihilate",
    "fix": "repair",
    "break": "shatter",
    "win": "triumph",
    "lose": "fail",
    "help": "assist",
    "hurt": "damage",
    "teach": "instruct",
    "learn": "absorb",
    "show": "demonstrate",
    "hide": "conceal",
    "open": "unseal",
    "close": "shut",
    "start": "initiate",
    "stop": "cease"
}

def reword_text(text: str, skip_words: int = 1):
    '''
    Takes in a text, replaces some common words with the synonym of
    that word.

    Parameters:
        text (str): The text to be reworded (assumed good input, i.e. no trailing spaces, double spaces, etc.)
        skip_words (int): The number of words to skip when reworded (if user wants more subtle changes)
    '''
    # reformat
    text = [word for word in text.split(" ")]
    encountered = 0
    for i, word in enumerate(text):
        if word in SYNONYMS:
            encountered += 1
            if encountered % skip_words == 0:
                text[i] = SYNONYMS[word]
    new_text = ""
    for word in text:
        new_text += word + " "
    return new_text

if __name__ == "__main__":
    txt = "Hi I am Kosta and I show my friends how to start a game"
    new_text = reword_text(txt)
    print(new_text)