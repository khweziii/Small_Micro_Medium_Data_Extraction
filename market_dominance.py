import pandas as pd
import tabula
import re
from remove_duplicates import remove_duplicate_lists, remove_empty_lists, remove_problem_lists
from list_cleaner import extract_label_and_grouped_numbers

pagesToBeExtracted = ['17','15', '15','20','19','21']
tableOrder = [0,0,1,1,0,0]
allReports = ['Report-64-20-012007.pdf', 'Report-64-20-012009.pdf', 'Report-64-20-012012.pdf', 'Report-64-20-012015.pdf','Report-64-20-012018.pdf', 'Report-64-20-012022.pdf']
yearReports = [2007, 2009, 2012, 2015, 2018, 2022]
listRetreival = [[5,6,7],[5,6,7]]
pagesToBeExtracted2 = ['20','19','21']
tableOrder2 = [1,0,0]
yearReports2 = [2015, 2018, 2022]
fromReports = ['Report-64-20-012015.pdf','Report-64-20-012018.pdf', 'Report-64-20-012022.pdf']

market_dominance_column_names = ['Year','Business_Type', 'Total Income', 'Income_5_largest_enterprises',
                                 'Concentration_Ratio_5', 'Income_10_largest_enterprises',
                                 'Concentration_Ratio_10', 'Income_20_largest_enterprises',
                                 'Concentration_Ratio_20']

market_dominance_df = pd.DataFrame(columns=market_dominance_column_names)

result_append = pd.DataFrame(columns=market_dominance_column_names)


market_dominance_df_2 = pd.DataFrame(columns=market_dominance_column_names)

## -------------------------------------2007, 2009 and 2012-----------------------------------------------##
for index_parent,value_parent in enumerate(allReports[:3]):
    # Extract tables from PDF
    print('-----------------------------------------')
    print(f'Processing {allReports[index_parent]}, with parameters page:{pagesToBeExtracted[index_parent]}, tableOrder:{tableOrder[index_parent]} and year:{yearReports[index_parent]}')

    tables = tabula.read_pdf(allReports[index_parent], pages=pagesToBeExtracted[index_parent]) # allReports, pagesToBeExtracted

    table = tables[tableOrder[index_parent]].apply(lambda x: x.str.strip() if x.dtype == "object" else x) # tableOrder


    table_columns = list(table.columns)
    table_values = table.values.tolist() # converting an n-dimensional array to a list of nested strings

    search_words = ['Unnamed', 'Item', 'nan', 'total']
    digits = r"^\d+" # checks the string to see if it starts with a digit
    #
    filtered_list_columns = [s for s in table_columns if not any(re.search(re.escape(word), s, re.IGNORECASE) for word in search_words)]
    #
    filtered_list_values_comp = [[value for value in nested_list if re.search(digits, str(value))] for nested_list in
                                 table_values]
    #
    filtered_list_values_clean_comp = remove_duplicate_lists([[value for index, value in enumerate(nested_list) if index <= 2] for nested_list in
                                       filtered_list_values_comp])

    filtered_list_values_extra_clean_comp = remove_empty_lists(filtered_list_values_clean_comp)

    filtered_list_values_extra_clean_2_comp = remove_problem_lists(filtered_list_values_extra_clean_comp)


    market_dominance_column_names = ['Year','Business_Type', 'Total Income', 'Income_5_largest_enterprises',
                                     'Concentration_Ratio_5', 'Income_10_largest_enterprises',
                                     'Concentration_Ratio_10', 'Income_20_largest_enterprises',
                                     'Concentration_Ratio_20']
    #
    market_dominance_df = pd.DataFrame(columns=market_dominance_column_names)
    #
    for index_child, value_child in enumerate(filtered_list_columns):

        new_row = {'Year':yearReports[index_parent], 'Business_Type':filtered_list_columns[index_child],
                   'Total Income': int("".join(filtered_list_values_extra_clean_2_comp[0][index_child].split())),
                   'Concentration_Ratio_5': float(filtered_list_values_extra_clean_2_comp[2][index_child].replace(",",".")),
                   'Income_10_largest_enterprises': int("".join(filtered_list_values_extra_clean_2_comp[3][index_child].split())),
                   'Concentration_Ratio_10': float(filtered_list_values_extra_clean_2_comp[4][index_child].replace(",",".")),
                   'Income_20_largest_enterprises': int("".join(filtered_list_values_extra_clean_2_comp[5][index_child].split())),
                   'Concentration_Ratio_20': float(filtered_list_values_extra_clean_2_comp[6][index_child].replace(",","."))
               }

        market_dominance_df.loc[len(market_dominance_df)] = new_row

    market_dominance_df['Income_5_largest_enterprises'] = (market_dominance_df['Concentration_Ratio_5'] / 100) * \
                                                          market_dominance_df['Total Income']

    market_dominance_df['Income_5_largest_enterprises'] = market_dominance_df[
        'Income_5_largest_enterprises'].astype(int)

    # market_dominance_df.to_csv('Market_Dominance.csv')
    result_append = pd.concat([result_append, market_dominance_df], ignore_index=True)

    print('-----------------------------------------')
    print(f'Done Processing {allReports[index_parent]}, with parameters page:{pagesToBeExtracted[index_parent]}, tableOrder:{tableOrder[index_parent]} and year:{yearReports[index_parent]}')
## -------------------------------------2007, 2009 and 2012-----------------------------------------------##




## -------------------------------------2015, 2018 and 2022-----------------------------------------------##
filtered_columns = ['Restaurants and coffee shops', 'Takeaway and fast-food outlets', 'Caterers and other catering services']
filtered_values_2015 = []
filtered_values_2018 = []
filtered_values_2022 = []
filtered_values_all = []


for index_parent_2, value_parent_2 in enumerate(fromReports):

    filtered_values = []
    print('-----------------------------------------')
    print(f'Processing {value_parent_2}, with parameters page:{pagesToBeExtracted2[index_parent_2]}, tableOrder:{tableOrder2[index_parent_2]} and year:{yearReports2[index_parent_2]}')

    tables_2 = tabula.read_pdf(fromReports[index_parent_2], pages=pagesToBeExtracted2[index_parent_2]) # allReports, pagesToBeExtracted

    table_2 = tables_2[tableOrder2[index_parent_2]].apply(lambda x: x.str.strip() if x.dtype == "object" else x) # tableOrder

    table_values_2 = table_2.values.tolist()  # converting an n-dimensional array to a list of nested strings

    for index, value in enumerate(table_values_2):

        if value_parent_2 == 'Report-64-20-012015.pdf':
            if index == 5:
                print(index)
                print(value[1:])
                filtered_values_2015.append(value[1:])

            if index == 6:
                print(index)
                print(value[1:])
                filtered_values_2015.append(value[1:])

            if index == 7:
                print(index)
                print(value[1:])
                filtered_values_2015.append(value[1:])

        if value_parent_2 == 'Report-64-20-012018.pdf':
            if index == 5:
                print(index)
                print(extract_label_and_grouped_numbers(value))
                print(value)

                filtered_values_2018.append(extract_label_and_grouped_numbers(value)[1:])

            if index == 6:
                print(index)
                print(extract_label_and_grouped_numbers(value))
                print(value)

                filtered_values_2018.append(extract_label_and_grouped_numbers(value)[1:])

            if index == 7:
                print(index)
                print(extract_label_and_grouped_numbers(value))
                print(value)

                filtered_values_2018.append(extract_label_and_grouped_numbers(value)[1:])

        if value_parent_2 == 'Report-64-20-012022.pdf':
            if index == 1:
                print(index)
                print(value)
                filtered_values_2022.append(value[1:])

            if index == 2:
                print(index)
                print(value)
                filtered_values_2022.append(value[1:])

            if index == 3:
                print(index)
                print(value[1:])
                filtered_values_2022.append(value[1:])


    print('-----------------------------------------')
    print(f'Processing {value_parent_2}, with parameters page:{pagesToBeExtracted2[index_parent_2]}, tableOrder:{tableOrder2[index_parent_2]} and year:{yearReports2[index_parent_2]}')

filtered_values_all.append(filtered_values_2015)
filtered_values_all.append(filtered_values_2018)
filtered_values_all.append(filtered_values_2022)

for index_parent_3, value_parent_3 in enumerate(filtered_values_all):

    for index_child_3, value_child_3 in enumerate(filtered_columns):


        for bus_type in range(0,3):

            new_row = {'Year': yearReports2[index_child_3],
                       'Business_Type': filtered_columns[bus_type],
                       'Total Income': int("".join(filtered_values_all[index_child_3][bus_type][0].split())),
                       'Income_5_largest_enterprises':int("".join(filtered_values_all[index_child_3][bus_type][1].split())),
                       'Concentration_Ratio_5': float(filtered_values_all[index_child_3][bus_type][2].replace(",",".")),
                       'Income_10_largest_enterprises': int("".join(filtered_values_all[index_child_3][bus_type][3].split())),
                       'Concentration_Ratio_10': float(filtered_values_all[index_child_3][bus_type][4].replace(",",".")),
                       'Income_20_largest_enterprises': int("".join(filtered_values_all[index_child_3][bus_type][5].split())),
                       'Concentration_Ratio_20': float(filtered_values_all[index_child_3][bus_type][6].replace(",","."))
                           }

            market_dominance_df_2.loc[len(market_dominance_df_2)] = new_row

    break

market_dominance_df_2.drop_duplicates()

df_append = pd.concat([result_append, market_dominance_df_2], ignore_index=True)

df_append.to_csv('Market_Dominance_complete.csv',header=True,index=False)
## -------------------------------------2015, 2018 and 2022-----------------------------------------------##

