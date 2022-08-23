from io import BufferedRandom
from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


# Tables that have to do with Users


class Users(models.Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    last_modified_at = fields.DatetimeField(auto_now=True)
    first_name = fields.CharField(null=True, max_length=255)
    last_name = fields.CharField(null=True, max_length=255)
    email = fields.CharField(null=False, max_length=255)
    hashed_password = fields.CharField(null=False, max_length=255)
    is_active = fields.BooleanField(null=False, default=False)
    confirmation = fields.UUIDField(null=True)
    roles = fields.relational.ManyToManyField(
        model_name="models.Roles", related_name="users", through="user_roles"
    )

    def __str__(self):
        return self.email


class Roles(models.Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    last_modified_at = fields.DatetimeField(auto_now=True)
    name = fields.CharField(null=False, max_length=255)
    description = fields.CharField(null=False, max_length=255)

    def __str__(self):
        return self.name


class AllowedUsers(models.Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    last_modified_at = fields.DatetimeField(auto_now=True)
    email = fields.CharField(null=False, max_length=255)

    def __str__(self):
        return self.email

    class Meta:
        table = "allowed_users"


class GeneralMaintenance(models.Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    created_by = fields.CharField(null=False, max_length=255)
    last_modified_at = fields.DatetimeField(auto_now=True)
    last_modified_by = fields.CharField(null=True, max_length=255)
    description = fields.TextField(null=False)

    def __str__(self):
        return self.description

    class Meta:
        table = "general_maintenance"


class WorkingHours(models.Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    created_by = fields.CharField(null=False, max_length=255)
    last_modified_at = fields.DatetimeField(auto_now=True)
    last_modified_by = fields.CharField(null=True, max_length=255)
    date = fields.DateField(null=True)
    hours = fields.FloatField(null=True)
    description = fields.TextField(null=True)
    submitted = fields.BooleanField(null=False, default=False)
    # Foreign key
    user = fields.ForeignKeyField("models.Users", related_name="working_hours")

    def __str__(self):
        return self.description

    class Meta:
        table = "working_hours"

 
class BouwPlan(models.Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    created_by = fields.CharField(null=False, max_length=255)
    last_modified_at = fields.DatetimeField(auto_now=True)
    last_modified_by = fields.CharField(null=True, max_length=255)
    year = fields.IntField(null=True)
    ha = fields.FloatField(null=True)
    link = fields.CharField(null=True, max_length=255)
    gewas = fields.CharField(null=True, max_length=255)
    ingetekend_door = fields.CharField(null=True, max_length=255)
    opmerking = fields.CharField(null=True, max_length=255)
    perceel_nummer = fields.CharField(null=True, max_length=255)
    werknaam = fields.CharField(null=True, max_length=255)
    mest = fields.CharField(null=True, max_length=255)

    class Meta:
        table = "bouwplannen"


class Machines(models.Model):
    id =  fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    created_by = fields.CharField(null=False, max_length=255)
    last_modified_at = fields.DatetimeField(auto_now=True)
    last_modified_by = fields.CharField(null=True, max_length=255)
    work_number = fields.CharField(null=True, max_length=255)
    work_name = fields.CharField(null=True, max_length=255)
    category = fields.CharField(null=True, max_length=255)
    group = fields.CharField(null=True, max_length=255)
    brand_name = fields.CharField(null=True, max_length=255)
    type_name = fields.CharField(null=True, max_length=255)
    licence_number = fields.CharField(null=True, max_length=255)
    chassis_number = fields.CharField(null=True, max_length=255)
    construction_year  = fields.IntField(null=True)
    ascription_code = fields.CharField(null=True, max_length=255)

    class PydanticMeta:
        exclude = ("created_at",'created_by','last_modified_at','last_modified_by', 'maintenance_issues')

class MaintenanceMachines(models.Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    created_by = fields.CharField(null=False, max_length=255)
    last_modified_at = fields.DatetimeField(auto_now=True)
    last_modified_by = fields.CharField(null=True, max_length=255)
    issue_description = fields.CharField(null=True, max_length=255)
    status = fields.CharField(null=True, max_length=255)
    priority = fields.CharField(null=True, max_length=255)
    # Relations
    machine = fields.ForeignKeyField('models.Machines', related_name='maintenance_issues')
    
    class Meta:
        table = "machine_maintenance"


class TankTransactions(models.Model):
    id = fields.IntField(pk=True)
    vehicle = fields.CharField(null=True, max_length=255)
    driver = fields.CharField(null=True, max_length=255)
    transaction_type = fields.CharField(null=True, max_length=255)
    acquisition_mode= fields.CharField(null=True, max_length=255)
    transaction_status  = fields.CharField(null=True, max_length=255)
    start_date_time = fields.DatetimeField(null=True)
    transaction_number = fields.IntField(null=True)
    product = fields.CharField(null=True, max_length=255)
    quantity = fields.FloatField(null=True)
    transaction_duration = fields.CharField(null=True, max_length=255)
    meter = fields.IntField(null=True)
    meter_type = fields.CharField(null=True, max_length=255)


    class Meta:
        table = "tank_transactions"
