import xadmin
from xadmin import views


class GlobalSettings:
    """xadmin的全局配置"""
    site_title = "乾坤学城"  # 设置站点标题
    site_footer = "乾坤学城有限公司"  # 设置站点的页脚
    # menu_style = "accordion"  # 设置菜单折叠


xadmin.site.register(views.CommAdminView, GlobalSettings)
