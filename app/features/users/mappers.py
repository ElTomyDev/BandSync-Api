from app.features.users.model import UserModel
from app.features.users.schema import UserResponseSchema


class UserMappers:
    def model_to_schema(user_model:UserModel) -> UserResponseSchema:
        return UserResponseSchema(
            _id = str(user_model.id),
            name = user_model.name,
            lastname = user_model.lastname,
            username = user_model.username
        )