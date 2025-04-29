import numpy as np

#%% Parameters

Task_tau = ("t1", "t2", "t3", "t4", "t5", "t6", "t7")

Task_C = (2, 3, 2, 2, 2, 2, 3)

Task_T = (10, 10, 20, 20, 40, 40, 80)

#%% Schedulability

Schedulability = 0
for i in range(len(Task_tau)):
    Schedulability += Task_C[i]/Task_T[i]
print("The Total Utilization is", Schedulability, ">" if Schedulability>1 else "<=", "1")
if Schedulability > 1:
    print("The Real Time System is not schedulable !")
else:
    print("The Real Time System might be schedulable !")


#%% Schedule

def check_deadline(Ji, Ti, Ci):
    for i in range(0,len(Task_tau)):
        if Task_T[i]*(Ji[i]+1)<=Ti+Ci:
            if Task_tau[i]=="t5":
                print("t5 missed its deadline, but we continue")
                return 1
            else:
                print(f"Deadline miss on task {Task_tau[i]} for job {Ji[i]+1}")
                return 0

def check_available(av_job, Ji, T, a_ij, W_ij):
    for i in range(0,len(Task_tau)):
        if Task_tau[i] not in av_job:
            if Task_T[i]*Ji[i]<=T:
                av_job.append(Task_tau[i])
                a_ij[i].append(T)
        if Task_tau[i] in av_job:
            W_ij[i] += 1
    return 2

#%% Execution

def Computing_job_order():
    R_ij = [[0],
            [0],
            [0],
            [0],
            [0],
            [0],
            [0]]
    
    job_order = []
    
    J = [[11, 12, 13, 14, 15, 16, 17, 18],  # task 1
         [21, 22, 23, 24, 25, 26, 27, 28],  # task 2
         [31, 32, 33, 34],                  # task 3
         [41, 42, 43, 44],                  # task 4
         [51, 52],                          # task 5
         [61, 62],                          # task 6
         [71]]                              # task 7
    
    Ji = [0, 0, 0, 0, 0, 0, 0]              # nb of job done
    
    av_job = ["t1", "t2", "t3", "t4", "t5", "t6", "t7"]     # jobs available at every time t
    
    a_ij = [[0, 0],        # arrival time of every task
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0]]
    
    W_ij = [0, 0, 0, 0, 0, 0, 0]
    
    T = 0
    Ti = 0
    Tii = 0
    Idle = 0
    while T<80:
        print("\nNew iteration")
        print(f"T = {T}")
        if len(av_job)==0:
            print("Idling until a job is ready to be done")
            T += 1
            Ti += 1
            Tii += 1
            Idle += 1
            check_available(av_job, Ji, T, a_ij, W_ij)
            continue
        tau = av_job[np.random.randint(0,len(av_job))]
        av_job.remove(tau)
        
        index_task = Task_tau.index(tau)
        Ci = Task_C[index_task]
        print("Checking deadline")
        if check_deadline(Ji, Ti, Ci)==0:
            break
        job_order.append(J[index_task][Ji[index_task]])
        Ji[index_task] += 1
        R_ij[index_task].append(R_ij[index_task][-1]+Ci-a_ij[index_task][-1] + a_ij[index_task][-2])
        
        Ti += Ci
        for i in range(1,Ci+1):
            T += 1
            print(f"Checking jobs that became available during {tau} at T = {Tii} + {i}")
            check_available(av_job, Ji, T, a_ij, W_ij)
        Tii += Ci
    
    if len(job_order)==29:
        print(f"Total Idle time: {Idle}")
        return job_order, W_ij
    else:
        return 0, 0

#%% Computing different job orders

# Parameters

Different_job_orders = []
Total_waiting_time = []

#%% Single execution

A, B = Computing_job_order()

#%% Multiple execution

for _ in range(20000):
    A, B = Computing_job_order()
    if A!= 0 and A not in Different_job_orders:
        Different_job_orders.append(A)
        Total_waiting_time.append(sum(B))

print(f"\n\nMinimum overall waiting time: {min(Total_waiting_time)}")
Best_schedule = Different_job_orders[Total_waiting_time.index(min(Total_waiting_time))]
for i in range(len(Best_schedule)):
    Best_schedule[i] = f"J_{Best_schedule[i]}"
print(Best_schedule)























