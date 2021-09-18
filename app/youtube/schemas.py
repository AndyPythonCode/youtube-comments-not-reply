from pydantic import BaseModel, HttpUrl

class YoutubeURL(BaseModel):
    url: HttpUrl  # Schema http or https, TLD required, max length 2083
