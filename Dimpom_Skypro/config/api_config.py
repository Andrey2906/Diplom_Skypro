BASE_URL_V2 = "https://web-agr.chitai-gorod.ru/web/api/v2/products"
BASE_URL_V1 = "https://web-agr.chitai-gorod.ru/web/api/v1/"
TOKEN = "Bearer%20eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9."
"eyJpc3MiOiJodHRwczovL3VzZXItcmlnaHQiLCJzdWIiOjI5Njcy"
"MzgwLCJpYXQiOjE3ODQ3MTE5OTEsImV4cCI6MTc4NDcxNTU5MSwi"
"dHlwZSI6MjAsImp0aSI6IjAxOWY4OTFmLWQyMDYtNzU4MS04N2Fl"
"LWM5NGNiNGIxYTZmMyIsInJvbGVzIjoxMH0.H__1gW1Wpd6Ag7qP"
"xmQ5blYFg_K3gLuOH-0Y0Ol_GC16S43Zfb-4V4HLkyC6qPM7N8dV_"
"sZIntzBZGH2t0_EwyedlprtY9jjx_81yqwPo0HXoLQqcwB5QZbRBz"
"OPEha95lj6TMlAMfn7sYJ5kr8wHHqqLxXnIezeZqqjl3yRvs2ashJ"
"OuvXI31UmPDHT11Qy6geR-Srd3RlCK6Mrt7NERmQBDztoZiEAAws"
"KKs-Ttlz2h1J0kyPyu9HIAt3snqAVqzYsJs3uutNTwc_Db53Fu49"
"mAwX2jZz4GiSxeWOjkE7V435-uec17K1Kf8I80gNOM_fdg_"
"8eb4cTfGmKmSiZNA"
HEADERS = {
    "Authorization": TOKEN,
    "Content-Type": "application/json",
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0",
    "Origin": "https://www.chitai-gorod.ru",
    "Referer": "https://www.chitai-gorod.ru/"
}

list_books_params = {
    "include": "productTexts,publisher",
    "forceFilters[categories]": "18030",
    "products[page]": "1"
}
