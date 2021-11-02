from django.http.response import HttpResponse
from django.shortcuts import render, redirect
import pymysql
from django.urls import reverse
import urllib.parse
import random
import requests
from bs4 import BeautifulSoup



#globals
cuisines_available = ['Afghani', 'African', 'American', 'Andhra', 'Arabian', 'Asian', 'Assamese', 'Australian', 'Awadhi', 'Bakery and Confectionary', 'Barbecue', 'Belgian', 'Bengali', 'Bihari', 'Biryani', 'Brazilian', 'British', 'Burger', 'Burmese', 'Cantonese', 'Chaat', 'Chettinad', 'Chinese', 'Coastal', 'Coffee', 'Contemporary Continental', 'Continental', 'Deli', 'Desserts', 'Doughnuts', 'Drinks', 'Ethiopian', 'European', 'Fast Food', 'Finger Food', 'French', 'Fusion', 'German', 'Goan', 'Greek', 'Gujarati', 'Haleem', 'Health Food', 'Hyderabadi', 'Ice Cream', 'Indian Cuisine', 'Indonesian', 'Iranian', 'Israeli', 'Italian', 'Japanese', 'Juice', 'Kashmiri', 'Kerala', 'Konkani', 'Korean', 'Latin American', 'Lebanese', 'Lucknowi', 'Maharashtrian', 'Malaysian', 'Malvani', 'Mangalorean', 'Mediterranean', 'Mexican', 'Middle Eastern', 'Mithai', 'Modern Indian', 'Moroccan', 'Mughlai', 'Multi-Cuisine', 'Naga', 'Nepalese', 'Nikkei', 'North Eastern', 'North Indian', 'North West Frontier', 'Odia', 'Oriental', 'Pakistani', 'Parsi', 'Persian', 'Pizza', 'Portuguese', 'Rajasthani', 'Russian', 'Seafood', 'Shakes', 'Sindhi', 'Singaporean', 'Sizzlers', 'South American', 'South Indian', 'Spanish', 'Street Food', 'Sushi', 'Tamil', 'Tea', 'Tex Mex', 'Thai', 'Tibetan', 'Turkish', 'Vietnamese', 'Waffle', 'Western', 'World Cuisine', 'Yogurt', 'Indian', 'All Day Dining', 'Bakery', 'Bangladeshi', 'Barbeque', 'Beverages', 'Burgers', 'Cafe', 'Casual Eclectic', 'Chicken', 'Cocktail Menu', 'Coffee and Tea', 'Confectionery', 'Cuban', 'Delicatessen ', 'Dim Sum', 'Drinks Only', 'Egyptian', 'Fish ', 'Healthy', 'Healthy Food', 'Indian Coastal Cuisine', 'Juices', 'Kababs', 'Konkan', 'Malaysian ', 'Milkshakes', 'Momos', 'Multicuisine', 'Nagaland', 'Oriya', 'Pan Asian', 'Parathas', 'Pasta', 'Progressive Indian Cuisine', 'Regional Indian', 'Salad', 'Sandwiches', 'Shawarma', 'Sindhi ', 'Sri Lankan', 'Steakhouse', 'Steaks', 'Tamil Nadu', 'Tapas', 'Tex-Mex', 'Vegan', 'oriental', 'Keventers & more', 'Attractive Combos Available', 'Bowl Company', 'Cold cuts', 'Combo', 'Fish & Seafood', 'Grill', 'Home Food', 'Ice Cream Cakes', 'Italian-American', 'Jain', 'Kebabs', 'Keto', 'Malwani', 'Mongolian', 'Mutton', 'Pan-Asian', 'Pastas', 'Pizzas', 'Popular Brand Store', 'Punjabi', 'Ready to cook meat', 'Salads', 'Snacks', 'Sweets', 'Tandoor', 'Tandoor ', 'Telangana', 'Thalis', 'indian', '8:15 To 11:30 Pm', 'Paan', 'Sandwich', 'Wraps', 'Rolls', 'Kebab', 'BBQ', 'Bar Food', 'Roast Chicken', 'Mishti', 'Raw Meats', 'Hot dogs', 'Afghan', 'Frozen Yogurt', 'Panini', 'Bubble Tea', 'Steak', 'Bohri', 'Jamaican']
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}

city = "jaipur"

#functions

def geolocation(request):
    ip = request.META.get('REMOTE_ADDR', None)
    #print(f"ip is: {ip}")

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

def rests_zomato():
    cur = database()
    cur.execute("select name from restaurants_zomato")
    results = cur.fetchall()
    rests = []
    for x in results:
        rests.append("".join(x))
    return rests


def bulk_cuisines(cuisines):
    image_cuisines = []
    for x in cuisines:
        try:
            image_cuisine = x.split(",")
            image_cuisine = image_cuisine[0]
            image_cuisine = image_cuisine[0:]
            image_cuisine = image_cuisine.title()
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
                image_original = x + str(random.randint(1,30))
                image_original = image_original + ".svg"
                image_originals.append(image_original)
            else:
                image_original = "random" + str(random.randint(1,30))
                image_original = image_original + ".svg"
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
        image_cuisine = image_cuisine[0:]
        image_cuisine = image_cuisine.title()
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
            image_original = image_cuisine(result_image) + str(random.randint(1,30))
            image_original = image_original + ".svg"
            return image_original
        else:
            image_original = "random" + (random.randint(1,30))
            image_original = image_original + ".svg"
            return image_original
    except:
        image_original = 'random'
        image_original += str(random.randint(1,7))
        image_original += ".svg"
        return image_original

#redirectors
def home(request):
    geolocation(request)
    context = {
        'cities' : cities(),
        'rests' : rests_zomato()
    }
    return render(request, 'index.html', context)

def about(request):
    context = {
        'cities' : cities()
    }
    return render(request, 'about-us.html', context)

def faq(request):
    context = {
        'cities' : cities()
    }
    return render(request, 'faq.html', context)

def privacy_policy(request):
    context = {
        'cities' : cities()
    }
    return render(request, 'privacy_policy.html', context)

def terms_of_use(request):
    context = {
        'cities' : cities()
    }
    return render(request, 'terms-of-use.html', context)


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
    cur.execute("select name, rating, cuisine, price, location from restaurants_zomato where city = %s", [rest_city])
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
    cur.execute('select cuisine from restaurants_zomato where city = %s and name = %s', [rest_city, rest_name])
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

    if zomato_url != "https://www.zomato.com":
        page = requests.get(zomato_url, headers=headers)
        content = page.content
        soup = BeautifulSoup(content, 'html.parser')
        #offers
        zomato_offers = []
        for parent in soup.find_all(class_='sc-1a03l6b-0 lkqupg'):
            if parent != None:
                offer = list(parent.get_text())
                for x in offer:
                    if x == "₹":
                        offer.remove("₹")
                current_offers = ""
                for x in offer:
                    current_offers += x
                offer = current_offers
                zomato_offers.append(offer)
        if zomato_offers == []:
            zomato_offers.append("No Offers")
        #offer codes
        codes = []
        for parent in soup.find_all(class_="sc-1a03l6b-1 kvnZBD"):
            if parent != None:
                offer = list(parent.get_text())
                for x in offer:
                    if x == "₹":
                        offer.remove("₹")
                current_offers = ""
                for x in offer:
                    current_offers += x
                offer = current_offers
                codes.append(offer)
        offer_with_codes = []
        if codes != []:
            for x, y in zip(zomato_offers, codes):
                offer_with_codes.append(x + "|" + y)
        #offer conversion from list to string
        if offer_with_codes != []:
            offers_final = ",".join(offer_with_codes)
        else:
            offers_final = "No Offers"
    else:
        offers_final = "No Offers"

    swiggy_offers = []
    if swiggy_url != "https://www.swiggy.com":
        page = requests.get(swiggy_url, headers=headers)
        content = page.content
        soup = BeautifulSoup(content, 'html.parser')
        #offers
        
        for parent in soup.find_all(class_="_3lvLZ"):
            if parent != None:
                swiggy_offers.append(parent.get_text())
            else:
                swiggy_offers.append("No Offers")
                break
    else:
        swiggy_offers.append("No Offers")
    """
    if eazydiner_url != "https://www.eazydiner.com":
        page = requests.get(eazydiner_url, headers=headers)
        content = page.content
        soup = BeautifulSoup(content, 'html.parser')
        for parent in soup.find_all(class_="bold font-14 lh-20 grey-dark mt-10 mb-15"):
            print(parent)
    """
        
    cur.execute('select offers from restaurants_dineout where city = %s and name = %s', [rest_city, rest_name])
    offer_dineout = cur.fetchone()
    cur.execute('select offers from restaurants_swiggy where city = %s and name = %s', [rest_city, rest_name])
    offer_swiggy = cur.fetchone()
    cur.execute('select offers from restaurants_eazydiner where city = %s and name = %s', [rest_city, rest_name])
    offer_eazydiner = cur.fetchone()
    cur.execute('select offers from restaurants_magicpin where city = %s and name = %s', [rest_city, rest_name])
    offer_magicpin = cur.fetchone()
    cur.execute('select rating, cuisine, price, location from restaurants_zomato where city = %s and name = %s', [rest_city, rest_name])
    results = cur.fetchall()
    if results == ():
        cur.execute('select rating, cuisine, price, location from restaurants_dineout where city = %s and name = %s', [rest_city, rest_name])
        results = cur.fetchall()
    if results == ():
        cur.execute('select rating, cuisine, price, location from restaurants_eazydiner where city = %s and name = %s', [rest_city, rest_name])
        results = cur.fetchall()
    if results == ():
        cur.execute('select rating, cuisine, price, location from restaurants_swiggy where city = %s and name = %s', [rest_city, rest_name])
        results = cur.fetchall()
    if results == ():
        cur.execute('select rating, cuisine, price, location from restaurants_magicpin where city = %s and name = %s', [rest_city, rest_name])
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
    offer_magicpin = None_offer_converter(offer_magicpin)
    ratings = None_converter(ratings)
    cuisines = None_converter(cuisines)
    prices = None_converter(prices)
    locations = None_converter(locations)

    if offer_swiggy != "No Offers":
        offer_swiggy = offer_swiggy.split(",")
    
    if offers_final != "No Offers":
        offers_final = offers_final.split(",")

    context = {
        'city' : rest_city,
        'name' : rest_name,
        'rating' : ratings,
        'cuisine' : cuisines,
        'price' : prices,
        'location' : locations,
        'offer_dineout' : offer_dineout,
        'offer_swiggy' : swiggy_offers,
        'offer_eazydiner' : offer_eazydiner,
        'offer_zomato' : offers_final,
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

