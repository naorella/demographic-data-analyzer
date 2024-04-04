#Code Author: Nelson Orellana
#demogrpahic_data_analyzer
#Data from freecodecamp.org
import pandas as pd


#calculate_demographic_data(): produces statistical data using pandas formating,
#prints the data and returns it as a dictionary. All data printed and returned
#will be rounded to the nearest tenths
#calculate_demographic_data(): None -> 
#Dict (Pandas Series, Pandas Dataframes, Num)
#Requires: that the data be properly formated in a csv file
def calculate_demographic_data(print_data=True):
    # Read data from file
    demo_df = pd.read_csv("adult.data.csv")

    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    #select the race subset of the data, group it and apply count()
    race_count = demo_df["race"].value_counts()

    # What is the average age of men?
    #seperate into sex, and calculate mean on age
    male_demo = demo_df[demo_df["sex"] == "Male"]
    average_age_men = male_demo["age"].mean().round(1)

    # What is the percentage of people who have a Bachelor's degree?
    #Count each educations count
    edu_df = demo_df['education'].value_counts()
    #count the total number of entries in education
    total_count = edu_df.sum()
    #seperate bachelors from the value count
    bach_count = edu_df["Bachelors"]
    #divide bachelors count by the total number of entries and multiply by 100
    #for the percentage of bachelors
    percentage_bachelors = (bach_count/total_count*100).round(1)

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # What percentage of people without advanced education make more than 50K?

    # with and without `Bachelors`, `Masters`, or `Doctorate`
    #use sql like query to select multiple columns, education, and salary, where
    #salary is >50K
    #A search string that we will use to find the education types we want, and
    #then the remainder with the inverse
    search_string = '{0}((education == "Bachelors") or (education == "Masters") or (education == "Doctorate"))'
    higher_education = demo_df[['education', 'salary']].query(search_string.format(""))
    #create the inverse of the above, that way we dont need to write out every
    #other education type besides the ones we have already done
    lower_education = demo_df[['education', 'salary']].query(search_string.format("not"))

    #find how many people with higher education make >50k by taking value counts
    #of all salaries and extracting ">50k"
    over_50k_high = higher_education['salary'].value_counts()[">50K"]
    #and the total number of people with higher education
    higher_total = higher_education['salary'].count()

    #find total of lower education with >50k
    over_50k_low = lower_education['salary'].value_counts()[">50K"]
    #and total with lower education
    lower_total = lower_education['salary'].count()
    

    # percentage with salary >50K
    higher_education_rich = (over_50k_high/higher_total*100).round(1)
    lower_education_rich = (over_50k_low/lower_total*100).round(1)

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = demo_df['hours-per-week'].min()

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    #we call upon min_work_hours within the query with the @ symbol
    #and we use [salary] just to get a single column so we can count and retun
    #an int, not a dataframe
    num_min_workers = demo_df.query('(`hours-per-week` == @min_work_hours)')['salary'].count()
    num_min_rich = demo_df.query('(salary == ">50K") and (`hours-per-week` == @min_work_hours)')['salary'].count()

    rich_percentage = (num_min_rich/num_min_workers*100).round(1)

    # What country has the highest percentage of people that earn >50K?
    #find the total pop from each country
    country_pop = demo_df['native-country'].value_counts()
    #then find the total from each country that makes more than 50k
    country_50k = demo_df[demo_df['salary'] == ">50K"]['native-country'].value_counts()
    #combine the two dataframes by dividing on to the other, since keys match
    #pandas will take care of it and create a series
    percent_country_50k = (country_50k/country_pop*100).round(1)

    #idxmax returns row Id of max number found
    highest_earning_country = percent_country_50k.idxmax()
    highest_earning_country_percentage = percent_country_50k.max()

    # Identify the most popular occupation for those who earn >50K in India.
    over_50k_India = demo_df.query('(`native-country` == "India") and (salary == ">50K")')
    #and then count the amount of jobs that applies to
    india_jobs = over_50k_India["occupation"].value_counts()
    #and return the job title that has the most hits
    top_IN_occupation = india_jobs.idxmax()

    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count) 
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }
