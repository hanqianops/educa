

* fixtures 可以用于初始化数据库
* ContentTypes
    - ContentTypes是由Django框架提供的一个核心功能，
    - 它对当前项目中所有基于Django驱动的model提供了更高层次的抽象接口，是对model的一次封装，可以通过contenttypes动态的访问model类型，而不需要每次import具体的model类型。
    - 在第一次对Django的model进行migrate之后生成django_content_type表
    - 记录了当前的Django项目中所有model所属的app（即app_label属性）以及model的名字（即model属性）。
    - 可以对当前model设置了一个ContentType的外键，当前model的每个实例都具备一个ContentType的id作为外键，而ContentType的id恰恰代表着一个Model


# 创建一个内容管理系统
- CMS将允许教师去创建课程以及管理课程的内容。
- 使用Django的认证框架。
- 排列教师创建的课程。
- 创建，编辑以及删除课程。
- 添加模块到一个课程中并且重新排序它们。
- 添加不同类型的内容给每个模块并且重新排序内容。


# 使用类视图来创建，编辑，以及删除课程
- 创建一个mixin类来包含一个公用的行为供课程的视图使用
- 使用Django认证框架管理视图权限，只有教师可以创建，更新以及删除课程
