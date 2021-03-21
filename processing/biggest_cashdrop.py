import pandas as pd
import numpy as np
import altair as alt

def generate_plot(element="Production", compared_year=1995):
    stacked = None
    stacked2 = None
    prod = df_sum[df_sum["Element"] == element].reset_index(drop=True)
    count = 0
    items = ["Cereals", "Citrus Fruit", "Fibre Crops", "Fruit", "Pulses", "Roots and Tubers", "Sugar Crops", "Treenuts", "Vegetables", "Oilcrops"]
    areas = ["World", "Africa", "Asia", "Americas", "Europe", "Oceania"]
    for area in areas:
        df = prod[prod["Area"] == area]
        for item in items:
            year_df = df[df["Year"] == compared_year]
            year_value = year_df[year_df["Item"] == item]["Value"].reset_index(drop=True)[0]
            df.loc[df['Item']== item, 'Value'] = ((df[df["Item"] == item]["Value"] - year_value)/year_value)*100

        base = alt.Chart(df).mark_line().encode(
            x=alt.X('Year', scale=alt.Scale(domain=[1960, 2020])),
            y=alt.Y('Value', title=f"{element} % vs {compared_year}"),
            color=alt.condition(highlight, 'Item', alt.ColorValue('lightgray')),
            tooltip=['Domain', 'Item', 'Year', 'Value']
        ).properties(
            title=f"{area} {element}"
        )
        points = base.mark_circle().encode(
            opacity=alt.value(0)
        ).add_selection(
            highlight
        )

        lines = base.mark_line().encode(
            size=alt.condition(~highlight, alt.value(1), alt.value(3))
        )
        current = lines + points
        if count < 3:
            if stacked is None:
                stacked = current
            else:
                stacked = stacked | current
        else:
            if stacked2 is None:
                stacked2 = current
            else:
                stacked2 = stacked2 | current
        count +=1

    final_plot = stacked & stacked2

    final_plot.save(f"../html/cashdrop_{element}.html", embed_options={'renderer':'svg'})

# utf-16 bc the format in this file has some WEIRD starting bytes idk why
df_sum = pd.read_csv("https://raw.githubusercontent.com/ignacioVidaurreta/infovis/gh-pages/datasets/harvested_crops_summary.csv", sep='\t', encoding="utf-16")

# Renaming because weird names make weird plots
# This is the opposite of DRY, this is wet but it works.
# I'm sorry for failing you Clean Code
df_sum.update(df_sum["Item"].replace({"Cereals, Total": "Cereals"}))
df_sum.update(df_sum["Item"].replace({"Citrus Fruit, Total": "Citrus Fruit"}))
df_sum.update(df_sum["Item"].replace({"Fibre Crops Primary": "Fibre Crops"}))
df_sum.update(df_sum["Item"].replace({"Fruit Primary": "Fruit"}))
df_sum.update(df_sum["Item"].replace({"Pulses, Total": "Pulses"}))
df_sum.update(df_sum["Item"].replace({"Roots and Tubers, Total": "Roots and Tubers"}))
df_sum.update(df_sum["Item"].replace({"Sugar Crops Primary": "Sugar Crops"}))
df_sum.update(df_sum["Item"].replace({"Treenuts, Total": "Treenuts"}))
df_sum.update(df_sum["Item"].replace({"Vegetables Primary": "Vegetables"}))

highlight = alt.selection(
	type='single', on='mouseover',
	fields=['Item'], nearest=True
)

elements = ["Area harvested", "Yield", "Production"]
for elem in elements:
	generate_plot(elem)