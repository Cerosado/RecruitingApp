import os
import csv

from joblib._multiprocessing_helpers import mp
from joblib import dump, load
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
import pandas
from sklearn.model_selection import train_test_split

from src.backend.resume_parser.custom_resume_parser import CustomResumeParser
from pyresparser.command_line import print_cyan
from pprint import pprint as pp


def print_parsed_resume(file, skills_file=None):
    data = CustomResumeParser(file, skills_file=skills_file).get_extracted_data()
    print(data)


def parse_resume_directory(directory, custom_regex=None):
    results = []
    skills_file = 'skills_dataset.csv'
    if os.path.exists(directory):
        pool = mp.Pool(mp.cpu_count())

        resumes = []
        for root, dirs, filenames in os.walk(directory):
            for filename in filenames:
                if not filename.startswith('~$'):
                    file = os.path.join(root, filename)
                    resumes.append([file, skills_file, custom_regex])
        # results = map(resume_result_wrapper, resumes)
        results = pool.starmap(resume_result_wrapper, resumes)
        pool.close()
        pool.join()
    return list(results)


def resume_result_wrapper(resume_file, skills_file, custom_regex):
    print_cyan('Extracting data from: {}'.format(resume_file))
    return CustomResumeParser(resume_file, skills_file, custom_regex).get_extracted_data()


def parse_dataset_to_csv(csv_file, resumes_path):
    """
    Function parses resumes from a directory and writes the parsed information in a csv file
    :return: None
    """
    with open(csv_file, mode='w', encoding='utf-8') as parse_results_file:
        field_names = ['skills', 'education', 'college_name', 'degree',
                       'designation', 'experience', 'company_names',
                       'total_experience', 'education_section', 'experience_section', 'label', 'resume']
        # field_names = ['skills', 'education_section', 'experience_section', 'label']
        # if os.environ.get('INCLUDE_RESUME_PATHS', None):
        #     field_names.append('resume')
        parse_writer = csv.DictWriter(parse_results_file, fieldnames=field_names)
        parse_writer.writeheader()
        education_important = bool('no_edu' not in csv_file)
        flags = ['unfit']
        if education_important:
            flags.append('no_education')
        # for resume_type in (resumes_path, resumes_path + '/unfit'):
        results = parse_resume_directory('resumes/%s' % (resumes_path,))
        for parse_result in results:
            parse_result['label'] = 0 if any(flag in parse_result['resume'] for flag in flags) else 1
            parse_writer.writerow(parse_result)


def parse_directory_to_csv(directory, csv_file):
    """

    :param directory: Name of directory containing resumes to parse
    :param csv_file: Name of file where parsed resumes will be stored in csv format
    :return: None
    """
    with open(csv_file, mode='w') as parse_csv:
        # field_names = ['skills', 'education', 'college_name', 'degree',
        #                'designation', 'experience', 'company_names',
        #                'total_experience', 'label']
        field_names = ['skills', 'education_section', 'experience_section', 'label']
        if os.environ.get('INCLUDE_RESUME_PATHS', None):
            field_names.append('resume')
        parse_writer = csv.DictWriter(parse_csv, fieldnames=field_names)
        parse_writer.writeheader()
        results = parse_resume_directory(directory)
        for parse_result in results:
            parse_writer.writerow(parse_result)


def test_model():
    # Retrieve dataset from csv file
    dataset = pandas.read_csv("parsed_results.csv", encoding='cp1252')
    data = dataset.iloc[:, 0]  # Retrieve skills column
    target = dataset['label']  # Retrieve label column

    # Vectorizer used to transform text data to a format that the model can use
    count_vect = CountVectorizer()
    vectorized_data = count_vect.fit_transform(data)
    dump(count_vect, 'vectorizer.joblib')
    dump(vectorized_data, 'vectorized_data.joblib')

    # Parse other resumes to use model.predict
    parse_directory_to_csv('resumes/additional',
                           csv_file='my_resume.csv')
    my_resume = pandas.read_csv("my_resume.csv", encoding='utf-8')
    my_resume_data = my_resume.iloc[:, 0]
    my_resume_vectorized = count_vect.transform(my_resume_data)

    # Split data for training and testing, train and then get accuracy score
    x_train, x_test, y_train, y_test = train_test_split(vectorized_data, target, stratify=target, random_state=5)
    # ranking_model = LogisticRegression(C=1).fit(x_train, y_train)
    # dump(ranking_model, 'ranking_model.joblib')
    ranking_model = load('ranking_model.joblib')
    print("Test set score: {:3f}".format(ranking_model.score(x_test, y_test)))
    print(ranking_model.predict(my_resume_vectorized))


if __name__ == '__main__':
    # print_parsed_resume('C:/Users/Eduardo Perez/Documents/Resume/RESUME_EduardoAPerezVega2020sinAcentos.pdf')
    # print_parsed_resume('resume_parser/resumes/Experienced/OmkarResume.pdf',
    #                     skills_file='resume_parser/skills_dataset.csv')
    # pp(parse_resume_directory('resume_parser/resumes/Experienced', skills_file='resume_parser/skills_dataset.csv'))

    # Parse training set resumes
    parse_dataset_to_csv(csv_file='dataset_csvs/management_no_edu.csv',
                         resumes_path='datasets/management')

    # parse_dict = CustomResumeParser(
    #     resume='resumes/kaggle_dataset/Resume - PM Agile-Scrum.docx',
    #     skills_file='skills_dataset.csv'
    # ).get_extracted_data()
    # print(parse_dict)

    # test_model()

    # Convert skills txt file to csv
    # skills = pandas.read_csv("C:/Users/Eduardo Perez/Downloads/linkedin_skills.txt",
    #                          names=('technical skills',), sep='\n')
    # skills.to_csv('skills_dataset.csv', index=None)
