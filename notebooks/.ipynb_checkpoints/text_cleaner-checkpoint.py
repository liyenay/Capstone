import pandas as pd
import re
from bs4 import BeautifulSoup
import spacy
from nltk.corpus import stopwords

class TextCleaner:

    def __init__(self, df, text_column):
        self.df = df
        self.text_column = text_column
    
    # this removes html links, numbers, non alphanumeric and make the words in lowercase
    def clean_text(self, raw_text):
        # Check if the value is NaN
        if pd.isna(raw_text):
            return raw_text

        # 1. Remove HTML.
        text = BeautifulSoup(str(raw_text), features="lxml").get_text()

        # 2. Remove URLs.
        no_urls = re.sub("http\S+", " ", text)

        # 3. Remove non-letters.
        letters_only = re.sub("[^a-zA-Z]", " ", no_urls)

        # 4. Convert to lower case, split into individual words.
        words = letters_only.lower().split()

        # 5. Stopwords to be removed.
        stops = set(stopwords.words('english'))

        # 6. Remove stopwords.
        meaningful_words = [w for w in words if not w in stops]

        # 8. Join the words back into one string separated by space,
        # and return the result.
        return " ".join(meaningful_words)

    def text_lem_spacy(self, text):
        # Check if the value is NaN
        if pd.isna(text):
            return ""

        doc = self.nlp(text)
        lemmatized_text = ' '.join([token.lemma_ for token in doc])
        return lemmatized_text

    def word_count(self):
        self.df['word_count'] = [len(s.split()) for s in self.df[self.text_column]]

    def clean_lemmatize_text(self):
        # Clean text
        self.df['cleaned_text'] = self.df[self.text_column].map(self.clean_text)

        # Load spaCy model
        self.nlp = spacy.load("en_core_web_sm")

        # Lemmatize text
        self.df['cleaned_lem_text'] = self.df['cleaned_text'].map(self.text_lem_spacy)

        # Calculate word count
        self.word_count()

    def clean_lemmatize_header(self):
        # Clean text
        self.df['cleaned_heading'] = self.df['review_heading'].map(lambda x: self.clean_text(x) if pd.notna(x) else x)

        # Load spaCy model
        self.nlp = spacy.load("en_core_web_sm")

        # Lemmatize text
        self.df['cleaned_lem_heading'] = self.df['cleaned_heading'].map(lambda x: self.text_lem_spacy(x) if pd.notna(x) else x)
