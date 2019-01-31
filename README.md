# Extended Time Calculator

Welcome to the Extended Time Accommodation Calculator.

This is an app for calculating extended time for students with disabilities


There are 4 sections to this README document.
1. Disclaimer
2. Instructions for use
3. Database
4. Tips and contact information for the developer

<h2>1. Disclaimer</h2>
	
This application is not intended to be the one measure used in determining an extended time accommodation for a student with a disability.  

This is simply one piece of data that can support any decision made by the Committee on Special Education.  

Decisions made by the CSE must be made in accordance with relevant laws and regulations and must take into account 
the impact of the diability on the student's ability to complete a test in the expected amount of time. 

Any application, especially this application, can only provide you with a number and a sentence that explains that number. 
Do not base a decision on this number alone. 

	Copyright (C) 2018  John Boniello

    This program comes with ABSOLUTELY NO WARRANTY; for details refer to license file.
    This is free software, and you are welcome to redistribute it
    under certain conditions; refer to license file for more information.

<h2>2. Instructions for Use</h2>

<h3>1. The front page.</h3>  
  The page that is displayed upon opening consists of two name entry fields and six subject fields. 
  The six subject fields are not editable, they will populate automatically. 
  The first field is for NEW entries ONLY.  If you fill this in with a student who has been entered prior the file will not save. 
                
  Do NOT click save until you have entered data on the following tabs and are finished entering data. 
  Please use a naming convention that can be consistent with all students, for example, Fist_L (First name spelled out with a capital letter, followed by the last initial).

The database used looks for the name, so names MUST be unique. If you have two students named John B. use something unique: John_Bo and John_Be for example.

The second field is for students who have been entered prior. 

If you cannot remember which students you have entered in the past you can open the student_names.txt file to check. (names are separated by ;)  

This is NOT where data is ultimately saved, that is done in the TimeAccommodations.db file. (see database section of this file.) Pressing load will load data from the database into memory. The fields will populate using data saved in the database. 

You must enter the student's name the same way each time.  Due to this requirement you may want to come to a naming convention for yourself, for example,all names are First Name_Last Initial (John_B). You must load the name as it is in the database. 

The Save Update button is used after you have loaded information from an existing student and entered new times in the subject pages.When this is complete and you press "Save Updated", the percentages displayed will update.

Save and Save Update should be the LAST buttons pressed. 


<h3>2. Entry tabs</h3>
		
Entry tabs are provided for all academic subjects for which a student with a disability may need extended time.  

Data should be collected during a test and entered here after one or multiple tests. There are four fields for you to enter data: 

Date (this always starts on the day of entry, you can go backrwards if needed)

Name of the test

Expected time: How much time did you allow all students to complete this assignment?

Actual time: How much time did the student in question actually use for the test? 

When data are entered click "Add New".  When you click add new you a line will pop up in the table next to the data entry fields.  
This is a temporary table and does not save.  The data does save however. You CANNOT delete data at this time. 

Please make sure to only press "Add New" when you are sure that the numbers in the entry fields are correct.  
Pressing ENTER or RETURN does NOT allow you to add data.  This is intentional. 

Clicking "Calculate" will populate the box below, which will generate a sentence about the percentage of time and what this data suggests about the extended time needs of the student.  This sentence will automatically populate the appropriate box on the front page.   

All entry pages are the same and behave in the same manner. 

Note: There is a tab for ENL.  This is intended for students with disabilities who are also in need of ENL (or ESL).  These are not accommodations students receive because of their ELL status.  This is an accommodation that is needed due to the impact of the disability on the student's ability to complete tests and tasks in ENL class.  

<h2>3. Database info</h2>

All data is stored in a sqlite database.  You can interact with this database directly to delete records and/or alter records.  

This is NOT recommended unless you are comfortable working with database programs, any changes made to this database directly will affect what happens in app.  

You will need another program to open and view the database.  

There are many opensource projects on the internet that allow you to view and interact with the .db file.  Some options are (in no particular order):
	
1. SQLite Viewer (all online, just drag and drop the file into the browser)
2. DB Browser for SQLite
3. SQLite Studio
	
<h2>4. Tips and Contact information</h2>

1. Collect data over multiple tests before entering into this application. 
	
2. If you want to see the output close the application and re-open after each new student, otherwise the data from the previous student will be inlcuded in this calculation (I'm working on a fix for this).  

If you enter for multiple students without restarting in between the database will populate correctly, but the sentence will be incorrect if you press calculate. 

To contact the developer with comments/questions email johnboniello@gmail.com.

You can view the full source code at https://github.com/johnboniello/extended_time_calculator. Or by clicking on the source code button
