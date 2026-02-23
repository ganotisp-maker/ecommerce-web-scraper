import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------
# SCRAPING ΠΟΛΛΑΠΛΩΝ ΣΕΛΙΔΩΝ
# -------------------------------

products = []

for page in range(1, 6):   # Για αρχή 5 σελίδες

    if page == 1:
        url = "https://books.toscrape.com/"
    else:
        url = f"https://books.toscrape.com/catalogue/page-{page}.html"

    print(f"Scraping page {page}...")

    response = requests.get(url)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")

    items = soup.select(".product_pod")

    for item in items:
        name = item.h3.a["title"]
        price = item.select_one(".price_color").text
        availability = item.select_one(".availability").text.strip()

        products.append({
            "Name": name,
            "Price": price,
            "Availability": availability
        })

# -------------------------------
# DATAFRAME
# -------------------------------

df = pd.DataFrame(products)

# Καθαρισμός τιμής
df["Price"] = (
    df["Price"]
    .str.replace("£", "", regex=False)
    .str.replace("Â", "", regex=False)
    .astype(float)
)

# -------------------------------
# ΣΤΑΤΙΣΤΙΚΑ
# -------------------------------

average_price = round(df["Price"].mean(), 2)
max_price = df["Price"].max()
min_price = df["Price"].min()

print("\n--- STATISTICS ---")
print("Total products:", len(df))
print("Average price:", average_price)
print("Most expensive:", max_price)
print("Cheapest:", min_price)

# -------------------------------
# TOP 10 ΑΚΡΙΒΟΤΕΡΑ
# -------------------------------

top10 = df.sort_values(by="Price", ascending=False).head(10)

print("\n--- TOP 10 MOST EXPENSIVE BOOKS ---")
print(top10[["Name", "Price"]])

# -------------------------------
# EXPORT TO EXCEL
# -------------------------------

with pd.ExcelWriter("products.xlsx") as writer:
    df.to_excel(writer, sheet_name="All Products", index=False)
    top10.to_excel(writer, sheet_name="Top 10", index=False)

print("\nExcel file created: products.xlsx")

# -------------------------------
# HISTOGRAM
# -------------------------------

plt.figure()
plt.hist(df["Price"], bins=10)
plt.title("Price Distribution")
plt.xlabel("Price")
plt.ylabel("Number of Books")
plt.tight_layout()
plt.savefig("price_distribution.png")
plt.show()

# -------------------------------
# BAR CHART TOP 10
# -------------------------------

plt.figure()
plt.barh(top10["Name"], top10["Price"])
plt.xlabel("Price")
plt.title("Top 10 Most Expensive Books")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("top10.png")
plt.show()

print("\nCharts saved as images (price_distribution.png & top10.png)")
print("DONE ✅")