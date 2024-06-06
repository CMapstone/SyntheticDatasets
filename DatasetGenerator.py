def DatasetgeneratorF(GeneticScenario,RCCad,NS,R,NF,numCF,minus,overprob,underprob,control_ln,case_ln):  
    #First create a dataset of 0s with NS rows and NF columns
    
    one_to_one=0.52381 
    one_to_zero=1-one_to_one
    zero_initially=1-R
    zero_to_one=one_to_zero*R/(1-R) #check this
    zero_to_zero=1-zero_to_one
    print(zero_to_one)
    cf=[]
    chainlength=NF/(numCF+1)
    for f in range (0,numCF):
        cf.append(int((1+f)*chainlength))
    print(cf)
    dt1cases=[]
    dt2cases=[]
    dt3cases=[]
    dt1controls=[]
    dt2controls=[]
    dt3controls=[]
    Ydata=[]
    for n in range (0,NS):
        Ydata.append(0) 
    for n in range (0,int(NS*RCCad)):
        Ydata[n]=1    
    numcases=0
    numcontrols=0
    if True:         
        while numcases<int(NS*RCCad) or numcontrols<int(NS-NS*RCCad):
            dt1row=[]
            x=random.random()
            if x<zero_initially:
                laststate=0.0
            if x>=zero_initially:
                laststate=1.0
            dt1row.append(laststate)
            for j in range(0,NF-1):
                x=random.random()
                if laststate==0:
                    if x<zero_to_one:
                        currentstate=1.0
                    else:
                        currentstate=0.0
                if laststate==1:
                    if x<one_to_one:
                        currentstate=1.0
                    else:
                        currentstate=0.0
                dt1row.append(currentstate)
                laststate=currentstate
            
            for g in range(0,NF):
                if dt1row[g]==0:
                    dt1row[g]=2               
                if dt1row[g]==1:
                    x=random.random()
                    if x<0.404:
                        nv=1
                    if x>=0.404 and x<0.986:
                        nv=3
                    if x>=0.986:
                        nv=4                    
                    startpoint=g
                    fv=1
                    while fv==1:
                        dt1row[startpoint]=nv
                        startpoint=startpoint+1
                        if startpoint>0 and startpoint<NF:
                            fv=dt1row[startpoint]
                        else:
                            fv=2
                    startpoint=g
                    fv=1
                    while fv==1:
                        dt1row[startpoint]=nv
                        startpoint=startpoint-1
                        if startpoint>0 and startpoint<NF:
                            fv=dt1row[startpoint]
                        else:
                            fv=2
                            
            dt2row=[]
            for g in range(0,NF):
                x=random.random()
                if x>minus:
                    dt2row.append(dt1row[g])
                if x<=minus:
                    dt2row.append(dt1row[g]-1)  
                    
            dt3row=[]
            for g in range(0,NF):
                x=random.random()
                if x<overprob:
                    if dt2row[g]<4:
                        dt3row.append(dt2row[g]+1)
                    if dt2row[g]>3:
                        dt3row.append(dt2row[g])
                if x>=overprob and x<(overprob+underprob):
                    if dt2row[g]>0:
                        dt3row.append(dt2row[g]-1)
                    if dt2row[g]<1:
                        dt3row.append(dt2row[g])
                if x>=(overprob+underprob):
                    dt3row.append(dt2row[g])
             
            cfrow=[]
            cfbinrow=[]
            for b in range(0,numCF):
                cfrow.append(dt3row[cf[b]])
                if dt3row[cf[b]]==2:
                    cfbinrow.append(0)
                if dt3row[cf[b]]!=2:
                    cfbinrow.append(1)
            Yval=0
            if GeneticScenario=='A':
                score1=0
                for j in range(0,int(numCF)):
                    score1=score1+cfbinrow[j]
                if score1>0:
                    Yval=1
            if GeneticScenario=='B':
                score1=0
                for j in range(0,int(numCF/2)):
                    score1=score1+cfbinrow[j]*cfbinrow[j+int(numCF/2)]
                if score1>0:
                    Yval=1
            if GeneticScenario=='C':
                score1=0
                for j in range(0,int(numCF/2)):
                    score1=score1+cfbinrow[j]
                score2=0
                for j in range(int(numCF/2),numCF):
                    score2=score2+cfbinrow[j]
                if score1>0 and score2>0:
                    Yval=1
            if GeneticScenario=='E':
                score1=0
                for j in range(0,int(numCF)):
                    score1=score1+cfbinrow[j]
                score2=0
                for j in range(0,int(numCF/2)):
                    score2=score2+cfbinrow[j]*cfbinrow[j+int(numCF/2)]
                if score1>=3:
                    Yval=1
                if score2>0:
                    Yval=1
            if GeneticScenario=='D':
                score1=0
                for j in range(0,int(numCF/2)):
                    if cfrow[j]<2:
                        score1=score1+1
                for j in range(int(numCF/2),numCF):
                    if cfrow[j]>2:
                        score1=score1+1       
                if score1>0:
                    Yval=1

            x=random.random()
            if Yval==0:
                finalYval=0
                if x<control_ln:
                    finalYval=1
            if Yval==1:
                finalYval=1
                if x<case_ln:
                    finalYval=0

            for g in range(0,NF):
                if dt1row[g]==2:
                    dt1row[g]=-2 
            for g in range(0,NF):
                if dt2row[g]==2:
                    dt2row[g]=-2 
            for g in range(0,NF):
                if dt3row[g]==2:
                    dt3row[g]=-2 
    
            #if final label is positive add one to positive count, if final label is negative, add one to negative count
            if finalYval==0:
                numcontrols+=1
                if numcontrols<=int(NS-NS*RCCad):
                    dt1controls.append(dt1row)
                    dt2controls.append(dt2row)
                    dt3controls.append(dt3row)
            if finalYval==1:
                numcases+=1
                if numcases<=int(NS*RCCad):
                    dt1cases.append(dt1row)
                    dt2cases.append(dt2row)
                    dt3cases.append(dt3row)

    dt1controls=np.array(dt1controls)
    dt2controls=np.array(dt2controls)
    dt3controls=np.array(dt3controls)
    dt1cases=np.array(dt1cases)
    dt2cases=np.array(dt2cases)
    dt3cases=np.array(dt3cases)
    Xdt1=np.concatenate((dt1cases,dt1controls))
    Xdt2=np.concatenate((dt2cases,dt2controls))
    Xdt3=np.concatenate((dt3cases,dt3controls))
    return Xdt1,Xdt2,Xdt3, Ydata