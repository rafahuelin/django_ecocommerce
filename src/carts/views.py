from django.shortcuts import render


def cart_home(request):
    # print(request.session)
    # print(dir(request.session))
    # request.session.set_expiry(300) # 5 minutes
    # key = request.session.session_key
    # print(key)
    # request.session['first_name'] = "Rafa"  # Setter
    request.session['cart_id'] = 12  # Set
    request.session['user'] = request.user.username
    return render(request, "carts/home.html", {})
