from marshmallow import Schema, fields, validate, validates, ValidationError
import re


class LocationSchema(Schema):
    lat = fields.Float(
        required=True,
        validate=validate.Range(min=-90, max=90, error="Latitude must be between -90 and 90")
    )
    lon = fields.Float(
        required=True,
        validate=validate.Range(min=-180, max=180, error="Longitude must be between -180 and 180")
    )


class AccelGyroSchema(Schema):
    x = fields.Float(required=True)
    y = fields.Float(required=True)
    z = fields.Float(required=True)


class DeviceReportSchema(Schema):
    device_name = fields.Str(required=True, validate=validate.Length(max=255))
    mac_address = fields.Str(required=True)
    location = fields.Nested(LocationSchema, required=True)
    speed = fields.Float(
        required=False,
        allow_none=True,
        validate=validate.Range(min=0, max=400, error="Speed must be 0-400 km/h")
    )
    vibration = fields.Int(
        required=False,
        allow_none=True,
        validate=validate.Range(min=0, max=1024, error="Vibration must be 0-1024")
    )
    accel = fields.Nested(AccelGyroSchema, required=False, allow_none=True)
    gyro = fields.Nested(AccelGyroSchema, required=False, allow_none=True)

    @validates('mac_address')
    def validate_mac_address(self, value, **kwargs):
        if not re.match(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$', value):
            raise ValidationError("Invalid MAC address format. Expected: AA:BB:CC:DD:EE:FF or AA-BB-CC-DD-EE-FF")
