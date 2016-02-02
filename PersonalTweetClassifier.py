__author__ = 'Ben Ahlbrand'
from FileFunc import FileFunc
import os
import csv

invalidRepetitions = [".", ">"]


class PersonalTweetClassifier:
    def __init__(self):
        os.chdir("data")

        # slang data from https://floatcode.wordpress.com/tag/dataset/
        with open("../data/slang.txt", 'rt') as f:
            reader = csv.reader(f, delimiter='`', quoting=csv.QUOTE_NONE)
            self.slang = [row[0] for row in reader]

        self.intensifiers = FileFunc.read_file_into_list("../data/intensifier.txt")
        self.exclamations = FileFunc.read_file_into_list("../data/exclamatoryWord.txt")
        self.modalVerbs = FileFunc.read_file_into_list("../data/modalVerb.txt")
        self.pronouns = FileFunc.read_file_into_list("../data/pronoun.txt")
        self.emoticons = FileFunc.read_file_into_list("../data/emoticon.txt")

    def punctuation_rule(self):
        pass

    @staticmethod
    def repeated_character_rule(term):
        if len(term) < 3:
            return False

        i = 0
        while i < len(term) - 2:
            if term[i] not in invalidRepetitions and term[i + 1] == term[i] and term[i + 2] == term[i]:
                return True
            i += 1

        return False

    def filter(self, term):
        if term in self.intensifiers:
            return True

        if term in self.exclamations:
            return True

        if term in self.modalVerbs:
            return True

        # if term in self.pronouns:
        #     return True

        if term in self.emoticons:
            return True

        if self.repeated_character_rule(term):
            return True

        if len(term) > 1 and term in self.slang:
            return True

        if len(term) > 3 and term.isupper():
            return True

        return False

if __name__ == '__main__':
    personals = PersonalTweetClassifier()
    os.chdir("..")

    count = 0

    for tweet in FileFunc.read_file_into_list("test_data.txt"):
        for term in tweet.split():
            if personals.filter(term):
                print(tweet)
                count += 1
                break
    print()
    print(count, "'personal' tweets found")

# latent factor model http://ijcai.org/papers15/Papers/IJCAI15-322.pdf
# http://dl.acm.org/citation.cfm?id=1858724
# VADER http://comp.social.gatech.edu/papers/icwsm14.vader.hutto.pdf