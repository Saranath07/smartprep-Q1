import streamlit as st
#from streamlit_extras.app_logo import add_logo
import sqlite3
from io import BytesIO


st.set_page_config(page_title="SmartPrep",page_icon="https://i.imgur.com/S9k9LNT.png")

# Function to fetch subjects from the database
def fetch_subjects():
    conn = sqlite3.connect("database.db")  # Update with your database name
    cursor = conn.cursor()

    cursor.execute("SELECT subjectname FROM Subjects")
    subjects = cursor.fetchall()
    frame = []
    for i in subjects:
        if i not in frame:
            frame.append(i)

    conn.close()
    return [subject[0] for subject in frame]


# Function to fetch papers by subject from the database
def fetch_papers_by_subject(subject):
    conn = sqlite3.connect("database.db")  # Update with your database name
    cursor = conn.cursor()
    paperid_list = []
    cursor.execute("SELECT subjects,paperid,papername,exam,paperterm FROM Paper")
    info = cursor.fetchall()

    for i in info:
        if subject in i[0]:
            for sub in i[0].split(','):
                if subject == sub:
                    paperid_list.append((i[1],i[2],i[3],i[4]))
                    break

    conn.close()
    return [paper for paper in paperid_list]


# Function to fetch questions by paper from the database
def fetch_questions_by_paper(paper, subject):
    conn = sqlite3.connect("database.db")  # Update with your database name
    cursor = conn.cursor()
    full_data = []
    cursor.execute("SELECT questionid, questiontext, questiontype, answer, imageids, marks, compid FROM Question WHERE paperid=? and subject=?", (paper,subject,))
    questions = cursor.fetchall()

    for i in questions:
        options = []
        comprehension = []
        cursor.execute("SELECT optnumber, opttext, answer, imageids FROM Options where questionid=?", (i[0],))
        options = cursor.fetchall()

        if i[6] != 'NONE':
            cursor.execute("SELECT comptext, imageids FROM Comprehension WHERE compid=?", (i[6],))
            comprehension = cursor.fetchall()

        full_data.append((i,options,comprehension))

    conn.close()
    return full_data

def fetch_image_by_id(imageid):

    conn = sqlite3.connect("database.db")  # Update with your database name
    cursor = conn.cursor()
    cursor.execute("SELECT image FROM Image WHERE imageid=?", (imageid,))
    blobdata = cursor.fetchall()

    return blobdata[0][0]

def btn_b_callback():
    st.session_state.display_result = False
    st.session_state.reset = False

def update_page_views():
    # Read the current page view count from the data store
    with open("page_views.txt", "r") as file:
        page_views = int(file.read())

    # Increment the page view count
    page_views += 1

    # Update the data store with the new count
    with open("page_views.txt", "w") as file:
        file.write(str(page_views))

    return page_views

def update_reviews(review):
    with open("page_reviews.txt", "r") as file:
        page_reviews = file.read()

    # Increment the page view count
    page_reviews += " -- " + review

    # Update the data store with the new count
    with open("page_reviews.txt", "w") as file:
        file.write(str(page_reviews))



def add_logo():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url(https://i.imgur.com/n1v7QfM.png);
                background-repeat: no-repeat;
                padding-top: 120px;
                background-position: 20px 20px;
                margin-top: 25px;

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
    st.title("Smartprep")


    st.write("Hello Everyone! Please select the below options to get your desired paper to practice. if you are unable to understand how to use the website, please go to guidelines section to know more. Happy preparation my friend! All the best for your exam.")
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url(https://drive.google.com/file/d/1GdRn4OQ4fZT0HsJ5NAFympFp-Q08Yczq/view?usp=sharing);
                background-repeat: no-repeat;
                padding-top: 100px;
                background-position: 20px 20px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
    subjects = sorted(fetch_subjects())
    selected_subject = st.selectbox("Select a subject", subjects)

    #add_logo("https://i.imgur.com/W0NrmI1.png")
    add_logo()


    papers = fetch_papers_by_subject(selected_subject)
    pnames = []
    paper_dict = {}
    for i in papers:
        term = i[3].split('T')
        year = 2000 + int(term[0])
        if term[1] == '1':
            month = 'Jan'
        elif term[1] == '2':
            month = 'May'
        else:
            month = 'Sept'

        if 'ET' in i[2]:
            exam = 'END TERM'
        elif 'Q2' in i[2]:
            exam = 'QUIZ 2'
        else:
            exam = 'QUIZ 1'

        pnames.append(month+' '+str(year)+' '+exam+': '+i[1])
        paper_dict[i[0]] = month+' '+str(year)+' '+exam+': '+i[1]

    selected_paper = st.selectbox("Select a paper", pnames)

    for i in paper_dict:
        if selected_paper == paper_dict[i]:
            selected_paper = i
    st.write("\n")
    selected_mode = st.selectbox("Select mode of exam", ["Practice Mode", "Exam Mode"])
    st.title("Questions")

    questions = fetch_questions_by_paper(selected_paper,selected_subject)
    qnum = 1
    optnum = 1

    if selected_mode == "Practice Mode":
        for i in questions:
            images_list = []
            ans_text = 'NONE'
            st.subheader(f"Question Number {qnum}")
            mcq = []
            optnum = 1
            if len(i[2]) > 0:
                st.markdown(f"{i[2][0][0]}")
                images_list = i[2][0][1].split("//")

                if len(images_list) > 0:
                    for img in images_list:
                        if len(img) > 2:
                            selected_image = fetch_image_by_id(img)
                            image_bytes = bytes(selected_image)
                            image_stream = BytesIO(image_bytes)
                            st.image(image_stream)

            st.markdown(f"{i[0][1]}")

            #questionid, questiontext, questiontype, answer, imageids, marks, compid

            if len(i[0][4]):
                images_list = i[0][4].split("//")

                if len(images_list) > 0:
                    for img in images_list:
                        if len(img) > 2:
                            selected_image = fetch_image_by_id(img)
                            image_bytes = bytes(selected_image)
                            image_stream = BytesIO(image_bytes)
                            st.image(image_stream)

            right_aligned_bold_text = f"<div style='text-align: right;'><b>[Marks: {i[0][5]}]</b></div>"
            st.markdown(right_aligned_bold_text, unsafe_allow_html=True)

            if "MCQ" in i[0][2]:
                if len(i[1][0][3]) > 4:
                    optnum = 1
                    for j in i[1]:
                        try:
                            selected_image = fetch_image_by_id(j[3])
                            image_bytes = bytes(selected_image)
                            image_stream = BytesIO(image_bytes)
                            st.image(image_stream)
                            mcq.append(str(optnum))

                        except:
                            st.markdown(f"<div style='color: #BF40BF'><p>Unable to retrieve option {optnum}. Sorry for the inconvenience caused. we will try to resolve this asap. We suggest you to not attempt this question as we are unsure that this question data is accurate</p></div>",unsafe_allow_html=True)
                        optnum += 1

                    st.radio("Select the Option based on Images above", mcq, key=i[0][0]+'__'+str(optnum))

                else:
                    optlist = []
                    for j in i[1]:
                        optlist.append(j[1])

                    st.radio("Select an Option", optlist,key=i[0][0]+'__'+str(optnum))

                ans_text = "The Correct Option is " + i[0][3]

            elif "MSQ" in i[0][2]:
                for j in i[1]:
                    st.checkbox(j[1],key=i[0][0]+'__'+str(optnum))
                    if len(j[3]) > 4:
                        try:
                            selected_image = fetch_image_by_id(j[3])
                            image_bytes = bytes(selected_image)
                            image_stream = BytesIO(image_bytes)
                            st.image(image_stream)

                        except:
                            st.markdown(
                                f"<div style='color: #BF40BF'><p>Unable to retrieve option {optnum}. Sorry for the inconvenience caused. we will try to resolve this asap. We suggest you to skip the question since we cant assure whether question data is accurate!</p></div>",
                                unsafe_allow_html=True)

                    optnum += 1
                ans = i[0][3].split(',')
                ans_text = "The Correct Options is/are"
                for k in ans:
                    ans_text += ' ' + k + ','
                ans_text = ans_text[:-1]
            else:
                ans_text = ''
                st.text_input("Answer:",key=i[0][0])
                ans = i[0][3].split(',')
                for k in ans:
                    ans_text += k
                if ",,," in i[0][3]:
                    arr1 = []
                    tans = i[0][3].split(',,,')
                    for sep in tans:
                        sep1 = ''.join(sep.split(','))
                        arr1.append(sep1)
                    ans_text = ','.join(arr1)
            qnum+=1

            button_a = st.button('Show Answer',key=i[0][0]+"SA")
            if button_a:
                st.write(ans_text)
                placeholder = st.empty()
                isclick = placeholder.button('Hide Answer')
                if isclick:
                    placeholder.empty()


            st.markdown('----')


    elif selected_mode == "Exam Mode":

        optnum = 1
        Total = []
        User_Total = []
        User_Attempts = []
        optcheck_dict = {}
        mcq = []

        for i in questions:
            if i[0][0].split('Q')[-1] not in optcheck_dict.keys():
                optcheck_dict[i[0][0].split('Q')[-1]] = 0
            optcheck_dict[i[0][0].split('Q')[-1]] = 0

        submitted = False
        for i in questions:
            images_list = []
            ans_text = 'NONE'
            answer = ''
            checkbox_ans = []
            Total.append(i[0][5])
            optnum = 1
            mcq = []
            st.subheader(f"Question Number {qnum}")
            if len(i[2]) > 0:
                st.markdown(f"{i[2][0][0]}")
                images_list = i[2][0][1].split("//")

                for img in images_list:
                    if len(img) > 2:
                        selected_image = fetch_image_by_id(img)
                        image_bytes = bytes(selected_image)
                        image_stream = BytesIO(image_bytes)
                        st.image(image_stream)

            st.markdown(f"{i[0][1]}")

            # questionid, questiontext, questiontype, answer, imageids, marks, compid

            if len(i[0][4]):
                images_list = i[0][4].split("//")

                for img in images_list:
                    if len(img) > 2:
                        selected_image = fetch_image_by_id(img)
                        image_bytes = bytes(selected_image)
                        image_stream = BytesIO(image_bytes)
                        st.image(image_stream)

            right_aligned_bold_text = f"<div style='text-align: right;'><b>[Marks: {i[0][5]}]</b></div>"
            st.markdown(right_aligned_bold_text, unsafe_allow_html=True)

            if "MCQ" in i[0][2]:
                optnum = 1
                if len(i[1][0][3]) > 4:
                    for j in i[1]:
                        try:
                            selected_image = fetch_image_by_id(j[3])
                            image_bytes = bytes(selected_image)
                            image_stream = BytesIO(image_bytes)
                            st.image(image_stream)
                            mcq.append(str(optnum))

                        except:
                            st.markdown(
                                f"<div style='color: #BF40BF'><p>Unable to retrieve option {optnum}. Sorry for the inconvenience caused. we will try to resolve this asap. We suggest you to not attempt this question as we are unsure that this question data is accurate</p></div>",
                                unsafe_allow_html=True)

                        optnum += 1
                    r_answer = st.radio("Select the Option based on Images above", mcq,
                                        key=i[0][0] + '__' + str(optnum))

                else:
                    optlist = []
                    for j in i[1]:
                        optlist.append(j[1])

                    r_answer = st.radio("Select an Option", optlist, key=i[0][0] + '__' + str(optnum))
                    r_answer = str(optlist.index(r_answer) + 1)

                ans_text = "The Correct Option is " + i[0][3]


                if r_answer == i[0][3]:
                    ans_text = "Your answer is correct. " + ans_text
                    User_Total.append(i[0][5])
                else:
                    User_Total.append(0)
                    ans_text = "Your answer is wrong. " + ans_text + ". You Answered " + r_answer

                User_Attempts.append(ans_text)


            elif "MSQ" in i[0][2]:
                for j in i[1]:
                    checkbox_ans.append(st.checkbox(j[1], key=i[0][0] + '__' + str(optnum)))
                    if len(j[3]) > 4:
                        try:
                            selected_image = fetch_image_by_id(j[3])
                            image_bytes = bytes(selected_image)
                            image_stream = BytesIO(image_bytes)
                            st.image(image_stream)

                        except:
                            st.markdown(
                                f"<div style='color: #BF40BF'><p>Unable to retrieve option {optnum}. Sorry for the inconvenience caused. we will try to resolve this asap. We suggest you to not attempt this question as we are unsure that this question data is accurate</p></div>",
                                unsafe_allow_html=True)

                    optnum += 1
                ans = i[0][3].split(',')
                ans_text = "The Correct Options is/are"
                for k in ans:
                    ans_text += ' ' + k + ','
                ans_text = ans_text[:-1]

                opt = 0
                answer_t = ''
                for check in checkbox_ans:
                    opt += 1
                    if check:
                        answer_t += str(opt) + ','

                if answer_t[:-1] == i[0][3]:
                    User_Total.append(i[0][5])
                    ans_text = "Your answer is correct. " + ans_text

                else:
                    ut = 0
                    wrong = False
                    for answ in answer_t[:-1].split(','):
                        if len(answ) == 0:
                            wrong = True
                            break
                        elif answ in i[0][3]:
                            ut += i[0][5]/len(ans)
                        else:
                            wrong = True
                            break
                    if wrong:
                        User_Total.append(0)
                        if len(answer_t) > 0:
                            ans_text = "Your answer is wrong. " + ans_text + ". You Answered " + answer_t[:-1]
                        else:
                            ans_text = "Your answer is wrong. " + ans_text + ". You didnt Answer anything."
                    else:
                        User_Total.append(ut)
                        ans_text = "Your answer is partially correct. " + ans_text + ". You Answered " + answer_t[:-1]

                User_Attempts.append(ans_text)

            else:
                ans_text = ''
                answer = st.text_input("Answer:", key=i[0][0])
                ans = i[0][3].split(',')
                for k in ans:
                    ans_text += k

                if ",,," in i[0][3]:
                    arr = []
                    tans = i[0][3].split(',,,')
                    for sep in tans:
                        sep1 = ''.join(sep.split(','))
                        arr.append(sep1)
                    ans_text = ','.join(arr)

                    if len(answer) == 0:
                        User_Total.append(0)
                        temp = "You did not answer anything for this. Correct Answer is " + ans_text
                    elif ans_text == answer:
                        User_Total.append(i[0][5])
                        temp = "Your answer is correct. " + "Correct Answer is " + ans_text
                    else:
                        User_Total.append(0)
                        temp = "Your answer is wrong. " + "Correct Answer is " + ans_text + ". You Answered " + answer


                elif 'to' in ''.join(i[0][3].split(',')):
                    range_min = float((''.join(i[0][3].split(','))).split('to')[0])
                    range_max = float((''.join(i[0][3].split(','))).split('to')[1])
                    try:
                        if answer == ''.join(i[0][3].split(',')):
                            User_Total.append(i[0][5])
                            temp = "Your answer is correct. " + "Correct Answer is " + ans_text
                        elif float(answer) >= range_min and float(answer) <= range_max:
                            User_Total.append(i[0][5])
                            temp = "Your answer is correct. " + "Correct Answer is " + ans_text + ". You Answered " + answer
                        else:
                            User_Total.append(0)
                            temp = "Your answer is wrong. " + "Correct Answer is " + ans_text + ". You Answered " + answer
                    except:
                        User_Total.append(0)
                        if len(answer) == 0:
                            temp = "You did not answer anything for this. Correct Answer is " + ans_text
                        else:
                            temp = "Your answer is wrong. " + "Correct Answer is " + ans_text + ". You Answered " + answer
                elif answer in ''.join(i[0][3].split(',')):
                    try:
                        if answer == ''.join(i[0][3].split(',')):
                            User_Total.append(i[0][5])
                            temp = "Your answer is correct. " + "Correct Answer is " + ans_text
                        elif float(answer) == float(''.join(i[0][3].split(','))):
                            User_Total.append(i[0][5])
                            temp = "Your answer is correct. " + "Correct Answer is " + ans_text
                        else:
                            User_Total.append(0)
                            temp = "Your answer is wrong. " + "Correct Answer is " + ans_text + ". You Answered " + answer
                    except:
                        User_Total.append(0)
                        if len(answer) == 0:
                            temp = "You did not answer anything for this. Correct Answer is " + ans_text
                        else:
                            temp= "Your answer is wrong. " + "Correct Answer is " + ans_text + ". You Answered " + answer
                else:
                    User_Total.append(0)
                    if len(answer) == 0:
                        temp = "You did not answer anything for this. Correct Answer is " + ans_text
                    else:
                        temp = "Your answer is wrong. " + "Correct Answer is " + ans_text + ". You Answered " + answer

                User_Attempts.append(temp)
            qnum += 1

            st.markdown('----')

        submit = st.button("Submit", key="EXAMMODE")



        if submit:
            submitted = True

        if submitted:
            st.markdown(f"""
                <div style="background-color: #e0f2f1; padding: 10px; text-align: center;line-height: 120%; margin: 20px; margin-bottom: 50px; border-radius: 5px; border: 2px dotted black;">
                    <p style="margin-top: 10px;">Your Score:</p>
                    <p style="font-size: 400%;">{((sum(User_Total)*100)//sum(Total))}/100</p>
                </div>
            """,unsafe_allow_html=True)

            qnum = 1
            optnum = 1
            ua = 0
            for i in questions:
                images_list = []
                ans_text = 'NONE'
                st.subheader(f"Question Number {qnum}")
                mcq = []
                if len(i[2]) > 0:
                    st.markdown(f"{i[2][0][0]}")
                    images_list = i[2][0][1].split("//")

                    for img in images_list:
                        if len(img) > 2:
                            selected_image = fetch_image_by_id(img)
                            image_bytes = bytes(selected_image)
                            image_stream = BytesIO(image_bytes)
                            st.image(image_stream)

                st.markdown(f"{i[0][1]}")

                # questionid, questiontext, questiontype, answer, imageids, marks, compid

                if len(i[0][4]):
                    images_list = i[0][4].split("//")

                    for img in images_list:
                        if len(img) > 2:
                            selected_image = fetch_image_by_id(img)
                            image_bytes = bytes(selected_image)
                            image_stream = BytesIO(image_bytes)
                            st.image(image_stream)

                right_aligned_bold_text = f"<div style='text-align: right;'><b>[Marks: {i[0][5]}]</b></div>"
                st.markdown(right_aligned_bold_text, unsafe_allow_html=True)

                if "MCQ" in i[0][2]:
                    if len(i[1][0][3]) > 4:
                        optnum = 1
                        for j in i[1]:
                            try:
                                selected_image = fetch_image_by_id(j[3])
                                image_bytes = bytes(selected_image)
                                image_stream = BytesIO(image_bytes)
                                st.image(image_stream)
                                mcq.append(str(optnum))

                            except:
                                st.markdown(
                                    f"<div style='color: #BF40BF'><p>Unable to retrieve option {optnum}. Sorry for the inconvenience caused. we will try to resolve this asap. We suggest you to not consider this question as we are unsure that this question data is accurate</p></div>",
                                    unsafe_allow_html=True)

                            optnum += 1

                    else:
                        optlist = []
                        for j in i[1]:
                            if j[2]:
                                st.markdown(f'<p style="color: green;">{j[1]}</p>', unsafe_allow_html=True)
                            else:
                                st.markdown(f'<p style="color: red;">{j[1]}</p>', unsafe_allow_html=True)

                    ans_text = "The Correct Option is " + i[0][3]
                    st.markdown(f'<p style="font-weight: bold;">{User_Attempts[ua]}</p>', unsafe_allow_html=True)


                elif "MSQ" in i[0][2]:
                    for j in i[1]:
                        if j[2]:
                            st.markdown(f'<p style="color: green;">{j[1]}</p>', unsafe_allow_html=True)
                        else:
                            st.markdown(f'<p style="color: red;">{j[1]}</p>', unsafe_allow_html=True)

                        if len(j[3]) > 4:
                            try:
                                selected_image = fetch_image_by_id(j[3])
                                image_bytes = bytes(selected_image)
                                image_stream = BytesIO(image_bytes)
                                if j[2]:
                                    st.markdown(
                                        """
                                        <style>
                                        .custom-container {
                                            background-color: green;
                                            padding: 5px;
                                        }
                                        .custom-image {
                                            display: block;
                                            width: 100%;
                                            border: 4px solid green;
                                        }
                                        </style>
                                        """,
                                        unsafe_allow_html=True
                                    )

                                    # Display the image within the custom-styled container
                                    st.markdown('<div class="custom-container"></div>', unsafe_allow_html=True)
                                    st.image(image_bytes, output_format="auto")
                                    st.markdown('<div class="custom-container"></div>', unsafe_allow_html=True)
                                else:
                                    st.markdown(
                                        """
                                        <style>
                                        .customi-container {
                                            background-color: red;
                                            padding: 5px;
                                        }
                                        .customi-image {
                                            display: block;
                                            width: 100%;
                                            border: 4px solid green;
                                        }
                                        </style>
                                        """,
                                        unsafe_allow_html=True
                                    )

                                    # Display the image within the custom-styled container
                                    st.markdown('<div class="customi-container"></div>', unsafe_allow_html=True)
                                    st.image(image_bytes, output_format="auto")
                                    st.markdown('<div class="customi-container"></div>', unsafe_allow_html=True)
                            except:
                                st.markdown(
                                    f"<div style='color: #BF40BF'><p>Unable to retrieve option {optnum}. Sorry for the inconvenience caused. we will try to resolve this asap. We suggest you to not consider this question as we are unsure that this question data is accurate</p></div>",
                                    unsafe_allow_html=True)

                        optnum += 1
                    ans = i[0][3].split(',')
                    ans_text = "The Correct Options is/are"
                    for k in ans:
                        ans_text += ' ' + k + ','
                    ans_text = ans_text[:-1]
                    st.markdown(f'<p style="font-weight: bold;">{User_Attempts[ua]}</p>', unsafe_allow_html=True)
                else:
                    ans_text = ''
                    ans = i[0][3].split(',')
                    for k in ans:
                        ans_text += k

                    if ",,," in i[0][3]:
                        arr1 = []
                        tans = i[0][3].split(',,,')
                        for sep in tans:
                            sep1 = ''.join(sep.split(','))
                            arr1.append(sep1)
                        ans_text = ','.join(arr1)

                    st.markdown(f'<p style="color: green;">{ans_text}</p>', unsafe_allow_html=True)
                    st.markdown(f'<p style="font-weight: bold;">{User_Attempts[ua]}</p>', unsafe_allow_html=True)

                if ua < len(User_Attempts) - 1:
                    ua += 1

                qnum += 1

                st.markdown('----')



if __name__ == "__main__":
    main()
