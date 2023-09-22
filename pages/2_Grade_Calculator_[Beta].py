import streamlit as st

st.set_page_config(page_title="SmartPrep",page_icon="https://i.imgur.com/S9k9LNT.png")

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


def Grade(T,OPcheck = True):
    
    if((not OPcheck) and (T >= 40)):
        grade = "I_OP"
    elif(T >= 90):
        grade = "S"
    elif(T >= 80):
        grade = "A"
    elif(T >= 70):
        grade = "B"
    elif(T >= 60):
        grade = "C"
    elif(T >= 50):
        grade = "D"
    elif(T >= 40):
        grade = "E"
    else:
        grade = "U"

    container = f"""
        <div style="background-color: #7beaf3; padding: 10px; text-align: center;line-height: 120%; margin: 20px; margin-bottom: 50px; border-radius: 5px; border: 2px dotted black;">
            <p style="margin-top: 10px; font-size: 150%;">Your Grade:</p>
            <p style="font-size: 220%;">{grade}</p>
            <p style="margin-top: 40px; font-size: 150%;">Your score: {T}</p>
        </div>
    """

    st.markdown(container, unsafe_allow_html=True)

def foundational(subject):
    ELG = st.selectbox("Do you know if you are eligible for End-Term or not?",["Yes","No"])
    check = False
    if(ELG == "No"):
        st.write("Enter 5 Highest scores in the first 9 weeks of Graded Assignments")

        GA1 = (st.number_input("Highest Score 1",step = 1,min_value = -1,max_value = 100))
        GA2 = (st.number_input("Highest Score 2",step = 1,min_value = -1,max_value = 100))
        GA3 = (st.number_input("Highest Score 3",step = 1,min_value = -1,max_value = 100))
        GA4 = (st.number_input("Highest Score 4",step = 1,min_value = -1,max_value = 100))
        GA5 = (st.number_input("Highest Score 5",step = 1,min_value = -1,max_value = 100))

        if (GA1+GA2+GA3+GA4+GA5 >= 200):
            st.write("You are Eligible for End-Term!!")
            check = True

        elif (min(GA1,GA2,GA3,GA4,GA5) > -1):
            st.write("You are not Eligible for End-Term. Better luck next time")

        else:
            st.write("Enter the Values")

    
    if(check or (ELG == "Yes")):
        T = 0
        GAA = st.number_input("Average score in Best 10 out of all weekly graded assignments",step = 1,min_value = 0,max_value = 100)
        Q1 = st.number_input("Score in Quiz 1 (-1, if not attempted)",step = 1,min_value = 0,max_value = 100)
        if(subject != "Introduction to Python programming"):
            Q2 = st.number_input("Score in Quiz 2 (-1, if not attempted)",step = 1,min_value = 0,max_value = 100)
        ET = st.number_input("Score in End Term (THIS CANNOT BE 0!!)",step = 1,min_value = 0,max_value = 100)
        BONUS = st.number_input("Bonus marks if any",value = 0,step = 1,min_value = 0,max_value = 5)
        if(subject == "Statistics for Data Science 2"):
            ea = st.number_input("Extra Activity Marks",value = 0,step = 1,min_value = 0,max_value = 10)
            T += ea
        if(subject == "Introduction to Python programming"):
            OPE1 = st.number_input("Score in Programming Quiz 1 (-1, if not attempted)",step = 1,min_value = 0,max_value = 100)
            OPE2 = st.number_input("Score in Programming Quiz 2 (-1, if not attempted)",step = 1,min_value = 0,max_value = 100)
            WTA =  st.number_input("Average of 6 best out of 8 Weekly Timed Assignments",step = 1,min_value = 0,max_value = 100)
        
        if st.button("Submit"): 
            if(subject == "Introduction to Python programming"):
                T += 0.1*GAA + BONUS
                T += 0.1*Q1
                if(0.4*ET + 0.2*max(OPE1, OPE2) >= 0.4*ET + 0.25*max(OPE1,OPE2) + 0.15*min(OPE1,OPE2)):
                    T += 0.4*ET + 0.2*max(OPE1,OPE2)
                else:
                    T += 0.4*ET + 0.25*max(OPE1,OPE2) + 0.15*min(OPE1,OPE2)
                if(max(OPE1,OPE2) >= 40):
                    Grade(T)
                else:
                    Grade(T,OPcheck = False)
            else:
                T += 0.1*GAA + BONUS
                if ((0.6*ET + 0.2*max(Q1,Q2)) >= (0.4*ET + 0.2*Q1 + 0.3*Q2)):
                    T += (0.6*ET + 0.2*max(Q1,Q2))
                else:
                    T += (0.4*ET + 0.2*Q1 + 0.3*Q2)
                Grade(T)

    elif(check):
        st.write("You're not eligible to write End-Term")

def diploma(subject):
    ELG = st.selectbox("Do you know if you are eligible for End-Term or not?",["Yes","No"])
    check = False
    if(ELG == "No" and (subject != "Business Analytics (DS Diploma)")): 
        st.write("Enter 5 Highest scores in the first 9 weeks of Graded Assignments")

        GA1 = (st.number_input("Highest Score 1",step = 1,min_value = -1,max_value = 100))
        GA2 = (st.number_input("Highest Score 2",step = 1,min_value = -1,max_value = 100))
        GA3 = (st.number_input("Highest Score 3",step = 1,min_value = -1,max_value = 100))
        GA4 = (st.number_input("Highest Score 4",step = 1,min_value = -1,max_value = 100))
        GA5 = (st.number_input("Highest Score 5",step = 1,min_value = -1,max_value = 100))

        if (GA1+GA2+GA3+GA4+GA5 >= 200):
            st.write("You are Eligible for End-Term!!")
            check = True

        elif (min(GA1,GA2,GA3,GA4,GA5) > -1):
            st.write("You are not Eligible for End-Term. Better luck next time")

        else:
            st.write("Enter the Values")

    elif(ELG == "No" and subject == "Business Analytics (DS Diploma)"):
        A1 = (st.radio("Did you attempt Assignment 1",["Yes","No"]))
        A2 = (st.radio("Did you attempt Assignment 2",["Yes","No"]))
        if(A1 == "No" and A2 == "No"):
            check = False
            st.write("You are not Eligible for End-Term. Better luck next time")
        else:
            check = True
 
    if(check or (ELG == "Yes")):
        T = 0
        if(subject != "Business Analytics (DS Diploma)"):
            GAA = st.number_input("Average score in Best 10 out of all weekly graded assignments",step = 1,min_value = 0,max_value = 100)
        if(subject != "Business Data management (DS Diploma)" and subject != "Tools in Data Science (DS Diploma)"):
            Q1 = st.number_input("Score in Quiz 1 (-1, if not attempted)",step = 1,min_value = 0,max_value = 100)
            Q2 = st.number_input("Score in Quiz 2 (-1, if not attempted)",step = 1,min_value = 0,max_value = 100)
        if(subject == "Programming Data structures and algorithms using Python (PDSA) (Diploma in Programming)"):
            OP = st.number_input("Score in Online Programming Exam (-1, if not attempted)",step = 1,min_value = 0,max_value = 100)
        if(subject == "Database management system (DBMS) (Diploma in Programming)"):
            DB_GAA2 = st.number_input("Average of PostgreSQL Assignments (-1, if not attempted)",step = 1,min_value = 0,max_value = 100)
            DB_GAA3 = st.number_input("Programming Assignment Score (-1, if not attempted)",step = 1,min_value = 0,max_value = 100)
            DB_OP = st.number_input("Score in Online Programming Exam (-1, if not attempted)",step = 1,min_value = 0,max_value = 100)
        if(subject == "Modern Application development - 1 (Diploma in programming)"):
            GLA1 = st.number_input("Average of best 5 out of 6 Graded Lab Assignments(-1 if not attempted)",step = 1,min_value = 0,max_value = 100)
        if(subject == "Programming concepts using Java (Diploma in programming)" or subject == "Machine Learning Practice (DS Diploma)"):
            OP1 = st.number_input("Score in Online Programming Exam 1 (-1, if not attempted)",step = 1,min_value = 0,max_value = 100)
            OP2 = st.number_input("Score in Online Programming Exam 2 (-1, if not attempted)",step = 1,min_value = 0,max_value = 100)
        if(subject == "Business Analytics (DS Diploma)"):
            A1 = st.number_input("Score in Assignment 1 (-1, if not attempted)",step = 1,min_value = 0,max_value = 20)
            A2 = st.number_input("Score in Assignment 2 (-1, if not attempted)",step = 1,min_value = 0,max_value = 20)
            A3 = st.number_input("Score in Assignment 3 (-1, if not attempted)",step = 1,min_value = 0,max_value = 20)
        if(subject == "Tools in Data Science (DS Diploma)"):
            ROE1 = st.number_input("Score in Remote Online Exam (-1, if not attempted)",step = 1,min_value = 0,max_value = 100)
            P1 = st.number_input("Score in Take Home Project 1 (-1, if not attempted)",step = 1,min_value = 0,max_value = 100)
            P2 = st.number_input("Score in Take Home Project 2 (-1, if not attempted)",step = 1,min_value = 0,max_value = 100)
        if(subject == "System commands (Diploma in programming)"):
            GAA1 = st.number_input("Score in Non Proctored Programming Exam 1 (-1, if not attempted)",step = 1,min_value = 0,max_value = 100,key = "A1")
            GAA2 = st.number_input("Score in Non Proctored Programming Exam 2 (-1, if not attempted)",step = 1,min_value = 0,max_value = 100,key = "G2")
            SC_OP1 = st.number_input("Score in Online Remote Proctored Programming Exam 1 (-1, if not attempted)",step = 1,min_value = 0,max_value = 100,key = "O1")
            SC_OP2 = st.number_input("Score in Online Remote Proctored Programming Exam 2 (-1, if not attempted)",step = 1,min_value = 0,max_value = 100,key = "P2")
            VMT = st.number_input("Score in VM Task (-1, if not attempted)",step = 1,min_value = 0,max_value = 100,key = "VM")
        if(subject == "Application Development - 2 (Diploma in programming)"):
            GLA2 = st.number_input("Average of 2 Graded Lab Assignments(-1 if not attempted)",step = 1,min_value = 0,max_value = 100)
        ET = st.number_input("Score in End Term ",step = 1,min_value = 0,max_value = 100)
        BONUS = st.number_input("Bonus marks if any",value = 0,step = 1,min_value = 0,max_value = 5)
        if st.button("Submit"):
            if(subject == "Business Data management (DS Diploma)"):
                T += 0.7*GAA + 0.3*ET
                Grade(T)
            elif(subject == "Programming Data structures and algorithms using Python (PDSA) (Diploma in Programming)"):
                T += 0.1*GAA + BONUS + 0.4*ET + 0.2*OP + max(0.2*max(Q1, Q2),(0.15*Q1 + 0.15*Q2))
                Grade(T)
            elif(subject == "Database management system (DBMS) (Diploma in Programming)"):
                T = 0.04*GAA + 0.03*DB_GAA2 + 0.03*DB_GAA3 + 0.2*DB_OP + max (0.45*ET + 0.15*max(Q1,Q2),0.4*ET + (0.10*Q1 + 0.20*Q2)) + BONUS
                if(DB_OP >= 35):
                    Grade(T)
                else:
                    Grade(T,OPcheck = False)
            elif(subject == "Modern Application development - 1 (Diploma in programming)"):
                T =  0.15*GLA1 + 0.05*GAA + max(0.35*ET + 0.2*Q1 + 0.25*Q2, 0.4*ET + 0.3*max(Q1,Q2)) + BONUS
                Grade(T)
            elif(subject == "Programming concepts using Java (Diploma in programming)"):
                T = 0.1*GAA + 0.3*ET + 0.2*max(OP1,OP2) + max (0.45*ET + 0.15*max(Q1,Q2),0.4*ET + (0.10*Q1 + 0.20*Q2))
                if(OP1 or OP2 >= 30):
                    Grade(T)
                else:
                    Grade(T,OPcheck = False)
            elif(subject == "Machine Learning Techniques (DS Diploma)"):
                T = 0.2*GAA + 0.4*ET + max(0.2*Q1 + 0.2*Q2,0.3*max(Q1,Q2)) + BONUS
                Grade(T)
            elif(subject == "Machine Learning Practice (DS Diploma)"):
                T = 0.1*GAA + 0.3*ET + 0.15*OP1 + 0.15*OP2 + max(0.15*Q1 + 0.15*Q2, 0.2*max(Q1,Q2)) + BONUS
                if(OP1 or OP2 >= 40):
                    Grade(T)
                else:
                    Grade(T,OPcheck = False)
            elif(subject == "Business Analytics (DS Diploma)"):
                Q = 0.7*max(Q1,Q2) + 0.3*min(Q1,Q2)
                A = A1 + A2 + A3 - min(A1,A2,A3)
                T = 0.2*Q + 0.2*A + 0.4*ET + BONUS
                Grade(T)
            elif(subject == "Tools in Data Science (DS Diploma)"):
                T = 0.1*GAA + 0.2*ROE1 + 0.2*P1 + 0.2*P2 + 0.3*ET + BONUS
                Grade(T)
            elif(subject == "System commands (Diploma in programming)"):
                G = 0.06*GAA + 0.02*GAA1 + 0.02*GAA2
                Q = max(0.15*Q1 + 0.15*Q2, 0.2*max(Q1,Q2)) + 0.3*ET
                O = 0.15*SC_OP1 + 0.15*SC_OP2 + 0.1*VMT
                T = G + Q + O + BONUS
                if(SC_OP1 or SC_OP2 >= 40):
                    Grade(T)
                else:
                    Grade(T,OPcheck = False)
            elif(subject == "Application Development - 2 (Diploma in programming)"):
                T =  0.05*GAA + 0.05*GLA2 + max(0.35*ET + 0.25*Q1 + 0.3*Q2, 0.5*ET + 0.3*max(Q1, Q2)) + BONUS
                Grade(T)
            else:
                T += 0.1*GAA + BONUS
                if ((0.6*ET + 0.2*max(Q1,Q2)) >= (0.4*ET + 0.2*Q1 + 0.3*Q2)):
                    T += (0.6*ET + 0.2*max(Q1,Q2))
                else:
                    T += (0.4*ET + 0.2*Q1 + 0.3*Q2)
                Grade(T)



def main():
    add_logo()
    st.title("Grade Calculator")
    st.markdown("Hello Everyone, Enter the relevant fileds for the subject of your choice. Once done with filling all the relevant fields, click on submit button for your Grade and Score in that subject. Please be patient with bugs, they are being worked upon. Thank you for using this Grade Calculator!")
    st.markdown("<i>Credits: Sai Prakash BVC</i>",unsafe_allow_html=True)

    level = ["Foundational","Diploma"]
    foundational_subjects = ["Mathematics for Data Science 1", "English 1", "Computational Thinking", "Statistics for Data Science 1", "Mathematics for Data Science 2", "English 2", "Introduction to Python programming", "Statistics for Data Science 2"]
    diploma_subjects = ["Machine Learning foundations (DS Diploma)", "Business Data management (DS Diploma)", "Programming Data structures and algorithms using Python (PDSA) (Diploma in Programming)", "Database management system (DBMS) (Diploma in Programming)", "Modern Application development - 1 (Diploma in programming)", "Programming concepts using Java (Diploma in programming)", "Machine Learning Techniques (DS Diploma)", "Machine Learning Practice (DS Diploma)", "Business Analytics (DS Diploma)","Tools in Data Science (DS Diploma)", "System commands (Diploma in programming)", "Application Development - 2 (Diploma in programming)"]
    degree_subjects = []

    selected_level = st.selectbox("Please select a Level",level)

    if(selected_level == "Foundational"):
        selected_subject = st.selectbox("Please select a Subject",foundational_subjects)
        foundational(selected_subject)
    elif(selected_level == "Diploma"):
        selected_subject = st.selectbox("Please select a Subject",diploma_subjects)
        diploma(selected_subject)
    


if __name__ == "__main__":
    main()
