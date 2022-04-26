# GBScheduler

Creating grade beam schedules is tedious and time-consuming. This application takes the report files generated from the popular concrete design software, 'ADAPT PT/RC', and creates an optimized grade beam schedule for your entire project. It can also map your grade beam runs to grade beam geometry imported from Revit and auto add tags (such as GB1, GB2, etc.) to your plan views next to the corresponding grade beam (this feature is WIP).

#### Step 1 - Clone and Install Dependencies:
`git clone https://github.com/connorivy/GBScheduler.git`

** Optional - create virtual environment `py -3.8 -m venv venv` `venv\Scripts\activate.bat` **

`pip install -r requirements.txt`

#### Step 2 - Get Revit GB Geometry:
(this step is setting up the mapping the grade beam runs to actual beams in Revit. However, the mapping logic hasn't been implemented yet, so this step is optional)
Copy the code found in the file "get_gb_geom_from_revit" and paste it into the [Revit Python Shell](https://github.com/architecture-building-systems/revitpythonshell). Make sure to edit the path for the location of the generated file, "revit_output.txt". Save that file in the "helper_files" folder. (The maintainer of RPS is stepping down, it seems that RPS may be moving to [pyRevit](https://github.com/eirannejad/pyRevit))

#### Step 3 - Startup the Program:
Run the program with `python new_gui.py`

![image](https://user-images.githubusercontent.com/43247197/165319253-565592a1-7272-4103-807b-b224001056e7.png)

#### Step 4 - Browse:
Browse to the folder location that contains all of your beam runs. **Important - All beam run folders must have an excel report named "report.xls"** 
The name of each beam run will populate as a button on the right-hand side of the screen.

![image](https://user-images.githubusercontent.com/43247197/165322694-be2b1b55-386f-458a-9c26-f6fbe4bdec4a.png)

Currently the 'Assign Beams to Run' and 'Hide/Unhide folder' buttons don't fully work

#### Step 5 - Create Schedule:
Press the Create Schedule Button.

#### Step 6 - View Beam Runs:
Now you can press the beam run button on the right side of the GUI and view the full schedule as well as the beam callouts for the individual beam run that you've selected. Note - the schedule is currently configured for a specific bar schedule which can be found in the 'helper_files' folder. To update those values for your own schedule, edit the information which is in the schedule_rebar.py file under the functions that end with _shapes.

![image](https://user-images.githubusercontent.com/43247197/165324435-617eed62-cd8d-41c2-8c8b-131fae575bc8.png)

You can view specific information about a beam's scheduled rebar by hovering over the specific rebar in the reinforcement diagram

![image](https://user-images.githubusercontent.com/43247197/165329053-7feb85c6-43ab-43cf-a1e8-7ea5f9283c55.png)

#### Step 7 - Enjoy Your Automatically Generated GB Schedule:
:)



