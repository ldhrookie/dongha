import math
Time_Stamp=[]
while True:
    Start_hour, Start_min = map(int, input("시작 시간(00:00분): ").split(':'))
    End_hour, End_min = map(int, input("종료 시간(00:00분): ").split(':'))
    if End_hour<Start_hour:
        End_hour+=24
    Tr = 60* (End_hour-Start_hour) + (End_min-Start_min)
    print("실제 시간: "+str(Tr))
    if Tr==0:
        break
    while True:
        Ts = input("체감시간(분): ")
        if Ts.isdigit():
            Ts=int(Ts)
            break
        else:
            print("다시 입력하세요")
    Subject = input("과목 입력(수학, 물리, 화학, 생명, 지구, 정보): ")
    while not (Subject=='수학' or Subject=='물리' or Subject=='화학' or Subject=='생명' or Subject=='지구' or Subject=='정보'):
        print("과목을 다시 입력하세요")
        Subject = input("과목 입력(수학, 물리, 화학, 생명, 지구, 정보): ")
    Ratio = Ts/Tr
    alpha=math.log(40)
    Concentrate_Rate= int(-100/alpha * math.log(Ratio))+60
    if Concentrate_Rate>=40:
        Concentrate_Rate = int(1.5*Concentrate_Rate-20)
    else:
        Concentrate_Rate = int(20+Concentrate_Rate/2)
    Concentrate_Rate= max(0, min(Concentrate_Rate, 100))
    print(str(Concentrate_Rate)+'%')
    Time_Stamp.append((Subject, Concentrate_Rate, Start_hour, End_hour))
print(Time_Stamp)