from crewai.flow.flow import Flow, listen, start, router, and_, or_
from pydantic import BaseModel

class ContentPipelineState(BaseModel):

    # Input
    content_type: str = ""
    topic: str = ""

    # Internal.
    max_length:int = 0


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

    @listen("make_blog")
    def handle_make_blog(self):
        print("blog만드는줒ㅇ..")
    
    @listen("make_tweet")
    def handle_make_tweet(self):
        print("tweet만드는줒ㅇ..")
    
    @listen("make_linkedin_post")
    def handle_make_linkedin_post(self):
        print("linkedin만드는줒ㅇ..")


    @listen("handle_make_blog")
    def check_seo(self):
        print("체킹 블로그 SEO")


    @listen(or_(handle_make_tweet,handle_make_linkedin_post))
    def check_varality(self):
        print("checking virality....")


    @listen(or_(check_varality, check_seo))
    def finalize_content(self):
        print("Finalizing content")

#  뭔가... 반대로 만들어졋는데...허어.....신기하네,,,,,

flow = ContentPipelineFlow()

# flow.kickoff(inputs={"content_type":"tweet" , "topic": "AI Dog Training", })
flow.plot()