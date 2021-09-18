import io
import pandas
import settings
import googleapiclient.discovery
from fastapi.responses import StreamingResponse
from fastapi import APIRouter, HTTPException, status
from .schemas import YoutubeURL
from typing import List

router_youtube = APIRouter(
    prefix="/youtube", tags=["YOUTUBE COMMENTS NOT REPLY"])

"""
----------------------------OUTPUT-------------------------------
|    o	videoId                                                 |
|    o	textOriginal                                            |
|    o	authorDisplayName                                       |
|    o	authorProfileImageUrl                                   |
|    o	authorChannelUrl                                        |
|    o	likeCount                                               |
|    o	publichedAt                                             |
|    o	updatedAt                                               |
-----------------------------------------------------------------
"""


@router_youtube.post("/comments-csv")
def message_csv(request: YoutubeURL):
    url_id = find_id_in_url(request.url)
    df = pandas.DataFrame(list_comments(url_id))

    # In-memory text
    stream = io.StringIO()

    # Encoding (spanish accent include)
    df.to_csv(stream, encoding="ISO-8859-1", index=False)

    # https://fastapi.tiangolo.com/advanced/custom-response/
    response = StreamingResponse(iter([stream.getvalue()]))

    # attachment (indicando que será descargado;
    response.headers["Content-Disposition"] = "attachment; filename=export.csv"
    return response


def find_id_in_url(url: str) -> str:
    url_exception = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Could not validate url",
    )

    start = url.find("v=")
    if start == -1:  # Method returns -1 if the value is not found.
        raise url_exception
    end = url.find("&", start)
    if end < 0:
        return url[start+2:]
    return url[start + 2:end]


def list_comments(video_id: str) -> List:
    data_dict: List[dict] = []

    youtube = googleapiclient.discovery.build(
        settings.api_service_name, settings.api_version, developerKey=settings.DEVELOPER_KEY)

    # SEARCHING
    request = youtube.commentThreads().list(
        part="id,snippet",
        maxResults=100,
        order="relevance",
        videoId=video_id
    )

    # DATA
    response = request.execute()
    add_to_dict(response.get("items"), data_dict)
    next_page_token = response.get("nextPageToken")

    # IF THERE IS MORE, LOOK FOR
    while next_page_token:
        request = youtube.commentThreads().list(
            part="id,snippet,replies",
            maxResults=100,
            pageToken=next_page_token,
            order="relevance",
            videoId=video_id
        )
        response = request.execute()
        add_to_dict(response.get("items"), data_dict)
        next_page_token = response.get("nextPageToken")
    return data_dict


def add_to_dict(response: List[dict], data_dict: List[dict]) -> None:
    for element in response:
        comment = element.get("snippet").get("topLevelComment").get("snippet")
        data_dict.append({
            "textOriginal": comment.get("textOriginal"),
            "authorDisplayName": comment.get("authorDisplayName"),
            "authorProfileImageUrl": comment.get("authorProfileImageUrl"),
            "authorChannelUrl": comment.get("authorChannelUrl"),
            "likeCount": comment.get("likeCount"),
            "publishedAt": comment.get("publishedAt"),
            "updatedAt": comment.get("updatedAt"),
        })
