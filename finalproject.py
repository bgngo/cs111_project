#
# finalproject.py - Final Project
#
# authors: Gia Bao Ngo, Salvatore Cordova Quijano

import math

def clean_text(txt):
    """ returns a list containing the words in txt after it has been cleaned
        input: a string of text txt
    """
    for character in txt:
        if character in """.,?"'!;:""":
            txt = txt.replace(character, '')
    
    lowered_txt = txt.lower()
    
    split_txt = lowered_txt.split()
    
    return split_txt

def stem(s):
    """ returns the stem of s
        input: a string s
    """
    if len(s) > 4:
        if s[-4:] == 'itis':
            s = s[:-4]
        elif s[-3:] == 'ing':
            s = s[:-3]
        elif s[-2:] == 'er':
            s = s[:-2]
        elif s[-4:] == 'sses':
            s = s[:-2]
        elif s[-2:] == 'ss':
            s = s
        elif s[-1] == 's':
            s = s[:-1]
        elif s[-2:] == 'ed':
            s = s[:-2]
        elif s[-2:] == 'ly':
            s = s[:-2]
        elif s[-2:] == 'fy':
            s = s[:-2]
        elif s[-3:] == 'ize':
            s = s[:-3]
        elif s[-3:] == 'ise':
            s = s[:-3]
    
    return s

def compare_dictionaries(d1, d2):
    """ computes and returns the log similarity score of d1 and d2
        inputs: two feature dictionaries d1 and d2
    """
    if d1 == {}:
        return -50
    
    score = 0
    total = 0
    
    for word in d1:
        total += d1[word]
    
    for word in d2:
        if word in d1:
            individual_value = d1[word] / total
            score += d2[word] * math.log(individual_value)
        else:
            individual_value = 0.5 / total
            score += d2[word] * math.log(individual_value)
    
    return score

class TextModel:
    def __init__(self, model_name):
        """ constructs a new TextModel object
            input: a string model_name
        """
        self.name = model_name
        self.words = {}
        self.word_lengths = {}
        self.stems = {}
        self.sentence_lengths = {}
        self.exclams_and_questions = {}
     
    def __repr__(self):
        """ returns a string representation of the TextModel
        """
        s = 'text model name: ' + self.name + '\n'
        s += '  number of words: ' + str(len(self.words)) + '\n'
        s += '  number of word lengths: ' + str(len(self.word_lengths)) + '\n'
        s += '  number of stems: ' + str(len(self.stems)) + '\n'
        s += '  number of sentence lengths: ' + str(len(self.sentence_lengths)) + '\n'
        s += '  number of special marks: ' + str(len(self.exclams_and_questions)) + '\n'
        
        return s
    
    def add_string(self, s):
        """ analyzes s and adds its pieces to all of the dictionaries in this
            text model
            input: a string of text s
        """
        # counter for spaces in sentences
        number_of_spaces = 0
        for index in range(len(s)):
            if s[index] != ' ' and index == 0:
                number_of_spaces += 1
            if s[index] == ' ':
                number_of_spaces += 1
            elif s[index] in '!?.':
                if number_of_spaces not in self.sentence_lengths:
                    self.sentence_lengths[number_of_spaces] = 1
                else:
                    self.sentence_lengths[number_of_spaces] += 1
            
                number_of_spaces = 0
            
            if s[index] == '!':
                if '!' not in self.exclams_and_questions:
                    self.exclams_and_questions['!'] = 1
                else:
                    self.exclams_and_questions['!'] += 1
            elif s[index] == '?':
                if '?' not in self.exclams_and_questions:
                    self.exclams_and_questions['?'] = 1
                else:
                    self.exclams_and_questions['?'] += 1
        
        # cleans text
        word_list = clean_text(s)
        
        for word in word_list:
            if word not in self.words:
                self.words[word] = 1
            else:
                self.words[word] += 1
            
            if len(word) not in self.word_lengths:
                self.word_lengths[len(word)] = 1
            else:
                self.word_lengths[len(word)] += 1
            
            stem_of_word = stem(word)
            if stem_of_word not in self.stems:
                self.stems[stem_of_word] = 1
            else:
                self.stems[stem_of_word] += 1
    
    def add_file(self, filename):
        """ adds all of the text in filename to the model
            input: a text file filename
        """
        file = open(filename, 'r', encoding='utf8', errors='ignore')
        text = file.read()
        file.close()
        
        self.add_string(text)
    
    def save_model(self):
        """ defines a small dictionary and saves it to a file 
        """
        file1 = open(self.name + '_words', 'w')
        file1.write(str(self.words))
        file1.close()
        
        file2 = open(self.name + '_word_lengths', 'w')
        file2.write(str(self.word_lengths))
        file2.close()
        
        file3 = open(self.name + '_stems', 'w')
        file3.write(str(self.stems))
        file3.close()
        
        file4 = open(self.name + '_sentence_lengths', 'w')
        file4.write(str(self.sentence_lengths))
        file4.close()
        
        file5 = open(self.name + '_exclams_and_questions', 'w')
        file5.write(str(self.exclams_and_questions))
        file5.close()
    
    def read_model(self):
        """ reads a dictionary and converts it to an actual dictionary object
        """
        f1 = open(self.name + '_words', 'r')
        d1_str = f1.read()
        f1.close()
        
        self.words = dict(eval(d1_str))
        
        f2 = open(self.name + '_word_lengths', 'r')
        d2_str = f2.read()
        f2.close()
        
        self.word_lengths = dict(eval(d2_str))
        
        f3 = open(self.name + '_stems', 'r')
        d3_str = f3.read()
        f3.close()
        
        self.stems = dict(eval(d3_str))
        
        f4 = open(self.name + '_sentence_lengths', 'r')
        d4_str = f4.read()
        f4.close()
        
        self.sentence_lengths = dict(eval(d4_str))
        
        f5 = open(self.name + '_exclams_and_questions', 'r')
        d5_str = f5.read()
        f5.close()
        
        self.exclams_and_questions = dict(eval(d5_str))
    
    def similarity_scores(self, other):
        """ computes and returns a list of log similarity scores measuring the
            similarity of self and other
        """
        word_score = compare_dictionaries(other.words, self.words)
        word_lengths_score = compare_dictionaries(other.word_lengths, self.word_lengths)
        stem_score = compare_dictionaries(other.stems, self.stems)
        sentence_lengths_score = compare_dictionaries(other.sentence_lengths, self.sentence_lengths)
        marks_score = compare_dictionaries(other.exclams_and_questions, self.exclams_and_questions)
        
        return_list = []
        return_list += [word_score]
        return_list += [word_lengths_score]
        return_list += [stem_score]
        return_list += [sentence_lengths_score]
        return_list += [marks_score]
        
        return return_list
    
    def classify(self, source1, source2):
        """ compares the called TextModel object (self) to two other “source”
            TextModel objects (source1 and source2) and determines which of
            these other TextModels is the more likely source of the called
            TextModel
        """
        scores1 = self.similarity_scores(source1)
        scores2 = self.similarity_scores(source2)
        
        print('scores for', source1.name, ':', scores1)
        print('scores for', source2.name, ':', scores2)
        
        weighted_sum1 = 8*scores1[0] + 6*scores1[1] + 5*scores1[2] + 7*scores1[3] + 7*scores1[4]
        weighted_sum2 = 8*scores2[0] + 6*scores2[1] + 5*scores2[2] + 7*scores2[3] + 7*scores2[4]
        
        if weighted_sum1 > weighted_sum2:
            print(self.name, 'is more likely to have come from', source1.name)
        elif weighted_sum2 > weighted_sum1:
            print(self.name, 'is more likely to have come from', source2.name)
        elif weighted_sum2 == weighted_sum1:
            print('weird...')

#def test():
    #""" your docstring goes here """
    #source1 = TextModel('source1')
    #source1.add_string('It is interesting that she is interested.')

    #source2 = TextModel('source2')
    #source2.add_string('I am very, very excited about this!')

    #mystery = TextModel('mystery')
    #mystery.add_string('Is he interested? No, but I am.')
    #mystery.classify(source1, source2)

def run_tests():
    """ performs tests
    """
    source1 = TextModel('friends')
    source1.add_file('friends.txt')

    source2 = TextModel('himym')
    source2.add_file('himym.txt')

    new1 = TextModel('himym_pilot')
    new1.add_file('himym_pilot.txt')
    new1.classify(source1, source2)
    print()
    
    new2 = TextModel('friends106')
    new2.add_file('friends106.txt')
    new2.classify(source1, source2)
    print()
    
    new3 = TextModel('friends107')
    new3.add_file('friends107.txt')
    new3.classify(source1, source2)
    print()
    
    new4 = TextModel('friends108')
    new4.add_file('friends108.txt')
    new4.classify(source1, source2)
