import urllib
import re
import ssl
from nltk.corpus import stopwords
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

pipe = pipeline("summarization", model="google-t5/t5-small")
tokenizer = AutoTokenizer.from_pretrained("google-t5/t5-small")
model = AutoModelForSeq2SeqLM.from_pretrained("google-t5/t5-small")

ssl._create_default_https_context = ssl._create_unverified_context
stopwords_ = stopwords.words('english')

class ai_in_video:
    """
    This class analyses the videa link and recommends the best video.
    """
    def __init__(self) -> None:
        pass

    def fetch_urls(self, text_summ:str)->str:
        """
        This function gives the relevant video links for the doubt posted.
        """
        out = pipe(text_summ)[0]['summary_text']
        search_keyword = "+".join([re.sub('[^A-Za-z0-9]+', '',w) for w in out.split(' ')])
        html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_keyword)
        unq_list = []
        video_ids = [unq_list.append(id_) for id_ in re.findall(r"watch\?v=(\S{11})", html.read().decode()) if id_ not in unq_list]
        video_links = []
        for id_ in unq_list:
            video_links.append("https://www.youtube.com/embed/"+id_)

        return video_links



