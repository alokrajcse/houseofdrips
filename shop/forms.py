from django import forms

class CategoryForm(forms.Form):
    id = forms.CharField(label="Category ID", max_length=100)
    name = forms.CharField(label="Category Name", max_length=100)
    description = forms.CharField(label="Description", widget=forms.Textarea)

class ProductForm(forms.Form):
    id = forms.CharField(label="Product ID", max_length=100)
    name = forms.CharField(label="Product Name", max_length=100)
    description = forms.CharField(label="Description", widget=forms.Textarea)
    price = forms.DecimalField(label="Price", max_digits=10, decimal_places=2)
    categoryId = forms.CharField(label="Category ID", max_length=100)
    imageUrl = forms.URLField(label="Image URL")

class EditCategoryForm(forms.Form):
    id = forms.CharField(label="Category ID", max_length=100, widget=forms.HiddenInput)
    name = forms.CharField(label="Category Name", max_length=100)
    description = forms.CharField(label="Description", widget=forms.Textarea)

class EditProductForm(forms.Form):
    id = forms.CharField(label="Product ID", max_length=100, widget=forms.HiddenInput)
    name = forms.CharField(label="Product Name", max_length=100)
    description = forms.CharField(label="Description", widget=forms.Textarea)
    price = forms.DecimalField(label="Price", max_digits=10, decimal_places=2)
    categoryId = forms.CharField(label="Category ID", max_length=100)
    imageUrl = forms.URLField(label="Image URL")
