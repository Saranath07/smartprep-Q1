import streamlit as st

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

    add_logo()
    st.title("Guidelines")

    st.write("This website allows you to practice for your quizzes and endterm in a easier and smarter way. If you are unable to understand how to use this website, follow the below instructions\n")
    st.write("As you can see in the startpage, we asked you to select for a subject, a paper and mode of exam. \n")
    st.subheader("Subject")
    st.write(" Select the subject which you want to practice. once you change the subject in the dropdown, your previous data might get lost. so please choose wisely the subject you want to practice and once completely done with the subject, move for the next one.")
    st.write("For few subjects, there are multiple entries in the selectbox. for example: Deep learning has 2 entries. one is Deep Learning with capital L and other one is deep learning with small l. SW Engg and Sw Engg are same as well. we are looking into the issue and will resolve asap.")
    st.write("All foundational level courses have 2 entries as well. Ex: Maths1 and Sem1 Maths1, Statistics 2 and Sem2 Statistics 2. both entries have different papers so please check both of them and we are sorry for the inconvenience again")
    st.subheader("Papers")
    st.write("After selecting the subject, Select the paper which you want to practice for your preparation. as you can see, the papers naming is sorted in (TERM) (QUIZ/ENDTERM): (PAPER NAME). here TERM is the term in which the paper is released and QUIZ/ENDTERM represents whether its Quiz1,Quiz2 or endterm. and paper name represents the name of paper which is given by iitm. if you are unaware of paper name, just keep practicing a random paper and move to next one once completed. ")
    st.write("There are few Questions where options are not displayed. we regret for the inconvenience caused. only 5 questions out of all the questions of all papers dont have options. we are looking into this and will resolve as soon as possible")
    st.subheader("Mode of Exam")
    st.write("After selecting both subject and paper, Select the mode of exam you want to attempt.\n If you want to attempt the paper in a practicing fashion without validating your answers, then we suggest you to go for practice mode which allows you to see answer at any time by clicking the button show answer.\n")
    st.write("If you want to attempt the paper in a exam like fashion where you want ot validate your answers and test yourself how good you are in the particular subject, then we suggest you to go for exam mode. once you finish attempting the paper, click on submit button below so that the score will be displayed and correct answers and your atempted answers also will be displayed below.")
    st.markdown('----')
    st.write("\n\n\nNOTE: We understand that there are few difficulties in using the website as streamlit has a limited number of fucntions to execute the website in a desired manner. if you feel any or have any suggestions for us to improvise the website then please mail us at 21f1005681@student.onlinedegree.iitm.ac.in. ")
if __name__ == "__main__":
    main()
