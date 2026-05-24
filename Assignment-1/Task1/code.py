import re

class WordCounter:
    def __init__(self, file_path):
        with open(file_path, 'r') as file:
            self.file_content = file.read()
    
    def url_and_mail_removal(self, text):
        email_pattern = r"[a-zA-Z0-9.-_%+]+@[a-zA-Z0-9-.]+\.[a-zA-Z]{2,}"
        url_pattern = r"(?:https?://|www\.)[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}[a-zA-Z0-9./?=#%&+-]*(?<!\.)"
        result_email = re.sub(email_pattern,'', text)
        result = re.sub(url_pattern,'', result_email)
        self.url_and_mail_removed = result
        return result

    def convert_to_lowercase(self, text):
        result = text.lower()
        self.converted_to_lowercase = result
        return result

    def number_removal(self, text):
        number_pattern = r"\d"
        result = re.sub(number_pattern, '', text)
        self.removed_numbers = result
        return result

    def punctuation_removal(self, text):
        punctuation_pattern = r"[^\w\s\d]"
        result = re.sub(punctuation_pattern, '', text)
        self.removed_punctuation = result
        return result

    def pipeline_func(self):
        result = self.file_content
        list_of_functions = [self.url_and_mail_removal, self.convert_to_lowercase, self.number_removal, self.punctuation_removal]
        for function in list_of_functions:
            result = function(result)
        self.final_cleaned_text = result
        return result
    
    def mapping_phase(self):
        text = self.pipeline_func()
        words_list = text.split()
        filtered_words = filter(lambda word: len(word)>2 and word.isprintable(), words_list)
        mapped_words = map(lambda word: (word, 1), filtered_words)
        self.list_of_words = list(mapped_words)
        return self.list_of_words
    
    def reduce_phase(self):
        if not hasattr(self, 'list_of_words'):
            self.mapping_phase()
        groupped_words = {}
        for word in self.list_of_words:
            if word[0] in groupped_words:
                groupped_words[word[0]].append(1)
            else:
                groupped_words[word[0]] = [1]
        sorted_groupped_words = dict(sorted(groupped_words.items()))
        final_words_count = {}
        for word in sorted_groupped_words.items():
            final_words_count[word[0]] = sum(word[1])
        return final_words_count


instance = WordCounter('dataset.txt')
with open("1.urlAndMailRemoved.txt", 'w') as file1, open("2.lowerCaseConverted.txt", 'w') as file2, open("3.numbersRemoved.txt", 'w') as file3, open("4.punctuationRemoved.txt", 'w') as file4, open("5.pipelineResult.txt", 'w') as file5, open("6.mappingPhase.txt", 'w') as file6:
    file1.write(instance.url_and_mail_removal(instance.file_content))
    file2.write(instance.convert_to_lowercase(instance.file_content))
    file3.write(instance.number_removal(instance.file_content))
    file4.write(instance.punctuation_removal(instance.file_content))
    file5.write(instance.pipeline_func())
    file6.write(str(instance.mapping_phase()))

with open('7.finalCsv.csv', 'w') as csv:
    csv.write("Word,Count\n")
    for word, count in instance.reduce_phase().items():
        csv.write(f"{word},{count}\n")

#since I can't upload .csv in Moodle, I am gonna write the final result in text file
with open('7.finalCsv.txt', 'w') as csv:
    csv.write("Word,Count\n")
    for word, count in instance.reduce_phase().items():
        csv.write(f"{word},{count}\n")


    
