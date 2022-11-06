import imp
from api.ma import ma, MethodField
from api.models.post import PostModel
from api.models.user import UserModel


class PostSchema(ma.SQLAlchemyAutoSchema):
    """
    게시물 모델에 관한 직렬화 규칙 정의
    """

    author_name = MethodField("get_author_name")

    def get_author_name(self, obj):
        return obj.author.username

    class Meta:
        model = PostModel
        dump_only = [
            "author_name",
        ]
        # load_only = [
        #     "author_id",
        # ]
        exclude = ("author_id",)
        include_fk = True
        load_instance = True
        ordered = True
