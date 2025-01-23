import requests
import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CategoryForm, ProductForm, EditCategoryForm, EditProductForm
from django.http import JsonResponse

# Replace this with your Google Apps Script web app URL
GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxPmWpRAKT8fqL4_p3xlDOTRmia1JSdtj6ZU5FDQfM9W4RuPu6BDAG1ssvdQ0HLevXm/exec"

# Function to handle authentication with Google Apps Script API
def authenticate_user(username, password):
    if not username or not password:
        return False, "Username and password are required"

    payload = {
        'action': 'authenticate',
        'username': username,
        'password': password
    }
    
    try:
        response = requests.post(GOOGLE_SCRIPT_URL, json=payload, timeout=10)
        if response.status_code == 200:
            try:
                data = response.json()
                # Access the 'verified' dictionary
                verified_data = data.get('verified', {})
                authenticated = verified_data.get('authenticated', False)
                message = verified_data.get('message', "No message provided")

                if authenticated:
                    print('Authentication successful:', message)
                    return True, message
                else:
                    print('Authentication failed:', message)
                    return False, message
            except ValueError:
                return False, "Invalid JSON response from server"
        else:
            return False, f"Error: {response.status_code} - {response.reason}"
    except requests.exceptions.RequestException as e:
        return False, f"Request failed: {str(e)}"



def category_list(request):
    # Fetch categories
    response = requests.get(f"{GOOGLE_SCRIPT_URL}?action=getCategories")
    categories = response.json()

    # Fetch highlights
    highlights = get_highlights()

    # Pass both categories and highlights to the template
    context = {
        'categories': categories,
        'highlights': highlights,
    }
    return render(request, 'shop/category_list.html', context)

# Function to get category name from Google Sheets using Apps Script API
def get_category_name_from_sheet(category_id):
    url = f"{GOOGLE_SCRIPT_URL}?action=getCategoryById&categoryId={category_id}"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            data = response.json()
            return data.get('name', 'Unknown Category')
        except ValueError:
            print("Error: Response is not valid JSON")
            return None
    else:
        print(f"Error: Failed to fetch category with status code {response.status_code}")
        return None

def product_list(request, category_id):
    category_name = get_category_name_from_sheet(category_id)
    if category_name is None:
       category_name = 'Unknown Category'

    products_url = f"{GOOGLE_SCRIPT_URL}?action=getProducts&categoryId={category_id}"
    products_response = requests.get(products_url)
    products = products_response.json()

    context = {
        'category_name': category_name,
        'products': products,
    }
    return render(request, 'shop/product_list.html', context)

def product_detail(request, product_id):
    response = requests.get(f"{GOOGLE_SCRIPT_URL}?action=getProductDetails&productId={product_id}")
    product = response.json()
    return render(request, 'shop/product_detail.html', {'product': product})

def get_data(request):
    response = requests.get(GOOGLE_SCRIPT_URL)
    if response.status_code == 200:
        data = response.json()
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'error': 'Failed to fetch data'}, status=500)

@csrf_exempt
def add_row(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            payload = {
                'action': 'addRow',
                'data': data['data']
            }
            response = requests.post(GOOGLE_SCRIPT_URL, json=payload)
            return JsonResponse({'message': response.text}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid method'}, status=405)

@csrf_exempt
def delete_row(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            row_index = data['rowIndex']
            payload = {
                'action': 'deleteRow',
                'rowIndex': row_index
            }
            response = requests.post(GOOGLE_SCRIPT_URL, json=payload)
            return JsonResponse({'message': response.text}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid method'}, status=405)

@csrf_exempt
def reorder_rows(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            new_order = data['newOrder']
            payload = {
                'action': 'reorderRows',
                'newOrder': new_order
            }
            response = requests.post(GOOGLE_SCRIPT_URL, json=payload)
            return JsonResponse({'message': response.text}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid method'}, status=405)

@csrf_exempt
def add_row_at_index(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            row_index = data.get('rowIndex')
            new_data = data.get('newData')

            if not row_index or not new_data:
                return JsonResponse({"status": "error", "message": "Missing required fields"}, status=400)

            payload = {
                'action': 'insertRowAtIndex',
                'rowIndex': row_index,
                'newData': new_data
            }

            response = requests.post(GOOGLE_SCRIPT_URL, json=payload)

            if response.status_code == 200:
                return JsonResponse({"status": "success", "message": "Row inserted successfully"}, status=200)
            else:
                return JsonResponse({"status": "error", "message": "Failed to insert row", "details": response.text}, status=400)

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse({"status": "error", "message": "Invalid method"}, status=405)

def get_highlights():
    url = f"{GOOGLE_SCRIPT_URL}?action=getHighlights"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            data = response.json()
            if isinstance(data, dict) and "highlights" in data:
                return data["highlights"]
            elif isinstance(data, list):
                return data
            else:
                print("Unexpected data format:", data)
                return []
        except ValueError:
            print("Error: Invalid JSON format for highlights data. Raw response:", response.text)
            return []
    else:
        print(f"Error fetching highlights, status code: {response.status_code}, response: {response.text}")
        return []

def index(request):
    highlights = get_highlights()
    context = {
        "highlights": highlights
    }
    return render(request, "shop/index.html", context)


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        is_authenticated, message = authenticate_user(username=username, password=password)

        if is_authenticated:
            # Proceed with login or further steps
            return render(request, 'shop/index.html', {'user': username})  # Example, replace with actual user handling
        else:
            return render(request, 'shop/login.html', {'error': message})  # Display the error message

    return render(request, 'shop/login.html')


# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')
    
