import os
import re
import pandas as pd
from collections import defaultdict

path = "/home/ranajit/Documents/Production Logs"

c = 0

student_dict = {}
advisor_dict = {}

s_date = []
a_date = []

s_time = []
a_time = []
s_request_id = []
a_request_id = []
s_intervention = []
a_intervention = []
s_action = []
a_action = []
s_editor = []
a_editor = []
s_profile_id = []
a_profile_id = []
s_profile_type = []
a_profile_type = []


s_intervention_with_date = []
a_intervention_with_date = []

for root, dirs, files in os.walk(path):
    if files != []:   
        for file in files:
            with open(os.path.join(root, file), 'r') as f:
                lines = f.readlines()
                for line in lines:
                    line = line.strip()
                    if "tiny_mce_track: " in line:
                        date_string = root.split("/")[-3].split("_")[-2]
                        print(date_string)
                        
                        time_string = line.split(" ")[0]
                        print(time_string)
                        
                        request_match = re.search(r"request_id=(\w+)", line)
                        request_id = request_match.group(1) if request_match else None
                        print(request_id)
                        
                        intervention_match = re.search(r"Intervention:>>\s*(.+?)(?:\s+and|\s*$)", line, re.IGNORECASE)
                        intervention = intervention_match.group(1) if intervention_match else None
                        print(intervention)
                        
                        action_match = re.search(r"action:>>\s*([^,]+)", line, re.IGNORECASE)
                        action = action_match.group(1) if action_match else None
                        print(action)
                        
                        editor_match = re.search(r"editor_id: \s*([^,]+)", line, re.IGNORECASE)
                        editor = editor_match.group(1) if editor_match else None
                        print(editor)
                        
                        profile_id_match = re.search(r"profile_id: \s*([^,]+)", line, re.IGNORECASE)
                        profile_id = profile_id_match.group(1) if profile_id_match else None
                        print(profile_id)
                        
                        profile_type_match = re.search(r"profile_type: \s*([^,]+)", line, re.IGNORECASE)
                        profile_type = profile_type_match.group(1) if profile_type_match else None
                        print(profile_type)
                        
                        if profile_type == "STUDENT":
                            s_date.append(date_string)
                            s_time.append(time_string)
                            s_request_id.append(request_id)
                            s_intervention.append(intervention)
                            s_action.append(action)
                            s_editor.append(editor)
                            s_profile_id.append(profile_id)
                            s_profile_type.append(profile_type)
                            s_intervention_with_date.append((date_string, intervention))
                        elif profile_type == "ADVISOR": 
                            a_date.append(date_string)
                            a_time.append(time_string)
                            a_request_id.append(request_id)
                            a_intervention.append(intervention)
                            a_action.append(action)
                            a_editor.append(editor)
                            a_profile_id.append(profile_id)
                            a_profile_type.append(profile_type)
                            a_intervention_with_date.append((date_string, intervention))

                        # print(c+1)
                        # c+=1
                        
#Count frequency of each intervention
s_intervention_count = {}
for intervention in s_intervention:
    if intervention in s_intervention_count:
        s_intervention_count[intervention] += 1
    else:
        s_intervention_count[intervention] = 1
print("Intervention Count:")
print(s_intervention_count)   

s_intervention_dict = defaultdict(lambda: defaultdict(int))
for date, intervention in s_intervention_with_date:
    s_intervention_dict[date][intervention] += 1

student_inter_count = {date: dict(interventions) for date, interventions in s_intervention_dict.items()}
print("Intervention Count with Date:")
print(student_inter_count)

a_intervention_count = defaultdict(lambda: defaultdict(int))
for date, intervention in a_intervention_with_date:
    a_intervention_count[date][intervention] += 1   
    
advisor_inter_count = {date: dict(interventions) for date, interventions in a_intervention_count.items()}
print("Advisor Intervention Count with Date:")
print(advisor_inter_count)




                        
student_dict = {
    "date": s_date,
    "time": s_time,
    "request_id": s_request_id,
    "intervention": s_intervention,
    "action": s_action,
    "editor": s_editor,
    "profile_id": s_profile_id,
    "profile_type": s_profile_type
}
advisor_dict = {
    "date": a_date,
    "time": a_time,
    "request_id": a_request_id,
    "intervention": a_intervention,
    "action": a_action,
    "editor": a_editor,
    "profile_id": a_profile_id,
    "profile_type": a_profile_type
}
print("Student Dictionary:")
print(student_dict)
print("Advisor Dictionary:")
print(advisor_dict)

# Create DataFrames
student_df = pd.DataFrame(student_dict)
advisor_df = pd.DataFrame(advisor_dict)
# Save DataFrames to CSV files
student_df.to_csv("student_logs.csv", index=False)
advisor_df.to_csv("advisor_logs.csv", index=False)

student_frequency_df = pd.DataFrame.from_dict(student_inter_count, orient='index').fillna(0).astype(int)
student_frequency_df.to_csv("student_intervention_frequency.csv")

advisor_frequency_df = pd.DataFrame.from_dict(advisor_inter_count, orient='index').fillna(0).astype(int)
advisor_frequency_df.to_csv("advisor_intervention_frequency.csv")


            
        
                            