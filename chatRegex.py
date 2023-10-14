import html
import sys
import time
import requests as req
from bs4 import BeautifulSoup as bs
import re

class ChatRegex:
    def __init__(self) -> None:
        self.processRun = True
        self.bookStore = {}
        self.onlyAlphabets = r'\b([A-Za-z]+)\b'
        self.chapters = []

    def spinningCursor(self):
        while True:
            for cursor in '|/-\\': yield cursor

    def extractUrl(self, url):
        response = req.get(url)
        html_content = response.content
        soup = bs(html_content, 'html.parser')

        # Step 3: Identify HTML structure containing chapter names and content
        # Assuming chapters are within <div class="chapter"> elements
        chapter_divs = soup.find_all('div', class_='chapter')

        # Step 4: Extract chapter names and content
        chapters = []
        pattern = r'(Chapter\s+[IVXLCDM\d]+\s*\.?\s*|\b[A-Za-z]+\b)'
        for chapter_div in chapter_divs:
            chapter_name = chapter_div.find('h2').text if chapter_div.find('h2') else None
            if chapter_name is not None and re.findall(pattern, chapter_name):
                chapter_content = ' '.join([html.unescape(p.text.strip()) for p in chapter_div.find_all('p')]) if chapter_div.find_all('p') else None
                chapter_name = chapter_name.replace("\n", "")
                chapters.append({"chapterName": chapter_name, "chapterContent": chapter_content})
        # for i, chapter in range(chapters):
        #     print(chapter.chapterName)
        return chapters

    def print_red(text):
        print(f"\033[91m{text}\033[0m")

    def loadData(self, url):
        spinner = self.spinningCursor()
        for _ in range(50):
            sys.stdout.write(next(spinner))
            sys.stdout.flush()
            time.sleep(0.1)
            sys.stdout.write('\b')
        #List of chapters and contents as {"chapterName":"" , "chapterContent": ""}
        self.chapters = self.extractUrl(url)

        #for chapter in self.chapters:
        #    print(f"Chapter Name: {chapter['chapterName']}")
        #    print(f"Chapter Content: {chapter['chapterContent']}")    
        
    def processQuery(self, query, novel_selection):
        if novel_selection == '1':
            investigator = 'Sherlock Holmes'
            investigator2 = 'John Watson'
            crime = 'Death' #'Murder', 'Killing'
            perpetrator = r'\b(?:(John |Mr. )?Stapleton|Rodger( Baskerville)?)\b'
            suspect1 = 'James Mortimer'
            suspect2 = 'Beryl Stapleton'
            suspect3 = 'Henry Baskerville'
            suspect4 = 'Mr. Barrymore'
            suspect5 = 'Mrs. Barrymore'
        elif novel_selection == '2':
            investigator = r'\b(?:(the )?Young Adventurers(, Ltd.)?|(Mr.)?(Tommy|Thomas)( Beresford)?|(Miss )?Prudence( Cowley)?|(Miss )?Tuppence)\b'
            crime = r'\b(?:Labour Unrest|Revolution(s)?|(Labour )?coup?)\b'
            perpetrator = r'\b(?:(Mr. )?Brown|(Sir )?James( Peel Edgerton)?)\b'
            suspect1 = r'\b(?:(Mr. )?((Edward )?Whittington))\b'
            suspect2 = r'\b(?:(Mr. )?(Julius P. |Julius )?Hersheimmer)\b'
            suspect3 = r'\b(?:Jane( Finn)?)\b'
        elif novel_selection == '3':
            investigator = r'\b(?:(Monsieur |Hercule )?Poirot)\b'
            crime = r'\b(?:(strychnine )?(poisoned|poisoning)?|(Wilful )?Murder(ing|ed)?|Killed)\b'
            perpetrator = r'\b(?:Mr. Alfred Inglethorp|Alfred Inglethorp|Alfred|Mr. Inglethorp|Miss Howard|Evelyn( Howard)?)\b'
            suspect1 = r'\b(?:(Mr.( John)?|John|(Mrs. )?Lawrence) Cavendish|Cavendishes)\b'
            suspect2 = r'\b(?:(Miss|Evelyn) Howard|Evelyn)\b'
            suspect3 = r'\b(?:Mrs. Raikes)\b'

        #Question Parsing
        q1 = r'^(?=.*\bwhen\b)(?=.*\b(investigator(s)?|pair|duo|partner(s)?|detective(s)?)\b)(?=.*\bfirst\b)(?=.*\b(mention(ed)?|appear(s)?|occur(s)?|show(s)? up|shown|introduce(d)?|arrive(s)?)\b)'
        q2 = r'^(?=.*\bwhen\b)(?=.*\b(crime(s)?|theft(s)?|burglary|burglaries|murder(s)?|attack(s)?)\b)(?=.*\bfirst\b)(?=.*\b(mention(ed)?|appear(s)?|occur(s)?|show(s)? up|shown|introduce(d)?|arrive(s)?|happen(s)?)\b)'
        q3 = r'^(?=.*\bwhen\b)(?=.*\b(perpetrator(s)?|criminal(s)?|thief(s)?|murderer(s)?|attacker(s)?|burglar(s)?)\b)(?=.*\bfirst\b)(?=.*\b(mention(ed)?|appear(s)?|occur(s)?|show(s)? up|shown|introduce(d)?|arrive(s)?)\b)'
        q4 = r'^(?=.*\bwhat\b)(?=.*\bthree\b)(?=.*\bwords\b)(?=.*\b(mention(ed)?|appear(s)?|occur(s)?|show(s)? up|shown|introduce(d)?|happen(s)?)\b)(?=.*\b(perpetrator(s)?|criminal(s)?|thief(s)?|murderer(s)?|attacker(s)?|burglar(s)?)\b)'
        q5 = r'^(?=.*\bwhen\b)(?=.*\b(investigator(s)?|pair|duo|partner(s)?|detective(s)?)\b)(?=.*\b(perpetrator(s)?|criminal(s)?|thief(s)?|murderer(s)?|attacker(s)?|burglar(s)?)\b)(?=.*\b(co |co-)?(together|mention(ed)?|appear(s)?|occur(s)?|show(s)? up|shown|introduce(d)?|arrive(s)?)\b)'
        q6 = r'^(?=.*\bwhen\b)(?=.*\b(suspect(s)?|accused|defendant(s)?)\b)(?=.*\bfirst\b)(?=.*\b(mention(ed)?|appear(s)?|occur(s)?|show(s)? up|shown|introduce(d)?|arrive(s)?)\b)'

        if re.search(q1, query, re.IGNORECASE):
            print("When does the investigator (or a pair) occur for the first time -  chapter #, the sentence(s) # in a chapter")
        elif re.search(q2, query, re.IGNORECASE):
            print("When is the crime first mentioned - the type of the crime and the details -  chapter #, the sentence(s) # in a chapter")
        elif re.search(q3, query, re.IGNORECASE):
            print("When is the perpetrator first mentioned - chapter #, the sentence(s) # in a chapter")
        elif re.search(q4, query, re.IGNORECASE):
            count = 0
            for chapter in self.chapters:
                if(count == 0):
                    book_text = ""
                else:
                    book_text = book_text + " " + chapter['chapterContent']
                count = count + 1

            matches = re.finditer(perpetrator, book_text)
            count = 0
            for match in matches:
                count = count + 1
                words_before = re.findall(r'\w+', book_text[:match.start()])[-3:]
                words_after = re.findall(r'\w+', book_text[match.end():])[:3]

                print("Match ", count, ". Words before match: ", words_before, sep = '')
                print("Match ", count, ". Words after match:  ", words_after, sep = '')
        elif re.search(q5, query, re.IGNORECASE):
            print("When and how the detective/detectives and the perpetrators co-occur - chapter #, the sentence(s) # in a chapter")
        elif re.search(q6, query, re.IGNORECASE):
            print("When are other suspects first introduced - chapter #, the sentence(s) # in a chapter")
        else:
            print("I am unable to answer that question")

        #print(self.bookStore['selected_novel']) #Get text
        return 
    
    def run(self, novel_selection):
        while self.processRun:
            print("Type 'exit' or 'quit' to terminate\n")
            queryString = input("Enter the query: ")
            if not re.match(self.onlyAlphabets, queryString):
                self.print_red("Please enter only english characters")

            if queryString == "quit" or queryString == "exit":
                self.processRun = False
            else:
                self.processQuery(queryString, novel_selection)

        print("Chat completed..!\n")

chat = ChatRegex()

novel_selection = input("Select a novel to analyze(1-3): \n1. The Hound of the Baskervilles by Arthur Conan Doyle\n2. The Secret Adversary, by Agatha Christie\n3. The Mysterious Affair at Styles by Agatha Christie\nSelection: ")

while novel_selection not in ('1', '2', '3'):
    print("\nThat input was not valid. Enter a number 1-3 corresponding to a novel below")
    novel_selection = input("Select a novel to analyze(1-3): \n1. The Hound of the Baskervilles by Arthur Conan Doyle\n2. The Secret Adversary, by Agatha Christie\n3. The Mysterious Affair at Styles by Agatha Christie\nSelection: ")

print()

if novel_selection == '1': #The Hound of Baskervilles - Arthur Conan Doyle
    chat.loadData("https://www.gutenberg.org/cache/epub/2852/pg2852-images.html")
elif novel_selection == '2': #The Secret Adversary - Agatha Christie
    chat.loadData("https://www.gutenberg.org/cache/epub/1155/pg1155-images.html")
elif novel_selection == '3': #The Mysterious Affair at Styles - Agatha Christie
    chat.loadData("https://www.gutenberg.org/cache/epub/863/pg863-images.html")


chat.run(novel_selection)
