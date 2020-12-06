import io
import os
import inspect
import re

import docx2txt
import pandas as pd

import spacy
from pyresparser import ResumeParser, utils, constants as cs
from spacy.matcher import Matcher

EXPERIENCE_KEYWORDS = [
        "professional background",
        "career progression",
        "work history",
        "past employment",
        "experiences",
        "career overview",  # ?
        "work summary",
        "employment",
    ]

EDUCATION_KEYWORDS = [
    "qualifications",
    "academic qualifications",
    "qualification",
    "educational",
]

cs.RESUME_SECTIONS_GRAD.extend(EXPERIENCE_KEYWORDS)
cs.RESUME_SECTIONS_GRAD.extend(EDUCATION_KEYWORDS)


class CustomResumeParser(ResumeParser):
    def __init__(
            self,
            resume,
            skills_file=None,
            custom_regex=None
    ):
        nlp = spacy.load('en_core_web_sm')
        custom_nlp = spacy.load(os.path.dirname(os.path.abspath(inspect.getfile(ResumeParser))))
        self.__skills_file = skills_file
        self.__custom_regex = custom_regex
        self.__matcher = Matcher(nlp.vocab)
        self.__details = {
            'skills': None,
            'education': None,
            'college_name': None,
            'degree': None,
            'designation': None,
            'experience': None,
            'company_names': None,
            'total_experience': None,
            'education_section': None,
            'experience_section': None,
            'resume': resume
        }
        self.__resume = resume
        if not isinstance(self.__resume, io.BytesIO):
            ext = os.path.splitext(self.__resume)[1].split('.')[1]
        else:
            ext = self.__resume.name.split('.')[1]
        self.__text_raw = extract_text(self.__resume, '.' + ext)
        self.__text = ' '.join(self.__text_raw.split())
        self.__nlp = nlp(self.__text)
        self.__custom_nlp = custom_nlp(self.__text_raw)
        self.__noun_chunks = list(self.__nlp.noun_chunks)
        self.__get_basic_details()

    def get_extracted_data(self):
        return self.__details
        # fields_to_return = ['skills', 'education_section', 'experience_section']
        # if os.environ.get('INCLUDE_RESUME_PATHS', None):
        #     fields_to_return.append('resume')
        # return dict((key, self.__details[key]) for key in fields_to_return)

    def __get_basic_details(self):
        cust_ent = utils.extract_entities_wih_custom_model(
            self.__custom_nlp
        )
        skills = extract_skills(
            self.__nlp,
            self.__noun_chunks,
            self.__skills_file
        )
        edu = extract_education_with_gpa(
                      [sent.string.strip() for sent in self.__nlp.sents]
              )

        entities = extract_entity_sections_grad(self.__text_raw)

        for keyword in [*EDUCATION_KEYWORDS, 'education']:
            if keyword in entities and entities[keyword]:
                self.__details['education_section'] = entities[keyword]

        # if 'education' in entities:
        #     gpa = extract_gpa(entities['education'])

        # extract skills
        self.__details['skills'] = skills

        # Tuple of Degree,Year and Gpa
        self.__details['education'] = edu

        # extract college name
        try:
            self.__details['college_name'] = entities['College Name']
        except KeyError:
            pass

        # extract education Degree
        try:
            self.__details['degree'] = cust_ent['Degree']
        except KeyError:
            pass

        # extract designation
        try:
            self.__details['designation'] = cust_ent['Designation']
        except KeyError:
            pass

        # extract company names
        try:
            self.__details['company_names'] = cust_ent['Companies worked at']
        except KeyError:
            pass

        try:
            for keyword in [*EXPERIENCE_KEYWORDS, 'experience', 'professional experience']:
                if keyword in entities and entities[keyword]:
                    if self.__details['experience'] is None:
                        self.__details['experience'] = entities[keyword]
                        self.__details['experience_section'] = entities[keyword]
                    else:
                        self.__details['experience'].extend(entities[keyword])
                        self.__details['experience_section'].extend(entities[keyword])
            try:
                exp = round(
                    utils.get_total_experience(self.__details['experience']) / 12,
                    2
                )
                self.__details['total_experience'] = exp
            except (KeyError, TypeError):
                self.__details['total_experience'] = 0
        except KeyError:
            self.__details['total_experience'] = 0
        return


def extract_text(file_path, extension):
    '''
    Wrapper function to detect the file extension and call text
    extraction function accordingly

    :param file_path: path of file of which text is to be extracted
    :param extension: extension of file `file_name`
    '''
    text = ''
    if extension == '.pdf':
        for page in utils.extract_text_from_pdf(file_path):
            text += ' ' + page
    elif extension == '.docx':
        text = extract_text_from_docx(file_path)
    elif extension == '.doc':
        text = utils.extract_text_from_doc(file_path)
    return text


def extract_text_from_docx(doc_path):
    '''
    Helper function to extract plain text from .docx files

    :param doc_path: path to .docx file to be extracted
    :return: string of extracted text
    '''
    try:
        text = docx2txt.process(doc_path)
        return text
    except KeyError:
        return ' '


def extract_education_with_gpa(nlp_text):
    '''
        Helper function to extract education from spacy nlp text

        :param nlp_text: object of `spacy.tokens.doc.Doc`
        :return: tuple of education degree and year if year if found
                 else only returns education degree
        '''
    edu = {}
    # Extract education degree
    try:
        for index, text in enumerate(nlp_text):
            for tex in text.split():
                tex = re.sub(r'[?|$|.|!|,]', r'', tex)
                if tex.upper() in cs.EDUCATION and tex not in cs.STOPWORDS:
                    edu[tex] = text + nlp_text[index + 1]
    except IndexError:
        pass

    # Extract year and gpa if available
    education = []
    gpa_regex = r'(\d{1})\.(\d{1,2})'
    for key in edu.keys():
        year = re.search(re.compile(cs.YEAR), edu[key])
        gpa = re.search(re.compile(gpa_regex), edu[key])
        edu_tuple = (key,)
        if year:
            edu_tuple = edu_tuple + (''.join(year.group(0)),)
        if gpa:
            edu_tuple = edu_tuple + (gpa.group(),)

        if gpa or year:
            education.append(edu_tuple)
        else:
            education.append(key)
    return education


def extract_skills(nlp_text, noun_chunks, skills_file=None):
    """
    Helper function to extract skills from spacy nlp text

    :param nlp_text: object of `spacy.tokens.doc.Doc`
    :param noun_chunks: noun chunks extracted from nlp text
    :param skills_file: custom file with a collection of skills
    :return: list of skills extracted
    """
    tokens = [token.text for token in nlp_text if not token.is_stop]
    if not skills_file:
        data = pd.read_csv(
            os.path.join(os.path.dirname(inspect.getfile(ResumeParser)), 'skills.csv')
        )
        skills = list(data.columns.values)
    else:
        data = pd.read_csv(skills_file)
        skills = [str(x).lower() for x in data['technical skills'].tolist()]
    skillset = []
    # check for one-grams
    for token in tokens:
        if token.lower() in skills:
            skillset.append(token)

    # check for bi-grams and tri-grams
    for token in noun_chunks:
        token = token.text.strip()
        if token.lower() in skills:
            skillset.append(token)
    return [i.capitalize() for i in set([i.lower() for i in list(dict.fromkeys(skillset))])]


def extract_entity_sections_grad(text):
    '''
    Helper function to extract all the raw text from sections of
    resume specifically for graduates and undergraduates

    :param text: Raw text of resume
    :return: dictionary of entities
    '''
    text_split = [i.strip() for i in text.split('\n')]
    # sections_in_resume = [i for i in text_split if i.lower() in sections]
    entities = {}
    key = False
    edu_pattern = re.compile(
        r"(?P<before_colon>Education):(?P<after_colon>.+)",
        re.IGNORECASE
    )
    for phrase in text_split:
        p_key = ''
        if len(phrase.split()) <= 3:
            p_key = phrase.replace(':', '').lower()
            if p_key not in cs.RESUME_SECTIONS_GRAD:
                p_key = set(p_key.split()) & set(cs.RESUME_SECTIONS_GRAD)
        # else:
        #     p_key = set(word.replace(':', '') for word in phrase.lower().split()) & set(cs.RESUME_SECTIONS_GRAD)
                try:
                    p_key = list(p_key)[0]
                except IndexError:
                    pass
        elif re.search('education', phrase, flags=re.IGNORECASE):
            edu_match = re.search(edu_pattern, phrase)
            if edu_match:
                key = 'education'
                after = edu_match['after_colon'].strip()
                entities['education'] = [after]
                continue
        if p_key in cs.RESUME_SECTIONS_GRAD:
            if p_key not in entities:
                entities[p_key] = []
            key = p_key
        elif key and phrase.strip():
            entities[key].append(phrase)
    return entities
