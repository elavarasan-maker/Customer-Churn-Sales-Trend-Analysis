import pandas as pd
from pathlib import Path
df=pd.read_csv(Path(__file__).with_name("ecommerce_sales.csv"),parse_dates=["Order_Date"])
df["Year"]=df.Order_Date.dt.year; df["Month"]=df.Order_Date.dt.month
df["Month_Name"]=df.Order_Date.dt.strftime("%b"); df["Day_of_Week"]=df.Order_Date.dt.day_name()
df["Average_Order_Value"]=df.Revenue/df.Quantity
segment=df.groupby("Customer_Segment").agg(Orders=("Order_ID","nunique"),Revenue=("Revenue","sum"),Units=("Quantity","sum"))
segment["Revenue_Share_%"]=(segment.Revenue/df.Revenue.sum()*100).round(2)
print("Revenue by segment:\n",segment.sort_values("Revenue",ascending=False))
monthly=df.pivot_table(index=["Year","Month","Month_Name"],values="Revenue",aggfunc="sum").reset_index().sort_values(["Year","Month"])
monthly["MoM_Change_%"]=monthly.Revenue.pct_change().mul(100).round(2)
print("\nMonthly revenue trend:\n",monthly.to_string(index=False))
print("\nRegion x product pivot:\n",pd.pivot_table(df,index="Region",columns="Product",values="Revenue",aggfunc="sum",fill_value=0))
top_product=df.groupby("Product").Revenue.sum().idxmax()
top_region=df.groupby("Region").Revenue.sum().idxmax()
top_segment=segment.Revenue.idxmax()
summary=f"BUSINESS INSIGHTS\n- Top revenue segment: {top_segment}.\n- Top product: {top_product}.\n- Top region: {top_region}.\n\nRECOMMENDATIONS\n- Test retention offers for the leading customer segment.\n- Review stock and cross-selling for the leading product.\n- Study the leading region's practices before replicating them.\n- Investigate weak months before increasing marketing spend.\n"
Path(__file__).with_name("business_recommendations.txt").write_text(summary,encoding="utf-8")
monthly.to_csv(Path(__file__).with_name("monthly_revenue_trend.csv"),index=False)
print(summary)
