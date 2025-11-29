from marshmallow import Schema, fields, validate


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str()
    email = fields.Email()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class UserRegisterSchema(Schema):
    username = fields.Str(
        required=True,
        validate=[
            validate.Length(min=3, max=64, error="Username must be 3-64 characters"),
        ]
    )
    email = fields.Email(required=True)
    password = fields.Str(
        required=True,
        load_only=True,
        validate=validate.Length(min=6, max=128, error="Password must be 6-128 characters")
    )


class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)
