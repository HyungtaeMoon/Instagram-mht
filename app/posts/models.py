import re

from django.db import models

from django.conf import settings


class Post(models.Model):
    author = models.ForeignKey(
        # 'auth.User'
        # Django 가 기본으로 제공하는 User 클래
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='작성자',
    )
    photo = models.ImageField(
        '사진',
        upload_to='post',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '포스트'
        verbose_name_plural = f'{verbose_name} 목록'
        ordering = ['-pk']


class Comment(models.Model):
    TAG_PATTERN = re.compile(r'#(?P<tag>\w+)')
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='포스트',
        related_name='comments',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='작성자'
    )
    content = models.TextField('댓글 내용')
    tags = models.ManyToManyField(
        'HashTag',
        blank=True,
        verbose_name='해시태그 목록',
    )
    _html = models.TextField('태그가 HTML화 된 댓글 내용', blank=True)

    class Meta:
        verbose_name = '댓글'
        verbose_name_plural = f'{verbose_name} 목록'

    def save(self, *args, **kwargs):
        def save_html():
            # 저장하기 전에 _html 필드를 채워야 함 (content 값을 사용해서)
            self._html = re.sub(
                self.TAG_PATTERN,
                r'<a href="/explore/tags\g<tag>/">#\g<tag></a>',
                self.content,
            )

        def save_tags():
            # DB에 Comment 저장이 완료된 후,
            #   자신의 'content' 값에서 해시태그 목록을 가져와서
            #   자신의 'tag' 속성 (MTM 필드)에 할당
            tags = [HashTag.objects.get_or_create(name=name)[0]
                    for name in re.findall(self.TAG_PATTERN, self.content)]
            self.tags.set(tags)
        save_html()
        save_tags()
        super().save(*args, **kwargs)

    @property
    def html(self):
        return self._html


class HashTag(models.Model):
    name = models.CharField(
        '태그명',
        max_length=100,
        unique=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '해시태그'
        verbose_name_plural = f'{verbose_name} 목록'
