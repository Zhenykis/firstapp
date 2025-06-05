from requests import Response
from fastapi import APIRouter,Depends, status, Response
from schemas.comment import CommentIn
from repository.comments import CommentRepository

router = APIRouter(
    prefix="/comments",
    tags=["comment"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_comment(comment_data: CommentIn, comment_repository: CommentRepository = Depends()):
    await comment_repository.create_comment(comment_data)
    return Response(content= "Комментарий к объявлению создан!")


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(comment_id: int,comment_repository: CommentRepository = Depends() ):
        await comment_repository.del_comment(comment_id=comment_id)

