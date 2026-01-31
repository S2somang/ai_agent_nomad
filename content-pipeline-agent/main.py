from crewai.flow.flow import Flow, listen, start, router, and_, or_
from pydantic import BaseModel
from typing import List
from crewai.agent import Agent
from crewai import LLM
from tools import web_search_tool
from seo_crew import SeoCrew
from virality_crew import ViralityCrew


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

        researcher = Agent(
            role="Head Researcher",
            backstory="You're like a digital detective who loves digging up fascinating facts and insights. You have a knack for finding the good stuff that others miss.",
            goal=f"Find the most interesting and useful info about {self.state.topic}",
            tools=[web_search_tool],
        )

        self.state.research = researcher.kickoff(
            f"Find the most interesting and useful info about {self.state.topic}"
        )
    
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
        
        blog_post = self.state.blog_post
        # 글적,,긁적,,, 여튼 모델은 암거나 쓰시고,,
        llm = LLM(model="openai/o4-mini", response_format=BlogPost)

        if blog_post is None:
            # message와 함꼐 llm.call을 호출한다...
            # 메세지가 좀 길어질거라 """을 쓴다..
            # llm.call()이 이미 BlogPost(...) Pydantic 객체로 반환하는 케이스가 있어요. 
            # 그런데 model_validate_json()은 **JSON 문자열(str/bytes)**만 받습니다
            result = llm.call(
                f"""
            Make a blog post with SEO practices on the topic {self.state.topic} using the following research:

            <research>
            ================
            {self.state.research}
            ================
            </research>
            """
            )
        else:
            print("Remaking blog.")
            result = llm.call(
                f"""
            You wrote this blog post on {self.state.topic}, but it does not have a good SEO score because of {self.state.score.reason} 
            
            Improve it.

            <blog post>
            {self.state.blog_post.model_dump_json()}
            </blog post>

            Use the following research.

            <research>
            ================
            {self.state.research}
            ================
            </research>
            """
            )

        # BlogPost.model_validate_json() 함수는 JSON 문자열을 BlogPost 객체로 변환하는 함수인데, 
        # result 변수에는 이미 BlogPost 객체가 들어있어서 JSON 문자열이 아니라는 오류가 발생한 것입니다. 
        # result를 model_validate_json() 없이 바로 self.state.blog_post에 할당하면 해결됩니다.
        self.state.blog_post = result

    
    @listen(or_("make_tweet", "remake_tweet"))
    def handle_make_tweet(self):
        
        tweet = self.state.tweet

        llm = LLM(model="openai/o4-mini", response_format=Tweet)

        if tweet is None:
            result = llm.call(
                f"""
            Make a tweet that can go viral on the topic {self.state.topic} using the following research:

            <research>
            ================
            {self.state.research}
            ================
            </research>
            """
            )
        else:
            result = llm.call(
                f"""
            You wrote this tweet on {self.state.topic}, but it does not have a good virality score because of {self.state.score.reason} 
            
            Improve it.

            <tweet>
            {self.state.tweet.model_dump_json()}
            </tweet>

            Use the following research.

            <research>
            ================
            {self.state.research}
            ================
            </research>
            """
            )

        self.state.tweet = result
    
    @listen(or_("make_linkedin_post", "remake_linkein_post"))
    def handle_make_linkedin_post(self):
        linkedin_post = self.state.linkedin_post

        llm = LLM(model="openai/o4-mini", response_format=LinkedInPost)

        if linkedin_post is None:
            result = llm.call(
                f"""
            Make a linkedin post that can go viral on the topic {self.state.topic} using the following research:

            <research>
            ================
            {self.state.research}
            ================
            </research>
            """
            )
        else:
            result = llm.call(
                f"""
            You wrote this linkedin post on {self.state.topic}, but it does not have a good virality score because of {self.state.score.reason} 
            
            Improve it.

            <linkedin_post>
            {self.state.linkedin_post.model_dump_json()}
            </linkedin_post>

            Use the following research.

            <research>
            ================
            {self.state.research}
            ================
            </research>
            """
            )

        self.state.linkedin_post = result


    @listen("handle_make_blog")
    def check_seo(self):
        result = (
            SeoCrew()
            .crew()
            .kickoff(
                inputs={
                    "topic": self.state.topic,
                    "blog_post": self.state.blog_post.model_dump_json(),
                }
            )
        )
        self.state.score = result.pydantic


    @listen(or_(handle_make_tweet,handle_make_linkedin_post))
    def check_virality(self):
        result = (
            ViralityCrew()
            .crew()
            .kickoff(
                inputs={
                    "topic": self.state.topic,
                    "content_type": self.state.content_type,
                    "content": (
                        self.state.tweet.model_dump_json()
                        if self.state.content_type == "tweet"
                        else self.state.linkedin_post.model_dump_json()
                    ),
                }
            )
        )
        self.state.score = result.pydantic

    @router(or_(check_seo, check_virality))
    def score_router(self):

        content_type = self.state.content_type
        score = self.state.score

        if score.score >= 7:
            return "check_passed"
        else:
            if content_type == "blog":
                return "remake_blog"
            elif content_type == "linkedin":
                return "remake_linkedin_post"
            else:
                return "remake_tweet"

    @listen("check_passed")
    def finalize_content(self):
        """Finalize the content"""
        print("🎉 Finalizing content...")

        if self.state.content_type == "blog":
            print(f"📝 Blog Post: {self.state.blog_post.title}")
            print(f"🔍 SEO Score: {self.state.score.score}/100")
        elif self.state.content_type == "tweet":
            print(f"🐦 Tweet: {self.state.tweet}")
            print(f"🚀 Virality Score: {self.state.score.score}/100")
        elif self.state.content_type == "linkedin":
            print(f"💼 LinkedIn: {self.state.linkedin_post.title}")
            print(f"🚀 Virality Score: {self.state.score.score}/100")

        print("✅ Content ready for publication!")
        return (
            self.state.linkedin_post
            if self.state.content_type == "linkedin"
            else (
                self.state.tweet
                if self.state.content_type == "tweet"
                else self.state.blog_post
            )
        )


flow = ContentPipelineFlow()

flow.kickoff(inputs={"content_type":"blog" , "topic": "AI Dog Training", })
# flow.plot()