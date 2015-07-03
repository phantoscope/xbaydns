# 操作步骤 #

  1. 将django/bin下的make-messages.py和compile-messages.py，放到一个你执行顺手的地方
  1. 在你的app目录下，执行如下命令
```
make-messages.py -l zh_CN
```
> > 他会生成如下目录结构
```
locale/zh_CN/LC_MESSAGES/
```
  1. 编写po文件，类似格式如下:
```
# SOME DESCRIPTIVE TITLE.
# Copyright (C) YEAR THE PACKAGE'S COPYRIGHT HOLDER
# This file is distributed under the same license as the PACKAGE package.
# FIRST AUTHOR <paradise.qingfeng@gmail.com>, 2007.
#
msgid ""
msgstr ""
"Project-Id-Version: xbaydns v1.0\n"
"Report-Msgid-Bugs-To: \n"
"POT-Creation-Date: 2007-12-10 19:54+0800\n"
"PO-Revision-Date: 2007-12-10 19:54+0800\n"
"Last-Translator: qingfeng <paradise.qingfeng@gmail.com>\n"
"Language-Team: Simplified Chinese <paradise.qingfeng@gmail.com>\n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=utf-8\n"
"Content-Transfer-Encoding: 8bit\n"
"X-Poedit-Language: Chinese\n"
"X-Poedit-Country: CHINA\n"
"X-Poedit-SourceCharset: utf-8\n"
"Plural-Forms: nplurals=1; plural=0;\n"

msgid "acl_verbose_name"
msgstr "地址片名称"

msgid "acl_verbose_name_plural"
msgstr "1.1 地址片名称管理"
```
  1. 编译po到mo
```
compile-messages.py
```
  1. 在settings.py中开启i18n，注意:**LocaleMiddleware必须放在SessionMiddleware后面**
```
MIDDLEWARE_CLASSES = (
    ...
    'django.contrib.sessions.middleware.SessionMiddleware',
    ...
    'django.middleware.locale.LocaleMiddleware',
)
```
  1. 在settings.py中设置要开启的语言支持
```
gettext = lambda s: s
LANGUAGES = (
  ('zh-cn', gettext('Simplified Chinese')),
)
```
> > 全部支持的语言，详见:http://www.djangoproject.com/documentation/0.96/settings/#languages