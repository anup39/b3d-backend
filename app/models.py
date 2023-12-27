from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from colorfield.fields import ColorField
from django.contrib.gis.db import models
from django.db.models import Manager as GeoManager


class Role(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, help_text=_(
        "Name of the Role"), verbose_name=_("Name"), default="project admin")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, help_text=_(
        "The person who created"), verbose_name=_("Created by"))
    created_at = models.DateTimeField(default=timezone.now, help_text=_(
        "Creation date"), verbose_name=_("Created at"))
    is_display = models.BooleanField(default=True)
    is_edited = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name


class CaseInsensitiveCharField(models.CharField):
    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        if value is not None:
            value = value.lower()
        return value


class GlobalStandardCategory(models.Model):
    name = CaseInsensitiveCharField(max_length=255, help_text=_(
        "Standard Category name"), verbose_name=_("Name"), unique=True)
    description = models.TextField(default="",  help_text=_(
        "Description about this category"), verbose_name=_("Description"))
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, help_text=_(
        "The person who created"), verbose_name=_("Created by"))
    created_at = models.DateTimeField(default=timezone.now, help_text=_(
        "Creation date"), verbose_name=_("Created at"))
    is_display = models.BooleanField(default=True)
    is_edited = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)


class GlobalSubCategory(models.Model):
    name = models.CharField(max_length=255, help_text=_(
        "In which Sub category you want to seperate your project layer"), verbose_name=_("Name"))
    standard_category = models.ForeignKey(GlobalStandardCategory, on_delete=models.SET_NULL, null=True, help_text=_(
        "Standard Category related to the project"), verbose_name=_("Standard Category"))
    description = models.TextField(default="",  help_text=_(
        "Description about this category"), verbose_name=_("Description"))
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, help_text=_(
        "The person who created"), verbose_name=_("Created by"))
    created_at = models.DateTimeField(default=timezone.now, help_text=_(
        "Creation date"), verbose_name=_("Created at"))
    is_display = models.BooleanField(default=True)
    is_edited = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        unique_together = (("standard_category", "name"),)

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.standard_category.name)+"|"+str(self.name)


class GlobalCategory(models.Model):
    name = models.CharField(max_length=255, help_text=_(
        "In which category you want to seperate your project layer"), verbose_name=_("Name"))
    standard_category = models.ForeignKey(GlobalStandardCategory, on_delete=models.SET_NULL, null=True, help_text=_(
        "Standard Category related to the project"), verbose_name=_("Standard Category"))
    sub_category = models.ForeignKey(GlobalSubCategory, on_delete=models.SET_NULL, null=True, help_text=_(
        "Sub Category related to the project"), verbose_name=_("Sub Category"))
    description = models.TextField(default="",  help_text=_(
        "Description about this category"), verbose_name=_("Description"))
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, help_text=_(
        "The person who created"), verbose_name=_("Created by"))
    created_at = models.DateTimeField(default=timezone.now, help_text=_(
        "Creation date"), verbose_name=_("Created at"))
    type_of_geometry = models.CharField(max_length=255, default="Polygon")
    is_display = models.BooleanField(default=True)
    is_edited = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.sub_category.standard_category.name + "|" + "|" + self.sub_category.name+"|" + self.name


class GlobalCategoryStyle(models.Model):
    category = models.OneToOneField(GlobalCategory, on_delete=models.SET_NULL, null=True, help_text=_(
        "Style related to this Category"), verbose_name=_("Category"))
    fill = ColorField(default='#2c3e50', help_text=_(
        "Fill color for the polygon"), verbose_name=_("Fill Color"))
    fill_opacity = models.DecimalField(
        decimal_places=2, max_digits=3, default=0.5)
    stroke = ColorField(default='#C86AFF', help_text=_(
        "Stroke color for the polygon"), verbose_name=_("Stroke Color"))
    stroke_width = models.PositiveIntegerField(default=1)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, help_text=_(
        "The person who created"), verbose_name=_("Created by"))
    created_at = models.DateTimeField(default=timezone.now, help_text=_(
        "Creation date"), verbose_name=_("Created at"))
    is_display = models.BooleanField(default=True)
    is_edited = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.category.sub_category.standard_category.name + "|" + self.category.sub_category.name + "|" + self.category.name


class Client(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, help_text=_(
        "Client associated user"), verbose_name=_("Client User"), related_name="clients_as_user")
    name = models.CharField(max_length=255, help_text=_(
        "Client name"), verbose_name=_("Client name"))
    description = models.TextField(default="", help_text=_(
        "More in-depth description of the Client"), verbose_name=_("Description"))
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, help_text=_(
        "The person who created"), verbose_name=_("Created by"), related_name="clients_as_creator")
    created_at = models.DateTimeField(default=timezone.now, help_text=_(
        "Creation date"), verbose_name=_("Created at"))
    is_display = models.BooleanField(default=True)
    is_edited = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Client")
        verbose_name_plural = _("Clients")


class Project(models.Model):
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, help_text=_(
        "Client Associated with this project"), verbose_name=_("Client"))
    name = models.CharField(max_length=255, help_text=_(
        "A label used to describe the project"), verbose_name=_("Name"))
    description = models.TextField(default="", help_text=_(
        "More in-depth description of the project"), verbose_name=_("Description"))
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, help_text=_(
        "The person who created the project"), verbose_name=_("Created by"))
    created_at = models.DateTimeField(default=timezone.now, help_text=_(
        "Creation date"), verbose_name=_("Created at"))
    is_display = models.BooleanField(default=True)
    is_edited = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")


def validate_png(value):
    if not value.name.endswith('.png'):
        raise ValidationError("Only PNG files are allowed.")

# make endpoint like this "/tiles/{z}/{x}/{y}@{scale}x.{format}


class RasterData(models.Model):
    id = models.AutoField(primary_key=True)
    task_id = models.UUIDField(null=True)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, help_text=_(
        "Client Associated with this"), verbose_name=_("Client"))
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, help_text=_(
        "Point related to the project"), verbose_name=_("Project"))
    name = models.CharField(max_length=255, help_text=_(
        "Name for the rater data"), verbose_name=_("Name"))
    file_name = models.CharField(max_length=255, help_text=_(
        "Name for the rater file"), verbose_name=_("File Name"), default="")
    tif_file = models.FileField(upload_to="Uploads/RasterData")
    progress = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=255, help_text=_(
        "Status for the task"), verbose_name=_("Status"), default="Uploaded")
    file_size = models.PositiveBigIntegerField(default=0)
    projection = models.CharField(max_length=255, help_text=_(
        "Projection of the Tif"), verbose_name=_("Projection"), default="Not Defined")
    screenshot_image = models.ImageField(
        upload_to='Uploads/RasterImage', default='Uploads/RasterImage/raster_sample.png',  validators=[validate_png])
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, help_text=_(
        "The person who created"), verbose_name=_("Created by"))
    created_at = models.DateTimeField(default=timezone.now)
    is_display = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    is_edited = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Property'



class OBJData(models.Model):
    id = models.AutoField(primary_key=True)
    obj_file = models.FileField(upload_to="Uploads/OBJData")
    created_at = models.DateTimeField(default=timezone.now)
    is_display = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    is_edited = models.BooleanField(default=False)

    # def __str__(self):
    #     return self.id

    class Meta:
        verbose_name_plural = 'OBJData'



class StandardCategory(models.Model):
    name = models.CharField(max_length=255, help_text=_(
        "In which standard category you want to seperate your project layer"), verbose_name=_("Name"))
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, help_text=_(
        "Client Associated with this"), verbose_name=_("Client"))
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, help_text=_(
        "Standard Category related to the project"), verbose_name=_("Project"))
    properti = models.ForeignKey(RasterData, on_delete=models.SET_NULL, null=True, help_text=_(
        "Standard Category related to this property"), verbose_name=_("Property"))
    global_standard_category = models.ForeignKey(GlobalStandardCategory, on_delete=models.SET_NULL, null=True, help_text=_(
        "Global Standard Category related to the project"), verbose_name=_("Global Standard Category"))
    description = models.TextField(default="",  help_text=_(
        "Description about this category"), verbose_name=_("Description"))
    view_name = models.CharField(max_length=255,  null=True)
    publised = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, help_text=_(
        "The person who created"), verbose_name=_("Created by"))
    created_at = models.DateTimeField(default=timezone.now, help_text=_(
        "Creation date"), verbose_name=_("Created at"))
    is_display = models.BooleanField(default=True)
    is_edited = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.client.name) + "|"+str(self.name)


class SubCategory(models.Model):
    name = models.CharField(max_length=255, help_text=_(
        "In which Sub category you want to seperate your project layer"), verbose_name=_("Name"))
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, help_text=_(
        "Client Associated with this"), verbose_name=_("Client"))
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, help_text=_(
        "Sub Category related to the project"), verbose_name=_("Project"))
    properti = models.ForeignKey(RasterData, on_delete=models.SET_NULL, null=True, help_text=_(
        "Sub Category related to this property"), verbose_name=_("Property"))
    standard_category = models.ForeignKey(StandardCategory, on_delete=models.SET_NULL, null=True, help_text=_(
        "Standard Category related to the project"), verbose_name=_("Standard Category"))
    global_standard_category = models.ForeignKey(GlobalStandardCategory, on_delete=models.SET_NULL, null=True, help_text=_(
        "Global Standard Category related to the project"), verbose_name=_("Global Standard Category"))
    global_sub_category = models.ForeignKey(GlobalSubCategory, on_delete=models.SET_NULL, null=True,  help_text=_(
        "Global Sub Category related to the project"), verbose_name=_("Global Sub Category"))
    description = models.TextField(default="",  help_text=_(
        "Description about this category"), verbose_name=_("Description"))
    view_name = models.CharField(max_length=255,  null=True)
    publised = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, help_text=_(
        "The person who created"), verbose_name=_("Created by"))
    created_at = models.DateTimeField(default=timezone.now, help_text=_(
        "Creation date"), verbose_name=_("Created at"))
    is_display = models.BooleanField(default=True)
    is_edited = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.client.name) + "|"+str(self.standard_category.name)+"|"+str(self.name)


class Category(models.Model):
    name = models.CharField(max_length=255, help_text=_(
        "In which category you want to seperate your project layer"), verbose_name=_("Name"))
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, help_text=_(
        "Client Associated with this"), verbose_name=_("Client"))
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, help_text=_(
        "Category related to the project"), verbose_name=_("Project"))
    properti = models.ForeignKey(RasterData, on_delete=models.SET_NULL, null=True, help_text=_(
        "Category related to this property"), verbose_name=_("Property"))
    standard_category = models.ForeignKey(StandardCategory, on_delete=models.SET_NULL, null=True,  help_text=_(
        "Standard Category related to the project"), verbose_name=_("Standard Category"))
    global_standard_category = models.ForeignKey(GlobalStandardCategory, on_delete=models.SET_NULL, null=True, help_text=_(
        "Global Standard Category related to the project"), verbose_name=_("Global Standard Category"))
    sub_category = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, help_text=_(
        "Sub Category related to the project"), verbose_name=_("Sub Category"))
    global_sub_category = models.ForeignKey(GlobalSubCategory, on_delete=models.SET_NULL, null=True, help_text=_(
        "Global Sub Category related to the project"), verbose_name=_("Global Sub Category"))
    global_category = models.ForeignKey(GlobalCategory, on_delete=models.SET_NULL, null=True, help_text=_(
        "Global Category related to the project"), verbose_name=_("Global  Category"))
    description = models.TextField(default="",  help_text=_(
        "Description about this category"), verbose_name=_("Description"))
    type_of_geometry = models.CharField(max_length=255, default="Polygon")
    view_name = models.CharField(max_length=255,  null=True)
    publised = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, help_text=_(
        "The person who created"), verbose_name=_("Created by"))
    created_at = models.DateTimeField(default=timezone.now, help_text=_(
        "Creation date"), verbose_name=_("Created at"))
    is_display = models.BooleanField(default=True)
    is_edited = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            category_style = CategoryStyle.objects.get(category=self)
        except CategoryStyle.DoesNotExist:
            global_category_style = GlobalCategoryStyle.objects.get(
                category=self.global_category)
            fill = global_category_style.fill,
            stroke = global_category_style.stroke,
            category_style = CategoryStyle(
                client=self.client,
                created_by=self.created_by,
                project=self.project,
                category=self,
                global_category=self.global_category,
                fill=fill[0],
                stroke=stroke[0],
            )

        category_style.save()

    def delete(self, *args, **kwargs):
        try:
            category_style = CategoryStyle.objects.get(category=self)
            category_style.delete()
        except CategoryStyle.DoesNotExist:
            pass

        super().delete(*args, **kwargs)

    def __str__(self):
        return self.client.name + " | " + self.standard_category.name+" | " + self.sub_category.name+" | " + self.name

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


class CategoryStyle(models.Model):
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, help_text=_(
        "Client Associated with this"), verbose_name=_("Client"))
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, help_text=_(
        "Style related to the project"), verbose_name=_("Project"), null=True)
    properti = models.ForeignKey(RasterData, on_delete=models.SET_NULL, null=True, help_text=_(
        "Category Style related to this property"), verbose_name=_("Property"))
    category = models.OneToOneField(Category, on_delete=models.SET_NULL, help_text=_(
        "Geometry related to this Category"), verbose_name=_("Category"), null=True)
    global_category = models.OneToOneField(GlobalCategory, on_delete=models.SET_NULL, help_text=_(
        "Geometry related to this Category"), verbose_name=_("Global Category"), null=True)

    fill = ColorField(default='#2c3e50', help_text=_(
        "Fill color for the polygon"), verbose_name=_("Fill Color"))
    fill_opacity = models.DecimalField(
        decimal_places=2, max_digits=3, default=0.5)
    stroke = ColorField(default='#ffffff', help_text=_(
        "Stroke coloe for the polygon"), verbose_name=_("Stroke Color"))
    stroke_width = models.PositiveIntegerField(default=1)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, help_text=_(
        "The person who created"), verbose_name=_("Created by"))
    created_at = models.DateTimeField(default=timezone.now, help_text=_(
        "Creation date"), verbose_name=_("Created at"))
    is_display = models.BooleanField(default=True)
    is_edited = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.client.name + " | " + self.category.standard_category.name+" | " + self.category.sub_category.name+" | " + self.category.name

    class Meta:
        verbose_name = _("CategoryStyle")
        verbose_name_plural = _("CategoryStyles")


class PolygonData(models.Model):
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, help_text=_(
        "Client Associated with this"), verbose_name=_("Client"))
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, help_text=_(
        "Polygon related to the project"), verbose_name=_("Property"), null=True)
    properti = models.ForeignKey(RasterData, on_delete=models.SET_NULL, null=True, help_text=_(
        "Polygon related to this property"), verbose_name=_("map"))
    standard_category = models.ForeignKey(StandardCategory, on_delete=models.SET_NULL, help_text=_(
        "Standard Category related to the polygon"), verbose_name=_("Standard Category"), null=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, help_text=_(
        "Sub Category related to the polygon"), verbose_name=_("Sub Category"), null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, help_text=_(
        "Cateogyr related to this polygon"), verbose_name=_("Category"), null=True)
    standard_category_name = models.CharField(max_length=255,  null=True)
    sub_category_name = models.CharField(max_length=255,  null=True)
    category_name = models.CharField(max_length=255,  null=True)
    geom = models.PolygonField(srid=4326, dim=2)
    attributes = models.JSONField(default=dict,  null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, help_text=_(
        "The person who created"), verbose_name=_("Created by"))
    created_at = models.DateTimeField(default=timezone.now)
    is_display = models.BooleanField(default=True)
    is_edited = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    objects = GeoManager()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            self.standard_category_name = self.standard_category.name
            self.sub_category_name = self.sub_category.name
            self.category_name = self.category.name
            self.save()
        except:
            pass

    class Meta:
        verbose_name_plural = 'PolygonData'

    def __str__(self):
        return str(self.id)


class LineStringData(models.Model):
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, help_text=_(
        "Client Associated with this"), verbose_name=_("Client"))
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, help_text=_(
        "LineString related to the project"), verbose_name=_("Project"), null=True)
    properti = models.ForeignKey(RasterData, on_delete=models.SET_NULL, null=True, help_text=_(
        "LineString related to this property"), verbose_name=_("Property"))
    standard_category = models.ForeignKey(StandardCategory, on_delete=models.SET_NULL, help_text=_(
        "Standard Category related to the LineString"), verbose_name=_("Standard Category"), null=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, help_text=_(
        "Sub Category related to the LineString"), verbose_name=_("Sub Category"), null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, help_text=_(
        "Cateogyr related to this LineString"), verbose_name=_("Category"), null=True)
    standard_category_name = models.CharField(max_length=255,  null=True)
    sub_category_name = models.CharField(max_length=255,  null=True)
    category_name = models.CharField(max_length=255,  null=True)
    geom = models.LineStringField(srid=4326, dim=2)
    attributes = models.JSONField(default=dict,  null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, help_text=_(
        "The person who created"), verbose_name=_("Created by"))
    created_at = models.DateTimeField(default=timezone.now)
    is_display = models.BooleanField(default=True)
    is_edited = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    objects = GeoManager()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            self.standard_category_name = self.standard_category.name
            self.sub_category_name = self.sub_category.name
            self.category_name = self.category.name
            self.save()
        except:
            pass

    class Meta:
        verbose_name_plural = 'LineStringData'

    def __str__(self):
        return str(self.project.name)


class PointData(models.Model):
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, help_text=_(
        "Client Associated with this"), verbose_name=_("Client"))
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, help_text=_(
        "Point related to the project"), verbose_name=_("Project"), null=True)
    properti = models.ForeignKey(RasterData, on_delete=models.SET_NULL, null=True, help_text=_(
        "Point related to this property"), verbose_name=_("Property"))
    standard_category = models.ForeignKey(StandardCategory, on_delete=models.SET_NULL, help_text=_(
        "Standard Category related to the Point"), verbose_name=_("Standard Category"), null=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, help_text=_(
        "Sub Category related to the Point"), verbose_name=_("Sub Category"), null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, help_text=_(
        "Cateogyr related to this Point"), verbose_name=_("Category"), null=True)
    standard_category_name = models.CharField(max_length=255,  null=True)
    sub_category_name = models.CharField(max_length=255,  null=True)
    category_name = models.CharField(max_length=255,  null=True)
    geom = models.PointField(srid=4326, dim=2)
    attributes = models.JSONField(default=dict,  null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, help_text=_(
        "The person who created"), verbose_name=_("Created by"))
    created_at = models.DateTimeField(default=timezone.now)
    is_display = models.BooleanField(default=True)
    is_edited = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    objects = GeoManager()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            self.standard_category_name = self.standard_category.name
            self.sub_category_name = self.sub_category.name
            self.category_name = self.category.name
            self.save()
        except:
            pass

    class Meta:
        verbose_name_plural = 'PointData'

    def __str__(self):
        return str(self.project.name)


class UserRole(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,  help_text=_(
        "The person who created the project"), verbose_name=_("User"), related_name="roles_as_user")
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, help_text=_(
        "Role of the user"), verbose_name=_("Role"))
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, help_text=_(
        "Client Associated with this"), verbose_name=_("Client"))
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, help_text=_(
        "Project"), verbose_name=_("Project"), related_name="projects_as_user")
    properti = models.ForeignKey(RasterData, on_delete=models.SET_NULL, null=True, help_text=_(
        "User related to this property"), verbose_name=_("Property"))
    created_at = models.DateTimeField(default=timezone.now, help_text=_(
        "Creation date"), verbose_name=_("Created at"))
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, help_text=_(
        "The person who created"), verbose_name=_("Created by"), related_name="roles_as_creator")
    is_display = models.BooleanField(default=True)
    is_edited = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    def __str__(self) -> str:
        if self.client:
            return self.user.username + " | " + self.client.name + " | " + self.role.name
        else:
            return self.user.username + " | " + self.role.name
