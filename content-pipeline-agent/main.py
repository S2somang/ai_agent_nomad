from crewai.flow.flow import Flow, listen, start, router, and_, or_
from pydantic import BaseModel
from typing import List
from crewai.agent import Agent
from crewai import LLM
from tools import web_search_tool
# from seo_crew import SeoCrew
# from virality_crew import ViralityCrew


class BlogPost(BaseModel):
    title: str
    subtitle: str
    sections: List[str]


class Tweet(BaseModel):
    content: str
    hashtags: str


class LinkedInPost(BaseModel):
    hook: str
    content: str
    call_to_action: str


class Score(BaseModel):

    score: int = 0
    reason: str = ""

class ContentPipelineState(BaseModel):

    # Input
    content_type: str = ""
    topic: str = ""

    # Internal..
    max_length: int = 0
    research: str = ""
    score: Score | None = None

    # Content
    blog_post: BlogPost | None = None
    tweet: Tweet | None = None
    linkedin_post: LinkedInPost | None = None


class ContentPipelineFlow(Flow[ContentPipelineState]):

    @start()
    def init_content_pipeline(self):
        if self.state.content_type not in ["tweet", "blog", "linkedin"]:
            raise ValueError("The content type is wrong.")

        if self.state.topic == "":
            raise ValueError("The topic can't be blank.")

        if self.state.content_type == "tweet":
            self.state.max_length = 150
        elif self.state.content_type == "blog":
            self.state.max_length = 800
        elif self.state.content_type == "linkedin":
            self.state.max_length = 500

    @listen(init_content_pipeline)
    def conduct_research(self):
        print("검색중...")
        return True
    
    @router(conduct_research)
    def conduct_research_router(self):
        content_type = self.state.content_type

        if content_type == "blog":
            return "make_blog"
        elif content_type == "tweet":
            return "make_tweet"
        else:
            return "make_linkedin_post"

    @listen(or_("make_blog", "remake_blog"))
    def handle_make_blog(self):
        # 만약 블로그 포스트가 이전에 만들어진 적이 있는지 확인하고 그렇다면 예전 것을 ai에게 보여줘야함 그리고 그걸 개선해달라고 요청할거임
        # else 이전에 생성딘 적이 없으면 그냥 생성해달라고 요청할거임
        # 니가 만들었던건데 별로니까 더 좋게 만드삼...아하?
        print("blog만드는줒ㅇ..")
    
    @listen(or_("make_tweet", "remake_tweet"))
    def handle_make_tweet(self):
        print("tweet만드는줒ㅇ..")
    
    @listen(or_("make_linkedin_post", "remake_linkein_post"))
    def handle_make_linkedin_post(self):
        print("linkedin만드는줒ㅇ..")


    @listen("handle_make_blog")
    def check_seo(self):
        print("체킹 블로그 SEO")


    @listen(or_(handle_make_tweet,handle_make_linkedin_post))
    def check_varality(self):
        print("checking virality....")

    @router(or_(check_seo, check_varality))
    def score_router(self):

        content_type = self.state.content_type
        score = self.state.score

        if score >= 8:
            return "check_passed"

        else:
            if content_type == "blog":
                return "remake_blog"
            elif content_type == "linkedin":
                return "remake_linkein_post"
            else:
                return "remake_tweet"

    @listen("check_passed")
    def finalize_content(self):
        print("Finalizing content")

#  뭔가... 반대로 만들어졋는데...허어.....신기하네,,,,,

flow = ContentPipelineFlow()

# flow.kickoff(inputs={"content_type":"tweet" , "topic": "AI Dog Training", })
flow.plot()