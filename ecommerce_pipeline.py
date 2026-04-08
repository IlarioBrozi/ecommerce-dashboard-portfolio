import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df=pd.read_csv("ecommerce_sales_light.csv")

# Remove duplicates
df = df.drop_duplicates()

# Handle missing values
df["amount"] = df["amount"].fillna(0)

# Convert date column to datetime
df["date"] = pd.to_datetime(df["date"])

# Add month
df["month"] = df["date"].dt.month

#create sales categories
def sales_category(x):
    if x < 150:
        return "low"
    elif x <=200:
        return "medium"
    else:
        return "high"
df["sales_category"] = df["amount"].apply(sales_category)

#discounted sales 10%
df["discounted_sales"] = df["amount"] * 0.9

# Total sales per customer
total_sales_customer = df.groupby("customer")["discounted_sales"].sum().reset_index()

# Total sales per category
total_sales_category = df.groupby("category")["discounted_sales"].sum().reset_index()

# Average sales per category
avg_sales_category = df.groupby("customer")["discounted_sales"].mean().reset_index()

# Monthly sales trend
monthly_sales = df.groupby("month")["discounted_sales"].sum().reset_index()

# Bar plot: total sales per custome category
sns.barplot(data=total_sales_category, x="category",y="discounted_sales")
plt.title("Total Discounted Sales per Category")
plt.xticks(rotation=45)  # tilt labels
plt.savefig("sales_by_category.png")  # saves the file
plt.show()

# Bar plot: total sales per customer
sns.barplot(data=total_sales_customer, x="customer",y="discounted_sales")
plt.title("Total Discounted Sales per Customer")
plt.xticks(rotation=45)  # tilt labels
plt.savefig("sales_by_customer.png")  # saves the file
plt.show()

# Line plot: monthly sales trend
sns.lineplot(data=monthly_sales, x="month",y="discounted_sales",marker="o")
plt.title("Monthly Discounted Sales Trend")
plt.xticks(rotation=45)  # tilt labels
plt.savefig("sales_by_customer.png")  # saves the file
plt.show()

# calculate growth rate
monthly_sales["growth"] = monthly_sales["discounted_sales"].pct_change()

avg_growth = monthly_sales["growth"].mean()

last_month_sales = monthly_sales["discounted_sales"].iloc[-1]

# forecast next month
forecast = last_month_sales*(1+avg_growth)

print("Predicted next month sales:", round(forecast, 2))

# identify low value customers

threshold = total_sales_customer["discounted_sales"].mean()

low_customers = total_sales_customer[total_sales_customer["discounted_sales"] < threshold]

# promo strategy
def promo_strategy(amount):
    if amount < 550:
        return "20% discount coupon"
    elif amount < 680:
        return "10% discount + free shipping"
    else:
        return "Loyalty program"
    
low_customers["promotion"] = low_customers["discounted_sales"].apply(promo_strategy)

#csv creation
df.to_csv("cleaned_sales_data.csv", index=False)
total_sales_customer.to_csv("customer_summary.csv", index=False)
monthly_sales.to_csv("monthly_sales.csv", index=False)
low_customers.to_csv("cust_promo.csv", index=False)
