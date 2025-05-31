import pandas as pd
import tabula
import re
from remove_duplicates import remove_duplicate_lists, remove_empty_lists, remove_problem_lists
from list_cleaner import extract_label_and_grouped_numbers

#---------------------------------- 2007, 2009 and 2012 Parameters------------------------------------#
pagesToBeExtracted = ['16','15', '15']
tableOrder = [0,0,0]
allReports = ['Report-64-20-012007.pdf', 'Report-64-20-012009.pdf', 'Report-64-20-012012.pdf']
yearReports = [2007, 2009, 2012]
business_types = ['Restaurants and coffee shops', 'Takeaway/fast-food outlets', 'Caterers and other catering services']
size_types_2007 = ['Large', 'Medium', 'Small', 'Micro']
size_types_2012 = ['Large', 'Medium','Small and Micro']
#---------------------------------- 2007, 2009 and 2012 Parameters------------------------------------#

#---------------------------------- 2015, 2018 and 2022 Parameters------------------------------------#
pagesToBeExtracted2 = ['20','18','20']
tableOrder2 = [0,1,1]
yearReports2 = [2015, 2018, 2022]
fromReports = ['Report-64-20-012015.pdf','Report-64-20-012018.pdf', 'Report-64-20-012022.pdf']
#---------------------------------- 2015, 2018 and 2022 Parameters------------------------------------#

income_column_names = ['Year','Business_Type', 'Small', 'Micro','Medium', 'Large']

income_column_names_2 = ['Year','Business_Type', 'Small and Micro','Medium', 'Large']

income_by_business_size_df = pd.DataFrame(columns=income_column_names)

result_append = pd.DataFrame(columns=income_column_names)

result_append_2 = pd.DataFrame(columns=income_column_names_2)

income_by_business_size_df_2007 = pd.DataFrame(columns=income_column_names)

income_by_business_size_df_2012 = pd.DataFrame(columns=income_column_names_2)

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

    income_by_business_size_df_2007 = pd.DataFrame(columns=income_column_names)

    if yearReports[index_parent] == 2007:

        for index_child, value_child in enumerate(business_types):

            new_row = {'Year':yearReports[index_parent],
                       'Business_Type':business_types[index_child],
                       'Large': int("".join(filtered_list_values_extra_clean_2_comp[0][index_child].split())),
                       'Medium': int("".join(filtered_list_values_extra_clean_2_comp[1][index_child].split())),
                       'Small': int("".join(filtered_list_values_extra_clean_2_comp[2][index_child].split())),
                       'Micro': int("".join(filtered_list_values_extra_clean_2_comp[3][index_child].split()))
                   }

            print(new_row)

            income_by_business_size_df_2007.loc[len(income_by_business_size_df_2007)] = new_row

        result_append = pd.concat([result_append, income_by_business_size_df_2007], ignore_index=True)

    elif yearReports[index_parent] == 2009:

        for index_child, value_child in enumerate(business_types):

            new_row = {'Year':yearReports[index_parent],
                       'Business_Type':business_types[index_child],
                       'Large': 0,
                       'Medium': 0,
                       'Small': 0,
                       'Micro': 0
            }

            print(new_row)

            income_by_business_size_df_2007.loc[len(income_by_business_size_df_2007)] = new_row

        result_append = pd.concat([result_append, income_by_business_size_df_2007], ignore_index=True)


    elif yearReports[index_parent] == 2012:

        for index_child, value_child in enumerate(business_types):

            print(filtered_list_values_extra_clean_2_comp)

            new_row = {'Year': yearReports[index_parent],
                       'Business_Type': business_types[index_child],
                       'Large': int("".join(filtered_list_values_extra_clean_2_comp[index_child][2].split())),
                       'Medium': int("".join(filtered_list_values_extra_clean_2_comp[index_child][1].split())),
                       'Small and Micro': int("".join(filtered_list_values_extra_clean_2_comp[index_child][0].split()))
                       }

            print(new_row)

            income_by_business_size_df_2012.loc[len(income_by_business_size_df_2012)] = new_row


        result_append_2 = pd.concat([result_append_2, income_by_business_size_df_2012], ignore_index=True)

    print('-----------------------------------------')
    print(f'Done Processing {allReports[index_parent]}, with parameters page:{pagesToBeExtracted[index_parent]}, tableOrder:{tableOrder[index_parent]} and year:{yearReports[index_parent]}')
## -------------------------------------2007, 2009 and 2012-----------------------------------------------##




## -------------------------------------2015, 2018 and 2022-----------------------------------------------##

for index_parent,value_parent in enumerate(fromReports[:3]):
    # Extract tables from PDF
    print('-----------------------------------------')
    print(f'Processing {fromReports[index_parent]}, with parameters page:{pagesToBeExtracted2[index_parent]}, tableOrder:{tableOrder2[index_parent]} and year:{yearReports2[index_parent]}')

    tables = tabula.read_pdf(fromReports[index_parent], pages=pagesToBeExtracted2[index_parent]) # allReports, pagesToBeExtracted

    table = tables[tableOrder2[index_parent]].apply(lambda x: x.str.strip() if x.dtype == "object" else x) # tableOrder

    table_columns = list(table.columns)
    table_values = table.values.tolist() # converting an n-dimensional array to a list of nested strings

    search_words = ['Unnamed', 'Item', 'nan', 'total']
    digits = r"^\d+" # checks the string to see if it starts with a digit

    filtered_list_columns = [s for s in table_columns if not any(re.search(re.escape(word), s, re.IGNORECASE) for word in search_words)]

    filtered_list_values_comp = [[value for value in nested_list if re.search(digits, str(value))] for nested_list in
                                 table_values]

    filtered_list_values_clean_comp = remove_duplicate_lists([[value for index, value in enumerate(nested_list) if index <= 2] for nested_list in
                                       filtered_list_values_comp])

    filtered_list_values_extra_clean_comp = remove_empty_lists(filtered_list_values_clean_comp)

    filtered_list_values_extra_clean_2_comp = remove_problem_lists(filtered_list_values_extra_clean_comp)

    for index_child, value_child in enumerate(business_types):

        new_row = {'Year': yearReports2[index_parent],
                   'Business_Type': business_types[index_child],
                   'Large': int("".join(filtered_list_values_extra_clean_2_comp[index_child][0].split())),
                   'Medium': int("".join(filtered_list_values_extra_clean_2_comp[index_child][1].split())),
                   'Small and Micro': int("".join(filtered_list_values_extra_clean_2_comp[index_child][2].split()))
                   }

        income_by_business_size_df_2012.loc[len(income_by_business_size_df_2012)] = new_row


    result_append_2 = pd.concat([result_append_2, income_by_business_size_df_2012], ignore_index=True)

    print('-----------------------------------------')
    print(f'Done Processing {fromReports[index_parent]}, with parameters page:{pagesToBeExtracted2[index_parent]}, tableOrder:{tableOrder2[index_parent]} and year:{yearReports2[index_parent]}')
## -------------------------------------2015, 2018 and 2022-----------------------------------------------##

## ---------------------------------Cleaning 2007 dataframe-----------------------------------------------##
result_append['Small and Micro'] = result_append['Small'] + result_append['Micro']
result_append_clean = result_append[['Year','Business_Type','Small and Micro', 'Medium', 'Large']]
## ---------------------------------Cleaning 2007 dataframe-----------------------------------------------##

## ---------------------------------Dropping Duplicates-----------------------------------------------##
result_append_2_clean = result_append_2.drop_duplicates()
## ---------------------------------Dropping Duplicates-----------------------------------------------##

result_append_complete = pd.concat([result_append_clean, result_append_2_clean], ignore_index=True)

## ---------------------------------Dealing with missing values-----------------------------------------------##

# Using the imputation method to replace the missing values for 2009, replacing missing values with the
# median for the business type and size

##-------------------------------- Updating Restuarants for 2009 -----------------------------------------------##
result_append_complete.loc[
    (result_append_complete['Business_Type'] == 'Restaurants and coffee shops') & (result_append_complete['Small and Micro'] == 0)
    & (result_append_complete['Year'] == 2009), 'Small and Micro'
] = int(result_append_complete.query('Business_Type == "Restaurants and coffee shops"')['Small and Micro'].median())

result_append_complete.loc[
    (result_append_complete['Business_Type'] == 'Restaurants and coffee shops') & (result_append_complete['Medium'] == 0)
    & (result_append_complete['Year'] == 2009), 'Medium'
] = int(result_append_complete.query('Business_Type == "Restaurants and coffee shops"')['Medium'].median())

result_append_complete.loc[
    (result_append_complete['Business_Type'] == 'Restaurants and coffee shops') & (result_append_complete['Large'] == 0)
    & (result_append_complete['Year'] == 2009), 'Large'
] = int(result_append_complete.query('Business_Type == "Restaurants and coffee shops"')['Large'].median())
##-------------------------------- Updating Restuarants for 2009 -----------------------------------------------##

##-------------------------------- Updating Takeaways for 2009 -----------------------------------------------##
result_append_complete.loc[
    (result_append_complete['Business_Type'] == 'Takeaway/fast-food outlets') & (result_append_complete['Small and Micro'] == 0)
    & (result_append_complete['Year'] == 2009), 'Small and Micro'
] = int(result_append_complete.query('Business_Type == "Takeaway/fast-food outlets"')['Small and Micro'].median())

result_append_complete.loc[
    (result_append_complete['Business_Type'] == 'Takeaway/fast-food outlets') & (result_append_complete['Medium'] == 0)
    & (result_append_complete['Year'] == 2009), 'Medium'
] = int(result_append_complete.query('Business_Type == "Takeaway/fast-food outlets"')['Medium'].median())

result_append_complete.loc[
    (result_append_complete['Business_Type'] == 'Takeaway/fast-food outlets') & (result_append_complete['Large'] == 0)
    & (result_append_complete['Year'] == 2009), 'Large'
] = int(result_append_complete.query('Business_Type == "Takeaway/fast-food outlets"')['Large'].median())
##-------------------------------- Updating Takeaways for 2009 -----------------------------------------------##

##-------------------------------- Updating Caterers for 2009 -----------------------------------------------##
result_append_complete.loc[
    (result_append_complete['Business_Type'] == 'Caterers and other catering services') & (result_append_complete['Small and Micro'] == 0)
    & (result_append_complete['Year'] == 2009), 'Small and Micro'
] = int(result_append_complete.query('Business_Type == "Caterers and other catering services"')['Small and Micro'].median())

result_append_complete.loc[
    (result_append_complete['Business_Type'] == 'Caterers and other catering services') & (result_append_complete['Medium'] == 0)
    & (result_append_complete['Year'] == 2009), 'Medium'
] = int(result_append_complete.query('Business_Type == "Caterers and other catering services"')['Medium'].median())

result_append_complete.loc[
    (result_append_complete['Business_Type'] == 'Caterers and other catering services') & (result_append_complete['Large'] == 0)
    & (result_append_complete['Year'] == 2009), 'Large'
] = int(result_append_complete.query('Business_Type == "Caterers and other catering services"')['Large'].median())
##-------------------------------- Updating Caterers for 2009 -----------------------------------------------##


print(result_append_complete[['Business_Type', 'Small and Micro', 'Medium', 'Large']])

result_append_complete.to_csv('Income_complete.csv',header=True, index=False)

## ---------------------------------Dealing with missing values-----------------------------------------------##


