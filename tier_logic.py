Cutline_point=[0,100,300,500,700,1000,1300,1600,2000,2400,2800,3400,4000,4600,5400,6200,7000,8000,9000,10000,1000000000]
Daily_required=[0,0,10,20,30,40,50,60,80,100,120,140,160,180,210,240,270,300,330,360]
Maximum=[80,100,100,100,100,100,100,100,100,100,120,120,120,120,120,120,150,150,150,150]
Minimum=[0,-25,-25,-25,-50,-50,-50,-75,-75,-75,-100,-100,-100,-150,-150,-150,-200,-200,-200,-300]
Avoid_fall=[True,True,True,True,True,True,True,True,True,True,True,False,False,True,False,False,False,False,False,False]
Tier=['루키','브론즈1','브론즈2','브론즈3','실버1','실버2','실버3','골드1','골드2','골드3','다이아1','다이아2','다이아3','크리스탈1','크리스탈2','크리스탈3','레전드1','레전드2','레전드3','얼티밋']

def update_tier_and_score(rank, rank_point, study_time):
    change = max(Minimum[rank], min(Maximum[rank], (study_time - Daily_required[rank])))
    msg = ""
    if rank_point + change >= Cutline_point[rank+1]:
        rank_point += change
        rank += 1
        msg = f"티어가 상승했습니다: {Tier[rank-1]} -> {Tier[rank]}\n점수가 상승했습니다: {rank_point-change} -> {rank_point} ({change})"
    elif rank_point + change < Cutline_point[rank]:
        if Avoid_fall[rank]:
            change = rank_point - Cutline_point[rank]
            rank_point = Cutline_point[rank]
            msg = f"티어 강등이 방지되었습니다: {Tier[rank]}\n점수가 하락했습니다: {rank_point-change} -> {rank_point} ({change})"
        else:
            rank_point += change
            rank -= 1
            msg = f"티어가 강등되었습니다: {Tier[rank+1]} -> {Tier[rank]}\n점수가 하락했습니다: {rank_point-change} -> {rank_point} ({change})"
    else:
        rank_point += change
        msg = f"점수가 변동되었습니다: {rank_point-change} -> {rank_point} ({change})"
    return rank, rank_point, Tier[rank], msg