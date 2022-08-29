
def max_coverage(tim,ttim,file_path):    
    import pandas as pd
    import numpy as np
    coverage =0
    for i in range(len(tim)):
        p, n1, n2=0, 0, 0
    
        if i == 0:
            if pd.Interval(tim[i][0],tim[i][1]).overlaps(pd.Interval(tim[i+1][0],tim[i+1][1])):
                if(tim[i][1]>tim[i+1][1]):
                    tim[i].extend([abs(tim[i][1] - tim[i][0]) - abs(tim[i+1][1] - tim[i+1][0])])
                else: 
                    tim[i].extend([abs(tim[i][1] - tim[i][0]) - abs(tim[i][1] - tim[i+1][0])])
                i = i+1
            else:
                tim[i].extend([abs(tim[i][1] - tim[i][0])])
                i = i+1        

        elif i == len(tim) - 1:
            if tim[i][1] < tim[i-1][1]:
                tim[i].extend([0])
                i = i+1
            elif pd.Interval(tim[i-1][0],tim[i-1][1]).overlaps(pd.Interval(tim[i][0],tim[i][1])):
                tim[i].extend([abs(tim[i][1] - tim[i][0]) - abs(tim[i-1][1] - tim[i][0])])
                i = i+1
            else:
                tim[i].extend([abs(tim[i][1] - tim[i][0])])
                i = i+1

        else:
            if tim[i][1] < tim[i-1][1]:
                tim[i].extend([0])
                i = i+1
                continue
            if tim[i][0] < tim[i-1][1] and tim[i][1] > tim[i-1][1]:
                previous_overlap = tim[i-1][1] - tim[i][0]
                tim[i].extend([abs(tim[i][1] - tim[i][0]) - previous_overlap])
                p = 1
            if tim[i+1][0] < tim[i][1] and tim[i+1][1] > tim[i][1]:
                next_overlap =  tim[i][1] - tim[i+1][0]
                if p == 1 and tim[i+1][0]< tim[i-1][1]:
                    tim[i][2] = tim[i][2] - (tim[i][1] - tim[i-1][1])
                elif p==1 and tim[i+1][0]> tim[i-1][1]:
                    tim[i][2] = tim[i][2] - (tim[i][1] - tim[i+1][0])
                else:
                    tim[i].extend([abs(tim[i][1] - tim[i][0]) - next_overlap])
                n1 = 1
            if tim[i+1][0] < tim[i][1] and tim[i+1][1] < tim[i][1]:
                    if p==1 and tim[i+1][1] < tim[i-1][1]:
                        tim[i][2] = tim[i][2]
                    elif p == 1 and tim[i+1][1] > tim[i-1][1]:
                        next_overlap = tim[i+1][1] - tim[i-1][1]
                        tim[i][2] = tim[i][2] - next_overlap
                    else:
                        tim[i].extend([tim[i][1] - tim[i+1][1] + tim[i+1][0]-tim[i][0]])
                    n2=1
            if p==1 or n1==1 or n2==1:
                i = i+1
            else:
                tim[i].extend([abs(tim[i][1] - tim[i][0])])
                i = i+1

    least_effective_interval = min(tim, key=lambda x: x[2])
    least_effective_coverage = least_effective_interval[2]
    
    ind = np.where(np.diff(np.array(ttim).flatten()) <= 0)[0]
    merged_tim = np.delete(ttim, [ind, ind+1]).reshape(-1, 2)
    for i in range(len(merged_tim)):
        coverage = coverage + merged_tim[i][1] - merged_tim[i][0]
        i = i+1
    output = coverage - least_effective_coverage
    file_name = os.path.basename(file_path).split('.')[0] + ".out"
    with open(file_name, "w") as external_file:
        print(output, file=external_file)
    external_file.close()


import os
path ="C:/Users/Navtej Singh/Desktop/Assignment/Summer Orientation Assignment/Lifeguards/Files"
os.chdir(path)
for file in os.listdir():
    if file.endswith(".in"):
        file_path = f"{path}\{file}"
        tim = []
        ttim =[]
        with open(file_path) as file:
            next(file)
            for line in file:
                (s, e) = line.split()
                tim.append([eval(s),eval(e)])
                ttim.append((eval(s),eval(e)))
            tim.sort()
            ttim.sort()
            max_coverage(tim,ttim,file_path)