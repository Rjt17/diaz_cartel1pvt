from django.http.response import HttpResponse
from django.shortcuts import render, redirect
import pymysql
from django.urls import reverse
import urllib.parse
import random

#global
cuisines_available = ['asian', 'burger', 'chinese', 'continental', 'dessert', 'european', 'fast food', 'french', 'ice cream', 'indian', 'italian', 'japanese', 'lebanese', 'maharashtrian', 'mediterranean', 'mexican', 'nepalese', 'north indian', 'oriental', 'pizza', 'sea food', 'shake', 'south indian', 'tea', 'thai', 'tibetian', 'turkish', 'vietnamese', 'waffle', 'world']

city = "jaipur"

#functions

def geolocation(request):
    ip = request.META.get('REMOTE_ADDR', None)
    print(f"ip is: {ip}")

def database():
    db = pymysql.connect(host="www.oggy.co.in",
                     user="sql6418117",
                     passwd="ixSFQAYA2h",
                     db="oggy")
    cur = db.cursor()
    return cur

def cities():
    cur = database()
    cur.execute("select name from cities")
    results = cur.fetchall()
    cities = []
    for x in results:
        cities.append("".join(x))
    return cities

def bulk_cuisines(cuisines):
    image_cuisines = []
    for x in cuisines:
        try:
            image_cuisine = x.split(",")
            image_cuisine = image_cuisine[0]
            image_cuisine = image_cuisine[1:]
            image_cuisine = image_cuisine.lower()
            if image_cuisine not in cuisines_available:
                image_cuisines.append('random')
            else:
                image_cuisines.append(image_cuisine)
        except:
            image_cuisines.append("random")
    return image_cuisines

def bulk_images(cuisines):
    image_originals = []
    for x in cuisines:
        try:
            if x != "random":
                image_original = x + str(random.randint(1,7))
                image_original = image_original + ".jpg"
                image_originals.append(image_original)
            else:
                image_original = "random" + str(random.randint(1,7))
                image_original = image_original + ".jpg"
                image_originals.append(image_original)
        except:
            image_originals.append("random")
    return image_originals

def image_cuisine(result_image):
    try:
        image_cuisine = result_image
        image_cuisine = image_cuisine[0]
        image_cuisine = image_cuisine.split(",")
        image_cuisine = image_cuisine[0]
        image_cuisine = image_cuisine[1:]
        image_cuisine = image_cuisine.lower()
        if image_cuisine not in cuisines_available:
            return "random"
        else:
            return image_cuisine
    except:
        image_cuisine = 'random'
        return image_cuisine
    
def image_original(result_image):
    try:
        if image_cuisine(result_image) != "random":
            image_original = image_cuisine(result_image) + str(random.randint(1,7))
            image_original = image_original + ".jpg"
            return image_original
        else:
            image_original = "random" + (random.randint(1,7))
            image_original = image_original + ".jpg"
            return image_original
    except:
        image_original = 'random'
        image_original += str(random.randint(1,7))
        image_original += ".jpg"
        return image_original

#redirectors
def home(request):
    geolocation(request)
    context = {
        'cities' : cities()
    }
    return render(request, 'index.html', context)

def about(request):
    context = {
        'cities' : cities()
    }
    return render(request, 'about-us.html', context)


def login(request):
    context = {
        'cities' : cities()
    }
    return render(request, 'login.html', context)

def restaurants(request):
    #if restaurants page is accessed directly this will give 404
    if request.GET.get('city') is None:
        return render(request, '404.html')

    rest_city = request.GET.get('city')
    rest_name = request.GET.get('restaurant')

    cur = database()

    #redirecting to offers page
    if len(rest_name) != 0:
        dec = {'city':rest_city, 'restaurant':rest_name}
        url = '{}?{}'.format(reverse('home-offer'), urllib.parse.urlencode(dec))
        return redirect(url)

    #get data
    cur.execute("select name, rating, cuisine, price, location from restaurants_dineout where city = %s", [rest_city])
    results = cur.fetchall()
    names = []
    ratings = []
    cuisines = []
    prices = []
    locations = []
    url = []
    for x in results:
        list_x = list(x)
        name = list_x[0]
        rating = list_x[1]
        cuisine = list_x[2]
        price = list_x[3]
        location = list_x[4]
        names.append(name)
        ratings.append(rating)
        cuisines.append(cuisine)
        prices.append(price)
        locations.append(location)
        url.append(urllib.parse.quote(name))
    image_cuisines = bulk_cuisines(cuisines)
    image_originals = bulk_images(image_cuisines)
    zipped_data = zip(names, ratings, url, cuisines, prices, locations, image_cuisines, image_originals)
        
    context = {
        'city' : rest_city,
        'name' : rest_name,
        'cities' : cities(),
        'data' : zipped_data
    }
    return render(request, 'restaurants.html', context)

def offer(request):
    rest_city = request.GET.get('city')
    rest_name = request.GET.get('restaurant')

    share_to_whatsapp = urllib.parse.quote(f"https://www.oggy.co.in/offer/?city={rest_city}&restaurant={urllib.parse.quote(rest_name)}")
        
    cur = database()
    cur.execute('select url from restaurants_swiggy where city = %s and name regexp %s', [rest_city, rest_name])
    swiggy_url = cur.fetchone()
    cur.execute('select url from restaurants_zomato where city = %s and name regexp %s', [rest_city, rest_name])
    zomato_url = cur.fetchone()
    cur.execute('select url from restaurants_eazydiner where city = %s and name regexp %s', [rest_city, rest_name])
    eazydiner_url = cur.fetchone()
    cur.execute('select url from restaurants_dineout where city = %s and name regexp %s', [rest_city, rest_name])
    dineout_url = cur.fetchone()
    cur.execute('select url from restaurants_magicpin where city = %s and name = %s', [rest_city, rest_name])
    magicpin_url = cur.fetchone()
    cur.execute('select cuisine from restaurants_dineout where city = %s and name = %s', [rest_city, rest_name])
    result_image = cur.fetchone()

    try:
        swiggy_url = list(swiggy_url)
        swiggy_url = swiggy_url[0]
    except:
        swiggy_url = "https://www.swiggy.com"
    
    try:
        zomato_url = list(zomato_url)
        zomato_url = zomato_url[0]
    except:
        zomato_url = "https://www.zomato.com"
    
    try:
        eazydiner_url = list(eazydiner_url)
        eazydiner_url = eazydiner_url[0]
    except:
        eazydiner_url = "https://www.eazydiner.com"

    try:
        dineout_url = list(dineout_url)
        dineout_url = dineout_url[0]
    except:
        dineout_url = "https://www.dineout.co.in"
    
    try:
        magicpin_url = list(magicpin_url)
        magicpin_url = magicpin_url[0]
    except:
        magicpin_url = "https://www.magicpin.in"

    cur.execute('select offers from restaurants_dineout where city = %s and name = %s', [rest_city, rest_name])
    offer_dineout = cur.fetchone()
    cur.execute('select offers from restaurants_swiggy where city = %s and name = %s', [rest_city, rest_name])
    offer_swiggy = cur.fetchone()
    cur.execute('select offers from restaurants_eazydiner where city = %s and name = %s', [rest_city, rest_name])
    offer_eazydiner = cur.fetchone()
    cur.execute('select offers from restaurants_zomato where city = %s and name = %s', [rest_city, rest_name])
    offer_zomato = cur.fetchone()
    cur.execute('select offers from restaurants_magicpin where city = %s and name = %s', [rest_city, rest_name])
    offer_magicpin = cur.fetchone()
    cur.execute('select rating, cuisine, price, location from restaurants_dineout where city = %s and name = %s', [rest_city, rest_name])
    results = cur.fetchall()
    ratings = []
    cuisines = []
    prices = []
    locations = []

    for x in results:
        list_x = list(x)
        rating = list_x[0]
        cuisine = list_x[1]
        price = list_x[2]
        location = list_x[3]
        ratings.append(rating)
        cuisines.append(cuisine)
        prices.append(price)
        locations.append(location)

    def None_offer_converter(data):
        try:
            if data is None:
                data = "No offers"
            else:
                data = list(data)
                data = data[0]
            return data
        except:
            return data

    def None_converter(data):
        try:
            if data == []:
                data = "-"
            else:
                data = data[0]
            return data
        except:
            return data

    offer_dineout = None_offer_converter(offer_dineout)
    offer_eazydiner = None_offer_converter(offer_eazydiner)
    offer_swiggy = None_offer_converter(offer_swiggy)
    offer_zomato = None_offer_converter(offer_zomato)
    offer_magicpin = None_offer_converter(offer_magicpin)
    ratings = None_converter(ratings)
    cuisines = None_converter(cuisines)
    prices = None_converter(prices)
    locations = None_converter(locations)
    if offer_zomato == "" or " ":
        offer_zomato = "No Offers"

    if offer_swiggy != "No Offers":
        offer_swiggy = offer_swiggy.split(",")

    context = {
        'city' : rest_city,
        'name' : rest_name,
        'rating' : ratings,
        'cuisine' : cuisines,
        'price' : prices,
        'location' : locations,
        'offer_dineout' : offer_dineout,
        'offer_swiggy' : offer_swiggy,
        'offer_eazydiner' : offer_eazydiner,
        'offer_zomato' : offer_zomato,
        'offer_magicpin' : offer_magicpin,
        'cities' : cities(),
        'swiggy_url' : swiggy_url,
        'zomato_url' : zomato_url,
        'dineout_url' : dineout_url,
        'eazydiner_url' : eazydiner_url,
        'magicpin_url' : magicpin_url,
        'image_cuisine' : image_cuisine(result_image),
        'image_original' : image_original(result_image),
        'share_to_whatsapp' : share_to_whatsapp

    }
    return render(request, 'offer.html', context)

def south(request):
    cur = database()
    cur.execute("select name, rating, cuisine, price, location from restaurants_dineout where city = 'jaipur' AND cuisine REGEXP 'South'")
    names = cur.fetchall()
    south_names = []
    south_rating = []
    south_cuisine = []
    south_price = []
    south_location = []
    south_encoded_url = []
    for x in names:
        list_x = list(x)
        name = list_x[0]
        rating = list_x[1]
        cuisine = list_x[2]
        price = list_x[3]
        location = list_x[4]
        if rating == "None":
            rating = "Not Enough Reviews"
        south_names.append(name)
        south_rating.append(rating)
        south_cuisine.append(cuisine)
        south_price.append(price)
        south_location.append(location)
        south_encoded_url.append(urllib.parse.quote(name))
    image_cuisines = bulk_cuisines(south_cuisine)
    image_originals = bulk_images(image_cuisines)
    zipped_data = zip(south_names, south_rating, south_encoded_url, south_cuisine, south_price, south_location, image_cuisines, image_originals)
    
    context = {
        'data' : zipped_data,
        'cities' : cities()
    }
    return render(request, 'south.html', context)
    
def pizza(request):
    cur = database()
    cur.execute("select name, rating, cuisine, price, location from restaurants_dineout where city = 'jaipur' AND cuisine REGEXP 'Pizza'")
    names = cur.fetchall()
    pizza_names = []
    pizza_rating = []
    pizza_cuisine = []
    pizza_price = []
    pizza_location = []
    pizza_encoded_url = []
    for x in names:
        list_x = list(x)
        name = list_x[0]
        rating = list_x[1]
        cuisine = list_x[2]
        price = list_x[3]
        location = list_x[4]
        if rating == "None":
            rating = "Not Enough Reviews"
        pizza_names.append(name)
        pizza_rating.append(rating)
        pizza_cuisine.append(cuisine)
        pizza_price.append(price)
        pizza_location.append(location)
        pizza_encoded_url.append(urllib.parse.quote(name))
    image_cuisines = bulk_cuisines(pizza_cuisine)
    image_originals = bulk_images(image_cuisines)
    zipped_data = zip(pizza_names, pizza_rating, pizza_encoded_url, pizza_cuisine, pizza_price, pizza_location, image_cuisines, image_originals)
    
    context = {
        'data' : zipped_data,
        'cities' : cities()
    }
    return render(request, 'pizza.html', context)
    
def burger(request):
    cur = database()
    cur.execute("select name, rating, cuisine, price, location from restaurants_dineout where city = 'jaipur' AND name REGEXP 'Burger'")
    names = cur.fetchall()
    burger_names = []
    burger_rating = []
    burger_cuisine = []
    burger_price = []
    burger_location = []
    burger_encoded_url = []
    for x in names:
        list_x = list(x)
        name = list_x[0]
        rating = list_x[1]
        cuisine = list_x[2]
        price = list_x[3]
        location = list_x[4]
        if rating == "None":
            rating = "Not Enough Reviews"
        burger_names.append(name)
        burger_rating.append(rating)
        burger_cuisine.append(cuisine)
        burger_price.append(price)
        burger_location.append(location)
        burger_encoded_url.append(urllib.parse.quote(name))
    image_cuisines = bulk_cuisines(burger_cuisine)
    image_originals = bulk_images(image_cuisines)
    zipped_data = zip(burger_names, burger_rating, burger_encoded_url, burger_cuisine, burger_price, burger_location, image_cuisines, image_originals)
    
    context = {
        'data' : zipped_data,
        'cities' : cities()
    }
    return render(request, 'burger.html', context)

def dessert(request):
    cur = database()
    cur.execute("select name, rating, cuisine, price, location from restaurants_dineout where city = 'jaipur' AND cuisine REGEXP 'Dessert'")
    names = cur.fetchall()
    dessert_names = []
    dessert_rating = []
    dessert_cuisine = []
    dessert_price = []
    dessert_location = []
    dessert_encoded_url = []
    for x in names:
        list_x = list(x)
        name = list_x[0]
        rating = list_x[1]
        cuisine = list_x[2]
        price = list_x[3]
        location = list_x[4]
        if rating == "None":
            rating = "Not Enough Reviews"
        dessert_names.append(name)
        dessert_rating.append(rating)
        dessert_cuisine.append(cuisine)
        dessert_price.append(price)
        dessert_location.append(location)
        dessert_encoded_url.append(urllib.parse.quote(name))
    image_cuisines = bulk_cuisines(dessert_cuisine)
    image_originals = bulk_images(image_cuisines)
    zipped_data = zip(dessert_names, dessert_rating, dessert_encoded_url, dessert_cuisine, dessert_price, dessert_location, image_cuisines, image_originals)
    
    context = {
        'data' : zipped_data,
        'cities' : cities()
    }
    return render(request, 'dessert.html', context)
    
#filters

def price(request):
    rest_city = request.GET.get('city')
    filter_data = request.GET.get('filter') 
    cur = database()

    #get data
    if filter_data == "hightolow":
        cur.execute("select name, rating, cuisine, price, location from restaurants_dineout where city = %s  ORDER BY 'price' DESC", [rest_city])
    else:
        cur.execute("select name, rating, cuisine, price, location from restaurants_dineout where city = %s  ORDER BY 'price' ASC", [rest_city])
    results = cur.fetchall()
    names = []
    ratings = []
    cuisines = []
    prices = []
    locations = []
    url = []
    for x in results:
        list_x = list(x)
        name = list_x[0]
        rating = list_x[1]
        cuisine = list_x[2]
        price = list_x[3]
        location = list_x[4]
        names.append(name)
        ratings.append(rating)
        cuisines.append(cuisine)
        prices.append(price)
        locations.append(location)
        url.append(urllib.parse.quote(name))
    image_cuisines = bulk_cuisines(cuisines)
    image_originals = bulk_images(image_cuisines)
    zipped_data = zip(names, ratings, url, cuisines, prices, locations, image_cuisines, image_originals)
        
    context = {
        'city' : rest_city,
        'cities' : cities(),
        'data' : zipped_data
    }
    return render(request, 'price.html', context)


def rating(request):
    rest_city = request.GET.get('city')
    filter_data = request.GET.get('filter') 
    cur = database()

    #get data
    if filter_data == "5":
        cur.execute("select name, rating, cuisine, price, location from restaurants_dineout where rating = 5 and city = %s", [rest_city])
    elif filter_data == "4":
        cur.execute("select name, rating, cuisine, price, location from restaurants_dineout where rating between 4 and 5 and city = %s", [rest_city])
    elif filter_data == "3":
        cur.execute("select name, rating, cuisine, price, location from restaurants_dineout where rating between 3 and 4 and city = %s", [rest_city])
    elif filter_data == "2":
        cur.execute("select name, rating, cuisine, price, location from restaurants_dineout where rating between 2 and 3 and city = %s", [rest_city])
    elif filter_data == "1":
        cur.execute("select name, rating, cuisine, price, location from restaurants_dineout where rating between 1 and 2 and city = %s", [rest_city])
    else:
        cur.execute("select name, rating, cuisine, price, location from restaurants_dineout where rating between 0 and 1 and city = %s", [rest_city])
    results = cur.fetchall()
    names = []
    ratings = []
    cuisines = []
    prices = []
    locations = []
    url = []
    for x in results:
        list_x = list(x)
        name = list_x[0]
        rating = list_x[1]
        cuisine = list_x[2]
        price = list_x[3]
        location = list_x[4]
        names.append(name)
        ratings.append(rating)
        cuisines.append(cuisine)
        prices.append(price)
        locations.append(location)
        url.append(urllib.parse.quote(name))
    image_cuisines = bulk_cuisines(cuisines)
    image_originals = bulk_images(image_cuisines)
    zipped_data = zip(names, ratings, url, cuisines, prices, locations, image_cuisines, image_originals)
        
    context = {
        'city' : rest_city,
        'cities' : cities(),
        'data' : zipped_data
    }
    return render(request, 'rating.html', context)

def cuisine(request):
    return render(request, 'cuisine.html')

