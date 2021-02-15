from django import forms


class MyPostAdminForm(forms.ModelForm):
    def clean_content(self):
        content = self.cleaned_data['name']

        words = ['심심하다', '관리자', '금지어']
        error_message = '[{0}] {1}'.format(', '.join(words), '와 같은 단어들은 입력하실 수 없습니다.')

        if any(word in content for word in words):
            raise forms.ValidationError(error_message)

        return content


class MyFileAdminForm(forms.ModelForm):
    def save(self, commit=True):
        instance = super(MyFileAdminForm, self).save(commit=False)
        instance.file_ext = "old"
        print(instance)
        print(self)

        instance.save()  # finally save it.

        return instance


