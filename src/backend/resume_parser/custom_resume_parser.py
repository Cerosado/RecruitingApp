import io
import os
import inspect
import re

import docx2txt
import pandas as pd

import spacy
from pyresparser import ResumeParser, utils, constants as cs
from spacy.matcher import Matcher


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
            'total_experience': None,   # todo: remove??
            'education_section': None,
            'experience_section': None
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
        # return self.__details
        return dict((key, self.__details[key]) for key in ['skills', 'education_section', 'experience_section'])

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
        # TODO: Extract concentration, gpa, work experiences from entities
        entities = extract_entity_sections_grad(self.__text_raw)

        self.__details['education_section'] = entities.get('education', None)
        if 'experience' in entities:
            self.__details['experience_section'] = entities.get('experience', None)
        elif 'professional experience' in entities:
            self.__details['experience_section'] = entities.get('professional experience', None)

        # if 'education' in entities:
        #     gpa = extract_gpa(entities['education'])

        # extract skills
        self.__details['skills'] = skills

        # TODO: Currently extracting degree and year, not concentration nor university
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
            self.__details['experience'] = entities['experience']
            try:
                exp = round(
                    utils.get_total_experience(entities['experience']) / 12,
                    2
                )
                self.__details['total_experience'] = exp
            except KeyError:
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
    for phrase in text_split:
        if len(phrase) == 1:
            p_key = phrase.replace(':', '')
        else:
            p_key = set(word.replace(':', '') for word in phrase.lower().split()) & set(cs.RESUME_SECTIONS_GRAD)
        try:
            p_key = list(p_key)[0]
        except IndexError:
            pass
        if p_key in cs.RESUME_SECTIONS_GRAD:
            entities[p_key] = []
            key = p_key
        elif key and phrase.strip():
            entities[key].append(phrase)

    # entity_key = False
    # for entity in entities.keys():
    #     sub_entities = {}
    #     for entry in entities[entity]:
    #         if u'\u2022' not in entry:
    #             sub_entities[entry] = []
    #             entity_key = entry
    #         elif entity_key:
    #             sub_entities[entity_key].append(entry)
    #     entities[entity] = sub_entities

    # pprint.pprint(entities)

    # make entities that are not found None
    # for entity in cs.RESUME_SECTIONS:
    #     if entity not in entities.keys():
    #         entities[entity] = None
    return entities
