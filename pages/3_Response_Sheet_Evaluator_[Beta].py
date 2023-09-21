import streamlit as st
#from streamlit_extras.app_logo import add_logo
import sqlite3
from io import BytesIO
from PyPDF2 import PdfReader
import pandas as pd



st.set_page_config(page_title="Smartprep",page_icon="https://i.imgur.com/S9k9LNT.png")


def add_logo():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url(https://i.imgur.com/n1v7QfM.png);
                background-repeat: no-repeat;
                padding-top: 120px;
                background-position: 20px 20px;

            }
            [data-testid="stSidebarNav"]::before {
                margin-left: 20px;
                margin-top: 20px;
                font-size: 30px;
                position: relative;
                top: 100px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

def main():

    st.title("Response Sheet Evaluator")
    # add_logo("https://i.imgur.com/W0NrmI1.png")
    add_logo()


    st.markdown(""" You can check your score with respect to your answer key and response sheet here. If you are unaware of **how to get your Response sheet**, please follow the following steps -""")
    st.markdown("""  - Go to **IITM Dashboard** and select **Documents for Download**.""")
    st.markdown("""- Search for the paper which you have attempted in **document type: ANSWER TRANSCRIPT**""")
    st.markdown("""- Download the answer transcript and upload here""")
    st.write("\n")
    st.markdown(""" In the same manner, to **get the answer key** of exam for which you want to check your score, please follow these steps -
    - Go to IITM Dashboard and select **my current courses**
    - Select the course for which you want to check score
    - Select modules in course page and go to bottom most dropdown where you can find **Answer Key for Exam** dropdown
    - select the quiz for which you want to check (quiz1/quiz2/endterm) and then **go to the drive link provided**
    - download the paper in drive link for which you have attempted **(to know for which set out of all papers in drive you have attempted in exam, open your response sheet and check QP set and come back to drive and download the paper which matches the QP set)**""")



    declarers = 1

    if declarers == 1:
        file_name = ''
        diction = {}
        course_info = {}
        Comprehension = {}
        Question = {}
        score = total = 0
        user_session = {}
        declarers = 0
        text = ''

    paper = st.file_uploader("Upload your attempted paper answer key", type=['pdf'])
    response = st.file_uploader("Upload your response sheet", type=['pdf'])

    if paper is not None and response is not None:

        reader = PdfReader(paper)
        # Extract text from each page
        for page_number in range(len(reader.pages)):
            page = reader.pages[page_number]
            extracted_text = page.extract_text()
            text = text + extracted_text

        content = []
        for page in reader.pages:
            content.append(page.extract_text().split('\n'))

        # Courses information

        subjects = []
        start_taking_data = False
        course_info
        course_info = {}
        c = 1
        for i in content:
            for j in i:
                if 'Section Id :' in j and 'Sub-Section Id' not in j:
                    # print(j)
                    start_taking_data = True
                    c = 0
                if 'Question Shuffling Allowed :' in j:
                    start_taking_data = False
                    c = 1
                if c == 1:
                    subject = j

                if start_taking_data:
                    if subject not in course_info.keys():
                        course_info[subject] = {}
                    if ' : ' in j:
                        t = j.split(' : ')
                        course_info[subject][t[0]] = t[1]
                    elif ' :' in j:
                        t = j.split(' :')
                        course_info[subject][t[0]] = t[1]
                    elif ': ' in j:
                        t = j.split(': ')
                        course_info[subject][t[0]] = t[1]
                    elif ':' in j:
                        t = j.split(':')
                        course_info[subject][t[0]] = t[1]

            if subject not in subjects and c == 0:
                subjects.append(subject)

        for i in course_info:
            course_info[i]['Course Name'] = i

        # Taking Number of Questions for Each Subject Because in PDF number of Questions info is Wrong
        Qcount = 0
        c = m = 0
        endpoint = []
        for i in content:
            for j in i:
                if 'Section Id :' in j and 'Sub-Section Id' not in j:
                    c += 1
                if m == c:
                    course = j
                else:
                    m = c
                    subject = course

                if 'Question Number :' in j or 'Question Number:' in j:
                    Qcount += 1
                    if 'Question Starts at' not in course_info[subject].keys():
                        course_info[subject]['Question Starts at'] = Qcount
                        course_info[subject]['Question Ends at'] = Qcount
                    else:
                        course_info[subject]['Question Ends at'] = Qcount

        for i in course_info.keys():
            course_info[i]['Number of Questions'] = course_info[i]['Question Ends at'] - course_info[i][
                'Question Starts at'] + 1
            endpoint.append(course_info[i]['Question Ends at'])

        # Let us take the Questions Data now
        ques_no = 0
        Question = {}
        Comprehension = {}
        read_comp_data = False
        read_ques_data = False
        read_question = False
        first_occurence = True
        read_opt_data = read_sa_data = False
        opt_num = pre_opt = 0
        for i in content:
            for j in i:
                if 'Question Number :' in j:
                    read_ques_data = True
                    ques_no += 1
                    opt_num = 0

                if read_ques_data:
                    if ques_no not in Question.keys():
                        Question[ques_no] = {}
                        Question[ques_no]['Data'] = ''
                        Question[ques_no]['Answer'] = []
                        Question[ques_no]['Question'] = ''
                        Question[ques_no]['Question Number'] = ques_no
                        Question[ques_no]['Options'] = [{}]
                    Question[ques_no]['Data'] += j + '\n'

                    if 'Question Type :' in j:
                        check = False
                        temp = j.split(' : ')
                        for i in temp:
                            if check:
                                Question[ques_no]['Question Type'] = i.split(' ')[0]
                                break
                            if 'Question Type' in i:
                                check = True

                if ('Options :' in j or 'Response Type :' in j) and 'Selectable Options :' not in j:
                    read_ques_data = False
                    read_question = False

                if 'Sub questions' in j:
                    read_comp_data = False

                if 'Correct Marks :' in j:
                    Question[ques_no]['Marks'] = float((j.split(' : ')[1]).split(' ')[0])

                if 'Question Id :' in j or 'Sub-Section Number :' in j:
                    read_opt_data = False
                    c = 0

                if ques_no in endpoint and read_opt_data:
                    for i in course_info.keys():
                        if course_info[i]['Question Starts at'] == ques_no + 1:
                            clean = i
                    if clean in j:
                        read_opt_data = False

                if read_comp_data:
                    Comprehension[ques_no + 1]['Question'] += j

                if read_sa_data and '\xa0' not in j:
                    Question[ques_no]['Answer'] = j
                    read_sa_data = False

                if read_opt_data and '\xa0' not in j:
                    if '640653' in j:
                        Question[ques_no]['Options'].append({})
                        Question[ques_no]['Options'][opt_num]['ID'] = j.split('.')[0]
                        Question[ques_no]['Options'][opt_num]['text'] = ''
                        Question[ques_no]['Options'][opt_num]['Number'] = opt_num + 1
                        pre_opt = opt_num
                        opt_num += 1
                    elif 'text' not in Question[ques_no]['Options'][pre_opt].keys():
                        Question[ques_no]['Options'][pre_opt]['text'] = j
                    else:
                        Question[ques_no]['Options'][pre_opt]['text'] += j

                if 'Options :' in j and 'Selectable Options :' not in j:
                    read_opt_data = True

                if read_question:
                    if 'Question' not in Question[ques_no].keys():
                        Question[ques_no]['Question'] = ''
                    Question[ques_no]['Question'] += j + '\n'

                if 'Question Label :' in j:
                    if 'Comprehension' not in j:
                        read_question = True
                    else:
                        read_comp_data = True

                if 'Question Numbers :' in j:
                    Comprehension[ques_no + 1] = {}
                    Comprehension[ques_no + 1]['Question'] = ''
                    Comprehension[ques_no + 1]['min'] = int(
                        j.split(' : ')[1].split('(')[1].split(')')[0].split(' to ')[0])
                    Comprehension[ques_no + 1]['max'] = int(
                        j.split(' : ')[1].split('(')[1].split(')')[0].split(' to ')[1])

                if 'Possible Answers :' in j:
                    read_sa_data = True

        import pdfminer
        from pdfminer.high_level import extract_pages
        from pdfminer.layout import LTTextContainer, LTChar
        import sys

        correctID = []
        wrongID = []
        correct = wrong = cross_check = False
        for page_layout in extract_pages(paper):
            for element in page_layout:
                # print(element)
                if isinstance(element, LTTextContainer):
                    fontinfo = set()
                    for text_line in element:
                        if isinstance(text_line, pdfminer.layout.LTTextLineHorizontal):
                            correct = False
                            wrong = False
                            for character in text_line:
                                if isinstance(character, LTChar):
                                    if character.graphicstate.ncolor == (0, 0.50196, 0):
                                        correct = True
                                        break
                                    elif character.graphicstate.ncolor == (1, 0, 0):
                                        wrong = True
                                        break
                    if correct and '640653' in element.get_text():
                        correctID.append(element.get_text().split('.')[0])

                    elif wrong and '640653' in element.get_text():
                        wrongID.append(element.get_text().split('.')[0])

        for i in Question.values():
            if len(i['Options'][-1]) == 0:
                i['Options'].pop()

        for i in Question.values():
            for j in range(len(i['Options'])):
                if i['Options'][j]['ID'] in correctID:
                    i['Options'][j]['Answer'] = True
                elif i['Options'][j]['ID'] in wrongID:
                    i['Options'][j]['Answer'] = False

        for i in Question:
            for sub in course_info:
                if i >= course_info[sub]['Question Starts at'] and i <= course_info[sub]['Question Ends at']:
                    Question[i]['Subject'] = sub
                    break
            for j in Question[i]['Options']:
                if j['Answer']:
                    Question[i]['Answer'].append(str(j['Number']))

        for i in Question:
            for sub in course_info:
                if Question[i]['Subject'] == sub:
                    if 'Max Marks' not in course_info[sub].keys():
                        course_info[sub]['Max Marks'] = Question[i]['Marks']
                    else:
                        course_info[sub]['Max Marks'] += Question[i]['Marks']

        reader = PdfReader(response)
        # Extract text from each page
        text = ''
        for page_number in range(len(reader.pages)):
            page = reader.pages[page_number]
            extracted_text = page.extract_text()
            text = text + extracted_text

        rsheet = []
        for page in reader.pages:
            rsheet.append(page.extract_text().split('\n'))

        read_info = True
        read_response = False
        read_id = True
        start = False
        response_info = {}
        ri = 0
        curq = 0
        Response = {}
        for i in rsheet:
            for j in i:
                if read_info:
                    ri += 1
                    if j not in response_info.keys() and ri % 2 == 1:
                        temp = j
                    else:
                        response_info[temp] = j

                if 'Test Center Name' in j or 'Question Id' in j:
                    read_info = False

                if read_response and 'Unanswered' not in j:
                    Response[curq]['Response'] = j
                    Response[curq]['Attempt'] = True
                    if Question[curq]['Question Type'] == 'MCQ':
                        for opt in Question[curq]['Options']:
                            if j in opt['ID']:
                                Response[curq]['Response'] = str(opt['Number'])
                                if opt['Answer']:
                                    Response[curq]['Awarded Marks'] = Question[curq]['Marks']
                                else:
                                    Response[curq]['Awarded Marks'] = 0
                        Response[curq]['Max Marks'] = Question[curq]['Marks']
                    elif Question[curq]['Question Type'] == 'MSQ':
                        msq = j.split(',')
                        Response[curq]['Awarded Marks'] = 0
                        wrong = False
                        Response[curq]['Response'] = ''
                        for a in msq:
                            for opt in Question[curq]['Options']:
                                if a in opt['ID']:
                                    Response[curq]['Response'] += str(opt['Number']) + ','
                                if a in opt['ID'] and not wrong:
                                    if opt['Answer']:
                                        Response[curq]['Awarded Marks'] += Question[curq]['Marks'] / len(Question[curq]['Answer'])
                                    else:
                                        Response[curq]['Awarded Marks'] = 0
                                        wrong = True
                                        break
                        Response[curq]['Max Marks'] = Question[curq]['Marks']
                    else:
                        Response[curq]['Response'] = j
                        if 'to' in Question[curq]['Answer']:
                            sa = Question[curq]['Answer'].split('to')
                            min = float(sa[0])
                            max = float(sa[1])
                            if float(j) >= min and float(j) <= max:
                                Response[curq]['Awarded Marks'] = Question[curq]['Marks']
                            else:
                                Response[curq]['Awarded Marks'] = 0
                        else:
                            ans = Question[curq]['Answer'].split(' ')[0]
                            if ans == j.split(' ')[0]:
                                Response[curq]['Awarded Marks'] = Question[curq]['Marks']
                            else:
                                Response[curq]['Awarded Marks'] = 0
                        Response[curq]['Max Marks'] = Question[curq]['Marks']
                    read_response = False
                    read_id = False

                elif read_response:
                    Response[curq]['Response'] = j
                    Response[curq]['Attempt'] = False
                    read_response = False
                    read_id = False


                if read_id and start:
                    for q in Question:
                        if j in Question[q]['Data'] and 'Unanswered' not in j:
                            curq = q
                            read_response = True
                            Response[curq] = {}
                            Response[curq]['ID'] = j
                            Response[curq]['Number'] = curq
                            Response[curq]['Subject'] = Question[q]['Subject']
                            Response[curq]['Answer'] = Question[q]['Answer']
                            Response[curq]['Question Type'] = Question[q]['Question Type']
                            Response[curq]['Attempt'] = False

                if 'Options Selected' in j:
                    start = True

                read_id = True


        Summary = {}

        for sub in course_info:
            Summary[sub] = {}
            Summary[sub]['User Marks'] = 0
            Summary[sub]['Max Marks'] = course_info[sub]['Max Marks']
            for i in Response:
                if Response[i]['Subject'] == sub and Response[i]['Attempt']:
                    Summary[sub]['User Marks'] += Response[i]['Awarded Marks']

        st.table(response_info)

        Data = {}
        index = 1
        for sub in Summary:
            Data[index] = {}
            Data[index]['Subject'] = sub
            Data[index]['User Marks'] = Summary[sub]['User Marks']
            Data[index]['Max Marks'] = Summary[sub]['Max Marks']
            Data[index]['Percentage(%)'] = (Summary[sub]['User Marks']*100)/Summary[sub]['Max Marks']
            index += 1

        df1 = pd.DataFrame.from_dict(Data, orient="index")

        st.write(df1)

        Display = {}
        for i in Response:
            if Response[i]['Attempt']:
                t = int(i)
                Display[t] = {}
                Display[t]['Subject'] = Response[i]['Subject']
                Display[t]['Q No.'] = Response[i]['Number']
                Display[t]['Q Type'] = Response[i]['Question Type']
                Display[t]['Response'] = Response[i]['Response']
                if Response[i]['Question Type'] != 'SA':
                    Display[t]['Answer'] = ','.join(Response[i]['Answer'])
                else:
                    Display[t]['Answer'] = Response[i]['Answer']
                Display[t]['Marks Awarded'] = Response[i]['Awarded Marks']
                Display[t]['Max Marks'] = Response[i]['Max Marks']



        df = pd.DataFrame.from_dict(Display, orient="index")

        st.write(df)



if __name__ == "__main__":
    main()