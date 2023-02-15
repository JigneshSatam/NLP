import pickle
import re
import os
from db.knowledge_base import KnowledgeBase
import pandas as pd

from bs4 import BeautifulSoup
from urllib import request
from fake_useragent import UserAgent
from nltk import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer


class Crawler:
  url_file = "data/urls.txt"
  document_directory: str = "data/documents"
  clean_document_directory: str = "data/clean-documents"
  knowledge_base_file: str = "data/knowledge_base.pickle"

  def __init__(self, base_url: str) -> None:
    self.base_url = base_url
    self.relevant_articles: list[str] = []
    self.queue: list[str] = [base_url]
    self.document_tokens: list[str] = []
    self.corpus: list[str] = []
    self.knowledge_base: dict[list[str]] = {}
    # self.ua = UserAgent()

  def crawl(self, max_limit: int) -> None:
    # self.set_relevant_articles(max_limit)
    # self.save_urls()
    # # print(self.relevant_articles)
    # # print(len(self.relevant_articles))
    # self.crawl_relevant_articles()
    # self.clean_documents()
    # self.extract_all_documents_tokens()
    # self.calculate_tf_idf()
    self.create_knowledge_base()

  def get_headers(self) -> dict[str, str]:
    ua = UserAgent()
    return {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://www.google.com/',
        'Connection': 'keep-alive',
        'User-Agent': ua.random
    }
    # 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Safari/605.1.15',
    # 'Host': 'www.space.com',

  def set_relevant_articles(self, max_limit) -> None:
    while (len(self.relevant_articles) < max_limit and len(self.queue) > 0):
      url = self.queue.pop(0)
      req = request.Request(url, headers=self.get_headers())
      try:
        html = request.urlopen(req).read().decode("utf8")
      except:
        print("An error occurred with link", req)
        continue
      soup = BeautifulSoup(html, features="html.parser")
      page_urls = soup.find_all('a')
      while (len(self.relevant_articles) < max_limit and len(page_urls) > 0):
        link = page_urls.pop(0)
        link_str = str(link.get('href'))
        # print(link_str)
        if "facebook" in link_str \
                or "twitter" in link_str \
                or "whatsapp" in link_str \
                or "reddit" in link_str \
                or "pinterest" in link_str \
                or "flipboard" in link_str \
                or "mailto" in link_str \
                or "amazon." in link_str \
                or link_str.startswith("#") \
                or "www.nasa.gov" in link_str:
          continue
        if ('Black' in link_str or 'black' in link_str) and ('Hole' in link_str or 'hole' in link_str):
          self.relevant_articles.append(link_str)
        self.queue.append(link_str)

  def save_urls(self) -> None:
    with open(self.url_file, "w") as f:
      for l in self.relevant_articles:
        f.write(l + "\n")

  def crawl_relevant_articles(self) -> None:
    counter = 0
    for link in self.relevant_articles:
      counter += 1
      try:
        html = request.urlopen(link).read().decode("utf8")
      except:
        print("An error occurred with link", link)
        continue
      soup = BeautifulSoup(html, features="html.parser")
      with open(self.document_directory + "/document"+str(counter)+".txt", "w") as f:
        f.write(soup.get_text())

  def clean_documents(self) -> None:
    for file in os.scandir(self.document_directory):
      if file.is_file():
        # print("Cleaning: ", file.name)
        sent: list[str] = []
        with open(file.path, 'r') as f:
          text = f.read()
          text = text.replace("\n", ".")
          text = text.replace("\t", ".")
          text = text.replace("(opens in new tab)", "")
          text = re.sub("\.{2,}", ".", text)
          sent = sent_tokenize(text)

        with open(self.clean_document_directory + "/" + file.name, 'w') as f:
          for s in sent:
            f.write(s + "\n")

  def extract_all_documents_tokens(self) -> None:
    englis_stopwords = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()

    for file in os.scandir(self.clean_document_directory):
      if file.is_file():
        # print("Extracting Tokens: ", file.name)
        raw_text: str = ""
        with open(file.path, 'r') as f:
          raw_text = f.read()
        tokens = [t.lower() for t in word_tokenize(raw_text) if t.isalpha()]
        tokens = [lemmatizer.lemmatize(t)
                  for t in tokens if t not in englis_stopwords]
        doc = ' '.join(tokens)
        self.document_tokens.append(doc)

  def calculate_tf_idf(self) -> None:
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(self.document_tokens)
    # print("n_samples: %d, n_features: %d\n\n" % vectors.shape)

    tf_idf = pd.DataFrame(vectors.todense())

    tf_idf.columns = vectorizer.get_feature_names_out()
    tfidf_matrix = tf_idf.T
    tfidf_matrix.columns = ['document' +
                            str(i) for i in range(1, tf_idf.shape[0]+1)]
    tfidf_matrix['count'] = tfidf_matrix.sum(axis=1)

    # Top 40 words
    tfidf_matrix = tfidf_matrix.sort_values(by='count', ascending=False)[:40]

    # Print the first 40 words
    print(tfidf_matrix.drop(columns=['count']).head(40))

  def create_knowledge_base(self) -> None:
    releted_terms: list[str] = [
        "black", "hole", "space", "star", "galaxy", "horizon", "mass",
        "event", "universe", "supermassive", "light", "matter", "singularity", "solar", "gravity"]

    englis_stopwords = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()

    for file in os.scandir(self.clean_document_directory):
      raw_text: str = ""
      if file.is_file():
        with open(file.path, 'r') as f:
          raw_text = f.read()
      sentences = sent_tokenize(raw_text)
      for sent in sentences:
        tokens = [t.lower() for t in word_tokenize(sent) if t.isalpha()]
        tokens = [lemmatizer.lemmatize(t)
                  for t in tokens if t not in englis_stopwords]
        if len(tokens) > 3:
          sent = ' '.join(tokens)
          self.corpus.append(sent)

    # print(self.corpus)
    for sent in self.corpus:
      for term in releted_terms:
        if term in sent:
          lst = self.knowledge_base.get(term, [])
          lst.append(sent)
          self.knowledge_base[term] = lst

    # Save knowledge_base
    # kb = open(self.knowledge_base_file, 'wb')
    # pickle.dump(self.knowledge_base, kb)
    # kb.close()

    # # Print knowledge_base
    # for k, v in self.knowledge_base.items():
    #   print(k, len(v))
    #   # print(len(self.knowledge_base[releted_terms[0]]))

    # f = open("data.txt", "a+")
    # # f.write("Yaaay!!!")
    # L = ["This is Delhi \n", "This is Paris \n", "This is London"]
    # f.writelines(L)
    # f.close()

    kb = KnowledgeBase()
    kb.insert(self.knowledge_base)
