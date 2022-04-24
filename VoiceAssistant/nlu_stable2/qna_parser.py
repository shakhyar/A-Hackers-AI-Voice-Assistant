class Parser:
    def __init__(self):
        self.answer = None
        self.aux_verbs = ["is", "are", "was", "were", "has", "have", "had", "can", "could", "should", "would", "shall",
                          "will", "might", "may"]
        self.question_words = ["who", "where", "which", "whom", "how", "what"]
        self.question = None
        self.first_person = {"i": "you ", "me": "you", "my": "your", "mine": "yours", "myself": "yourself"}
        self.second_person = ['i', 'me', 'my', 'mine', 'myself']
        self.answer_list = []

    def parse_question(self, question):
        """
        :param question:
        :return:
        """
        self.question = str(question).lower()
        for i in self.question_words:
            if i in self.question:
                for j in self.aux_verbs:
                    if (i + " " + j) in self.question:
                        return self.question[self.question.index(i + " " + j) + len(i + " " + j + " "):]
                else:
                    return self.question[self.question.index(i + " ") + len(i + " "):]

    def parse_answer(self, answer):
        self.answer = str(answer).lower()
        self.answer_list = self.answer.split(" ")
        for i in self.answer_list:
            for j in self.first_person:
                if j == i:

                    self.answer_list.insert(self.answer_list.index(i), self.first_person[j])
                    self.answer_list.remove(self.answer_list[self.answer_list.index(i)])
                else:
                    pass
        self.answer = " ".join(self.answer_list)
        return self.answer


