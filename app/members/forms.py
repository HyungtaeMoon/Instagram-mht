from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._user = None

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError('사용자명 또는 비밀번호가 올바르지 않습니다.')
        self._user = user

    @property
    def user(self):
        if self.errors:
            raise ValueError('데이터 유효성 검증에 실패했습니다.')
        return self._user


class SignupForm(forms.Form):
    username = forms.CharField(
        label='사용자명',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    password1 = forms.CharField(
        label='비밀번호',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    password2 = forms.CharField(
        label='비밀번호 확인',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    def clean_username(self):
        data = self.cleaned_data['username']
        if User.objects.filter(username=data).exists():
            self.fields['username'].widget.attrs['class'] += ' is-invalid'
            raise forms.ValidationError('이미 사용중인 아이디입니다')
        return data

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            self.fields['password1'].widget.attrs['class'] += ' is-invalid'
            self.fields['password2'].widget.attrs['class'] += ' is-invalid'
            raise forms.ValidationError('비밀번호와 비밀번호 확인의 입력값이 다릅니다.')
        return password2

    def save(self):
        if self.errors:
            raise ValueError('데이터 유효성 검증에 실패했습니다.')

        else:
            user = User.objects.create_user(
                username=self.cleaned_data['username'],
                password=self.cleaned_data['password1']
            )
            return user
