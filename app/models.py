from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from colorfield.fields import ColorField
# Create your models here.


class Project(models.Model):
    owner = models.ForeignKey(User, on_delete=models.PROTECT, help_text=_("The person who created the project"), verbose_name=_("Owner"))
    name = models.CharField(max_length=255, help_text=_("A label used to describe the project"), verbose_name=_("Name"))
    description = models.TextField(default="", blank=True, help_text=_("More in-depth description of the project"), verbose_name=_("Description"))
    created_at = models.DateTimeField(default=timezone.now, help_text=_("Creation date"), verbose_name=_("Created at"))
    deleting = models.BooleanField(db_index=True, default=False, help_text=_("Whether this project has been marked for deletion. Projects that have running tasks need to wait for tasks to be properly cleaned up before they can be deleted."), verbose_name=_("Deleting"))
    tags = models.TextField(db_index=True, default="", blank=True, help_text=_("Project tags"), verbose_name=_("Tags"))


    def __str__(self):
        return self.name
    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")


class CaseInsensitiveCharField(models.CharField):
    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        if value is not None:
            value = value.lower()
        return value

class GlobalStandardCategory(models.Model):
    name = CaseInsensitiveCharField(max_length=255, help_text=_(
        "Standard Category name"), verbose_name=_("Name"), unique=True)
    description = models.TextField(default="", blank=True, help_text=_(
        "Description about this category"), verbose_name=_("Description"))
    created_at = models.DateTimeField(default=timezone.now, help_text=_(
        "Creation date"), verbose_name=_("Created at"))

    def __str__(self):
        return str(self.name)


class GlobalSubCategory(models.Model):
    name = models.CharField(max_length=255, help_text=_(
        "In which Sub category you want to seperate your project layer"), verbose_name=_("Name") )
    standard_category = models.ForeignKey(GlobalStandardCategory, on_delete=models.PROTECT, help_text=_(
        "Standard Category related to the project"), verbose_name=_("Standard Category"))
    description = models.TextField(default="", blank=True, help_text=_(
        "Description about this category"), verbose_name=_("Description"))
    created_at = models.DateTimeField(default=timezone.now, help_text=_(
        "Creation date"), verbose_name=_("Created at"))

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
    sub_category = models.ForeignKey(GlobalSubCategory, on_delete=models.PROTECT, help_text=_(
        "Sub Category related to the project"), verbose_name=_("Sub Category"))
    description = models.TextField(default="", blank=True, help_text=_(
        "Description about this category"), verbose_name=_("Description"))
    created_at = models.DateTimeField(default=timezone.now, help_text=_(
        "Creation date"), verbose_name=_("Created at"))

    def __str__(self):
        return self.sub_category.standard_category.name + "|" + "|" +self.sub_category.name+"|"+ self.name



class GlobalCategoryStyle(models.Model):
    category = models.OneToOneField(GlobalCategory, on_delete=models.PROTECT, help_text=_(
        "Style related to this Category"), verbose_name=_("Category"))
    fill = ColorField(default='#2c3e50', help_text=_(
        "Fill color for the polygon"), verbose_name=_("Fill Color"))
    fill_opacity = models.DecimalField(decimal_places=2, max_digits=3, default=0.5)
    stroke = ColorField(default='#C86AFF', help_text=_(
        "Stroke color for the polygon"), verbose_name=_("Stroke Color"))
    stroke_width = models.PositiveIntegerField(default=1 )
    xml  = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, help_text=_(
        "Creation date"), verbose_name=_("Created at"))
    
    def __str__(self):
        return self.category.sub_category.standard_category.name +"|"+  self.category.sub_category.name +"|"+ self.category.name