import xadmin
from . import models

xadmin.site.register(models.CourseCategory)
xadmin.site.register(models.Course)
xadmin.site.register(models.Teacher)
xadmin.site.register(models.CourseChapter)
xadmin.site.register(models.CourseSection)