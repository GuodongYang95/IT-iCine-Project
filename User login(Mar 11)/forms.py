from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.utils.translation import ugettext, ugettext_lazy as _

import re



def lowercase_email(email):
        """
        Normalize the address by lowercasing the domain part of the email
        address.
        """
        email = email or ''
        try:
            email_name, domain_part = email.strip().rsplit('@', 1)
        except ValueError:
            pass
        else:
            email = '@'.join([email_name.lower(), domain_part.lower()])
        return email

class SignupForm (forms.ModelForm):
	
	username =forms.CharField( 
		label='User Name',required=True,error_messages={'required': 'Please enter your user name','max_length':'15 letters length maximum!','min_length':'At least 3 letters'},max_length=15,min_length=3,widget=forms.TextInput(attrs={'placeholder':'3~15位字母/数字/汉字'}))
	email = forms.EmailField( error_messages={'required': 'Please enter your email','invalid':'email format invalid!'},
		label='Email',required=True,widget=forms.EmailInput(attrs={'placeholder':'Please enter email to activate your account!'}))
	password =forms.CharField( error_messages={'required': 'Please enter your password','max_length':'20 letters maximum!','min_length':'At least 6 letters!'},
		label='Password',required=True,max_length=20,widget = forms.PasswordInput(attrs={'placeholder':'Length between 6 to 20 letters'}))
	confirm_password= forms.CharField(error_messages={'required': 'Please enter your password','max_length':'maximun 20 letters!','min_length':'At least 6 letters!'},
		label='Confirm Password',required=True,max_length=20,min_length=6,widget = forms.PasswordInput(attrs={'placeholder':'Length between 6 to 20 letters'}))
	
	class Meta:
		model = get_user_model()
		fields = ("username","email","password",)
								

	def clean_email(self):
		UserModel = get_user_model()
		email=self.cleaned_data["email"]
		lower_email=lowercase_email(email)
		try:
			UserModel._default_manager.get(email=lower_email)
		except UserModel.DoesNotExist:
			return lower_email
		raise forms.ValidationError("E-mail address already existed, please login.")

	def clean_confirm_password(self):
		#cleaned_data=super(SignupForm,self).clean()
		password = self.cleaned_data.get("password",False)
		confirm_password = self.cleaned_data["confirm_password"]
		if  not( password == confirm_password):
			raise forms.ValidationError("Passwords are not identical!")
		return confirm_password

		

	def clean_username(self):
		UserModel = get_user_model()
		username = self.cleaned_data["username"]
		#Filter register username by sensitive word
		n=re.sub('[^\u4e00-\u9fa5a-zA-Z]','',username)
		
		mgc=['admin','icine','Donald Trump']		
		
		if n in mgc:
			raise forms.ValidationError("This name has been chosen, please change another one!")

		try:
			UserModel._default_manager.get(username = username)

		except UserModel.DoesNotExist:
			return username
		raise forms.ValidationError("This name has been chosen, please change another one!")


