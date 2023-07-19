import pathlib, pickle, requests, time, pandas as pd

# Q: What and how many different keyords were written about Tesla in the Technology section from January 1st, 2020 till current?


# Creating the API Key
API_KEY = "byYqRTtU1q9wpnK1Gd1bIkbTqWb8eaWm"

# New York Times Link
url = 'https://api.nytimes.com/svc/search/v2/articlesearch.json'

# Choosing the parameters for the call
parameters = {'q': 'Tesla', 'api-key': API_KEY, "fq": "document_type: (article) AND section_name:(Technology)",
              "begin_date": "20200101",
              "end_date": "20230731", "page": 0}



def api_pull(url_link, parameters1):
    """
     function to run a get request from the New York Times API to extract information about Tesla

     :argument:
        url (str): API endpoint
        parameters (dict): API params
    :return:
        dict: content
    """
    # Getting the requests
    response = requests.get(url_link, params=parameters1)

    # Storing results in a variable named content
    content = response.json()

    return content


# Getting the total results of the query and then calculating important values such as hit number and page count
results = api_pull(url, parameters)

number_of_hits = results["response"]["meta"]["hits"]
print(f"Number of Hits: {number_of_hits}")
page_count = number_of_hits // 10
print(f"Page Count: {page_count}\n")

# Creating the keyword files
for i in range(page_count):
    try:
        NYT_tesla = pathlib.Path.cwd() / "NYT_Tesla_keywords"
        NYT_tesla.mkdir(exist_ok=True)
        pg_num = i
        file_name = f"kews{pg_num}"
        parameters["page"] = i
        results = api_pull(url, parameters)
        for documents in results["response"]["docs"]:
            kews = []
            for keys in documents["keywords"]:
                kews.append(keys["value"])
                with open(f"NYT_Tesla_keywords/{file_name}", 'wb') as p_file:
                    pickle.dump(kews, p_file)
            time.sleep(7)
        print(f"Page Number ({pg_num}) completed.")
    except:
        print("Something unknown occurred.")

# Creating a list of all the words
list_of_all_words = []

# Setting the path and making a new directory for the keywords
cwd = pathlib.Path.cwd()
nyt_tesla_dir = cwd/"NYT_Tesla_keywords"

# Appending the words in the file into a large list to then utilize in a DataFrame
for i in nyt_tesla_dir.iterdir():
    with open(i, 'rb') as keyword_file:
        df = pd.read_pickle(keyword_file) # temporary variable to store the list value
        for _ in df:
            list_of_all_words.append(_)

print(list_of_all_words)

# Converting list into a Pandas Dataframe to make it easier to use certain calculation methods
# Write to a CSV using Pandas method
calc_dataframe = pd.DataFrame(list_of_all_words)

calc_dataframe = calc_dataframe.rename(columns={0: 'Keyword'})
print(calc_dataframe)

final_results = pd.DataFrame(calc_dataframe["Keyword"].value_counts())

print(final_results)


# This converts into a CSV file which is available on the folder I created previously with the other binary files or pickle files
final_results.to_csv("/Users/rishpednekar/PycharmProjects/allprojects/2023_summer/NYT_Tesla_keywords/final_results_tesla.csv")