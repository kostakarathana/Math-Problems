
CENSORED_WORDS = {
    "fuck", "fucks", "fucking", "fucked", "motherfucking", "motherfucker", "fucker", "fuckface", "fuckhead", "fuckwit", "fucktard", "fuckbag", "fuckboy", "fuckstick", "fucknut", "clusterfuck",
    "shit", "shits", "shitty", "shitting", "shithead", "shitbag", "shitstain", "shitface", "shitass", "shitshow", "horseshit", "bullshit", "batshit", "dumbshit", "ape-shit",
    "bitch", "bitches", "bitching", "bitchboy", "bitchass", "dumbbitch", "slutbitch", "hoe-bitch", "whinybitch",
    "asshole", "assholes", "asshat", "asswipe", "assclown", "asslicker", "assmunch", "assfuck", "asslick", "assbreath",
    "bastard", "bastards", "sonofabitch", "sumbitch", "cock-sucker", "cocksucker", "cocksucking", "cocksuck", "cockhead", "cockface", "cockboy",
    "pussy", "pussies", "pussyhole", "pussylicker", "pussified", "pussyfart", "pussywhipped", "pussyass",
    "cunt", "cunts", "cunting", "cuntface", "cuntbag", "cuntlicker", "cuntmunch", "cuntwhore", "twat", "twats", "twatting", "twatface", "twatmunch",
    "slut", "sluts", "slutting", "slutbag", "slutface", "cumslut", "slutwhore",
    "whore", "whores", "whoring", "manwhore", "fuckwhore", "cumwhore",
    "douche", "douchebag", "douchelord", "douchecanoe", "douchefucker",
    "prick", "pricks", "prickhead", "prickface", "prickass",
    "bollocks", "bollocking", "bollockhead", "bollockface",
    "wanker", "wankers", "wanking", "wankstain", "wankface",
    "tosser", "tossers", "tossing", "tosspot",
    "skank", "skanks", "skanky", "skankwhore", "skankbag",
    "tramp", "tramps", "trampy",
    "dyke", "dykes", "faggot", "fags", "faggy", "faglord", "buttfag",
    "homo", "homo-ass", "queer", "queers", "tranny", "shemale", "ladyboy",
    "chink", "gook", "spic", "wetback", "kike", "heeb", "nigger", "nigga", "nigs", "coon", "jigaboo", "porchmonkey", "sambo", "tarbaby",
    "redneck", "cracker", "honky", "hillbilly", "white trash", "guttertrash",
    "gypsy", "retard", "retards", "retarded", "spaz", "mongoloid", "freak", "weirdo", "mutant",
    "fatass", "lardass", "fatfuck", "fatty", "blubberass", "pigfuck", "cowfuck",
    "beaner", "zipperhead", "jap", "kraut", "polack", "paki", "camel jockey", "raghead", "sandnigger", "terrorist", "islamist",
    "nazi", "neo-nazi", "kkk", "slave", "slaver", "ape", "monkey", "gorilla", "chimpy",
    "dog", "bitchdog", "pigdog", "sow", "cow", "heifer", "donkeyfucker", "goatfucker", "sheepfucker",
    "cum", "cumdump", "cumslut", "cumguzzler", "cumbucket", "cumrag", "cumsock", "cumbrain", "cumwhore", "cumdrinker",
    "jizz", "jizzes", "jizzed", "spunk", "spooge", "wank", "wanks", "wanked", "wanking",
    "jackoff", "jerkoff", "jerking", "circlejerk", "circlejerking",
    "buttfuck", "buttfucker", "fistfuck", "fistfucker", "rimjob", "felch", "felcher", "felching", "anilingus", "deepthroat",
    "blowjob", "blowjobs", "blowfucker", "pisses", "half-ass","handjob", "handjobs",
    "rape", "rapes", "raping", "rapist", "molester", "pedophile", "pedo", "incest", "bestiality", "zoophile", "necrophile", "necrophilia",
    "orgy", "gangbang", "train", "sodomy", "buggery", "anal", "buttplug", "dildo", "vibrator", "sex toy", "strapon", "bdsm", "bondage", "gimp", "dominatrix", "submissive",
    "methhead", "crackhead", "dopehead", "junkie", "tweaker", "smackhead", "pillpopper", "pillhead",
    "wasted", "trashed", "shitfaced", "hammered", "sloshed", "fuckedup", "blitzed", "zooted", "lit", "faded",
    "loser", "failure", "dumbass", "stupidass", "jackass", "dipshit", "fuckstick", "shitstick", "knobhead", "bellend", "arsehole",
    "git", "muppet", "plonker", "fucklord", "schmuck", "puto", "cabron", "maricon", "pendejo", "chingado", "chingar", "mierda", "culo", "coño", "verga", "joto", "zorra", "perra", "puta", "chingona", "pinche",
    "madarchod", "bhenchod", "chutiya", "gaand", "randi", "gandu", "kuttiya", "lund", "choot", "lavda", "suar", "harami", "kamina", "saala", "bakrichod",
    "fucklord", "shitlord", "edge-lord", "fuckqueen", "pisslord", "cocklord"
}

def censor_text(text: str):
    text = [word for word in text.split(' ') if word != '']
    new_text = ""
    for i, word in enumerate(text):
        if word.lower() not in CENSORED_WORDS:
            new_text += word + " "
        else:
            new_text += word[0] + "*" * (len(word) - 2) + word[-1] + " "
    return new_text

if __name__ == "__main__":
    print(censor_text("I swear, nothing pisses me off more than when people half-ass their shit and then act like they’ve climbed fucking Everest. Like, don’t come at me bragging about how “busy” you are when all you did was scroll through TikTok and send a couple of shitty emails. Own your crap, do the fucking work, and maybe then you’ll actually have something worth opening your mouth about."))

