overview:

search_script.py
performs searches using designated sets of search terms on elicit.org. Organizes by pre-defined subtopics. Generates subfolders in 'results' that contain the csv files corresponding to each term within the subtopic.

search_compiler.py
parses through the search result csv files and compiles dataframes for each subtopic, as well as a master dataframe containing all results. Creates dedupe'd versions of these as well. optional running of keyword extraction if openai API is detected.
