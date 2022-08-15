import gevent
from nltk.stem import PorterStemmer
from regexExp import *
from string import printable

class PageProcessor(object):
    """
        Document class which handles
        tokenization, indexing, etc
    """

    # --------------------------------------------------------------------------
    def __init__(self, page_id, title, text, complete_index):

        self.page_id = page_id
        self.title = title.lower()
        self.refernces = ""
        self.external_links = ""
        self.categories = []
        self.text = text.lower()
        self.category_size = {"R": 0, "T": 0, "B": 0, "C": 0, "E": 0}
        self.stemmer = PorterStemmer()
        self.complete_index = complete_index
        self.sections(self.text)


    # --------------------------------------------------------------------------
    def sections(self, text):
        """
            Section flags --> R => References,
                              T => Title,
                              B => Body,
                              C => Category,
                              E => External links
        """

        # text = text.encode("ascii", "ignore")
        new_text = text

        # Different threads for parallel processing
        threads = []

        # Tokenize title
        title_tokens = self.title.split()
        self.category_size["T"] = len(title_tokens)
        threads.append(gevent.spawn(self.tokenize, title_tokens, "T"))

        # Remove citation text
        new_text = re.sub(r"\{\{[c|C]ite.*?\}\}", u"", new_text)

        # Get the references section
        references = ""
        try:
            references = references_re.search(text).group()
        except AttributeError:
            pass

        # Remove the extra words which should not be counted for index
        if references != "":
            references = re.sub(REFERENCES_SUB, u"", references)
            new_text = re.sub(references_re, u"==", new_text)
            references_tokens = references.split()
            self.category_size["R"] = len(references_tokens)
            threads.append(gevent.spawn(self.tokenize, references_tokens, "R"))

        # Get Categories
        categories = re.findall(category_re, text)
        new_text = re.sub(category_re, u"", new_text)
        category_tokens = []
        if categories != []:
            for ctg in categories:
                category_tokens.extend(ctg[11:-2].split())
            # Design decision - Space seperated categories
            # are considered seperately.
            self.category_size["C"] = len(category_tokens)
            threads.append(gevent.spawn(self.tokenize, category_tokens, "C"))

        # Get External links
        links = None
        try:
            links = external_links_re.search(text).group()
            # new_text = re.sub(external_links_re,
            #                   u"",
            #                   new_text).encode("ascii", "ignore")
            new_text = re.sub(external_links_re,
                              u"",
                              new_text)
        except AttributeError:
            pass

        if links:
            links = links.split("\n")
            for link in links:
                if link == "":
                    break
                links_tokens = link.split()
                self.category_size["E"] += len(links_tokens)
                threads.append(gevent.spawn(self.tokenize, links_tokens, "E"))

        try:
            infobox_tokens = infobox_re.search(new_text).group()
            infobox_tokens = infobox_tokens.split()
            if infobox_tokens != []:
                threads.append(gevent.spawn(self.tokenize,
                                            infobox_tokens,
                                            "I"))
                new_text = re.sub(infobox_re, "", new_text)
        except AttributeError:
            pass

        body_tokens = new_text.split()
        self.category_size["B"] = len(new_text)
        threads.append(gevent.spawn(self.tokenize, body_tokens, "B"))

        # Start parallel processing
        gevent.joinall(threads)

    # --------------------------------------------------------------------------
    def update_index(self, section, token):

        page_id = self.page_id
        category = self.complete_index[section]

        if token not in category:
            category[token] = {}
        if page_id not in category[token]:
            category[token][page_id] = 0

        category[token][page_id] += 1
        # @Todo: Add the following to normalize
        #.0 / self.category_size[section]


    # --------------------------------------------------------------------------
    def is_url(self, token):
        try:
            tmp = url_re.match(token).group()
            return True
        except AttributeError:
            return False

    # --------------------------------------------------------------------------
    def is_number(self, token):
        try:
            number_re.match(token).group()
            return True
        except:
            return False

    # --------------------------------------------------------------------------
    def tokenize(self, tokens, section):

        for token in tokens:
            splitted = re.split(u"(\|)|\-|\:|\;|\?|\(|\)|\*|\=|\\|\&|\/|\<|\>|\[|\]|\{|\}|\#|\+|\&|\%20|\_|\&nbsp|(\')|(\")", token)
            for i in splitted:
                if i is not None and len(i) > 1:
                    tmpi = i.strip(NOISE)
                    if tmpi not in NOISE_FILTER:
                        tmpi = self.stemmer.stem(tmpi)
                        tmpi = tmpi.strip(NOISE)
                        # tmpi = filter(lambda x: x in printable, tmpi)
                        # print(list(tmpi))
                        self.update_index(section, tmpi)

    def get_index(self):
        return self.complete_index

# ------------------------------------------------------------------------------