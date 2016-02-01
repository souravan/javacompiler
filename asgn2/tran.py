#!/usr/bin/python

import sys
class instruction(object):
    def convert(self, param):
        # print(param)
        if(len(param)==1):
            return 0
        self.lineno=param[0]
        self.op=param[1]
        if (param[1]=="ifgoto"):
            self.jmp=True
            self.cmpl=True
            self.cmpltype=param[2]
            self.src1=param[3]
            self.src2=param[4]
            self.jlno=param[5]
            basicblock.append(int(self.lineno))
            marker.append(int(self.jlno))
        elif (param[1]=="call"):
            basicblock.append(int(self.lineno))
            basicblock.append(int(self.lineno)+1)
            self.func=True
            self.funcname=param[2]
        elif (param[1]=="ret"):
            self.returnc=True
        elif (param[1]=="label"):
            # basicblock.append(int(self.lineno))
            marker.append(int(self.lineno))
            self.lbl=True
            self.lblname=param[2]
        elif (param[1]=="print"):
            self.printc=True
            self.src1=param[2]
        elif (param[1]=="="):
            self.dst=param[2]
            self.src1=param[3]
            variables.append(param[2])
            variables.append(param[3])
        else:
            self.dst=param[2]
            self.src1=param[3]
            self.src2=param[4]
            variables.append(param[2])
            variables.append(param[3])
            variables.append(param[4])

    def printobj(self):
        print("line no: "+self.lineno)
        print("op: "+self.op)
        print("dst: "+str(self.dst))
        print("src1: "+str(self.src1))
        print("src2: "+str(self.src2))
        print("jmp: "+str(self.jmp))
        print("cmpl: "+str(self.cmpl))
        print("cmpltype: "+str(self.cmpltype))
        print("jlno: "+str(self.jlno))
        print("lbl: "+str(self.lbl))
        print("lblname: "+str(self.lblname))
        print("func: "+str(self.func))
        print("funcname: "+str(self.funcname))
        print("print: "+str(self.printc))
        print("input: "+str(self.inputc))
        print("return: "+str(self.returnc))
        print("\n")

    def __init__(self):
        self.lineno=0
        self.op=None             #operator
        self.dst=None            #destination
        self.src1=None           #source1
        self.src2=None           #source2
        self.jmp=False           #if jump or not
        self.cmpl=False          #if compare or not
        self.cmpltype=None
        self.jlno=0              #line number to jump to
        self.lbl=False           #label of a function
        self.lblname=None        #Name of label
        self.func=False
        self.funcname=None
        self.printc=False        #If we have to print or not(lib func)
        self.inputc=False        #If we have to take input or not(lib func)
        self.returnc=False       #If we have to return or not(lib func)
#
def build_nextusetable():
    #print(type(basicblock[0]))
    # for i in range(1,len(basicblock)):
    #     for j in range(basicblock[i],basicblock[i-1],-1):
    #         print(str(j))
            # continue
    for i in range(1,len(basicblock)):
        newdiction  = {}
        newdiction['1line'] = -1
        for j in range(basicblock[i],basicblock[i-1],-1):
            # print("line no = " + str(j))
            newdiction['1line'] = j
            nextuse.insert(basicblock[i-1],newdiction.copy())
            if(splitins[j-1].dst!=None):
            	if(splitins[j-1].dst in newdiction.keys()):
                	del newdiction[splitins[j-1].dst]
            if(splitins[j-1].src1!= None):
            	if(splitins[j-1].src1.isdigit()==False):
                	newdiction[splitins[j-1].src1]=j
            if(splitins[j-1].src2!= None):
            	if(splitins[j-1].src2.isdigit()==False):
                	newdiction[splitins[j-1].src2]=j

    #             print(splitins[j-1].src1)

def isregassigned(var):
    for i in range(0,6):
        if(regalloc[i]==var):
            return i
    return "-1"

def regname(regno):
    #ebx=1 ,ecx=2, esi=3, edi=4, eax=5, edx=6
    if(regno==0):
        return 'ebx'
    if(regno==1):
        return 'ecx'
    if(regno==2):
        return 'esi'
    if(regno==3):
        return 'edi'
    if(regno==4):
        return 'eax'
    if(regno==5):
        return 'edx'

def getreg(lineno,var):
    if(splitins[lineno].dst!=None):
        if(splitins[lineno].op=="/" or splitins[lineno].op=="%"):
            return None
        else:
            for i in range(6):
                if(regalloc[i]=='-1'):
                    allocatedreg=i
                    regalloc[i]=var
                    return i
            for i in regalloc:
                if i not in nextuse[lineno-1].keys():
                    print( "line no: "+str(lineno)+ "  mov "+str(i)+" %"+str(regname(isregassigned(i))))
                    regtoassign=isregassigned(i)
                    regalloc[regtoassign]=var
                    return regtoassign
            tempvar=regalloc[0]
            tempnextuse=nextuse[lineno-1][tempvar]
            for j in range(1,6):
                i=regalloc[j]
                if(tempnextuse<nextuse[lineno-1][i]):
                    tempvar=i
                    tempnextuse=nextuse[lineno-1][i]
            # print("reg ass " + str(isregassigned(tempvar))+ " at" + regname(isregassigned(tempvar)))
            print("line no: "+str(lineno)+ "  mov "+str(tempvar)+" %"+str(regname(isregassigned(tempvar))))
            regtoassign=isregassigned(i)
            regalloc[regtoassign]=var
            return regtoassign

def convertassem():
    # print splitins
    for i in range(len(splitins)):
        if(splitins[i].op=='+'):
            tmp=isregassigned(splitins[i].src1)
            if(tmp!=-1):
                b=regname(tmp)
            else:
                b=regname(getreg)
            tmp=isregassigned(splitins[i].src2)
            if(tmp!=-1):
                c=regname(tmp)
            else:
                c=regname(getreg)
            tmp=isregassigned(splitins[i].dst)
            if(tmp!=-1):
                a=regname(tmp)
            else:
                a=regname(getreg)
            print ("movl " + str(c)+" "+ str(a))
            print ("addl " + str(b)+" "+ str(a))


variables = []
basicblock=[]
nextuse = []
basicblock.append(0)
marker=[]
regalloc = ['-1']*6
#No Scheme for regalloc
#ebx=1 ,ecx=2, esi=3, edi=4, eax=5, edx=6
i=0
filename = sys.argv[1]
f = open(filename, 'r')
data = f.read()
lines=data.split('\n')
splitins2 = []
for i in lines:
    f=i.split(",")
    splitins2.append(f)
splitins=[]
x=[]
# print(splitins2)
for l in splitins2:
    x=[]
    for i in l:
        i=i.strip(" ")
        x.append(i)
    temp=instruction()
    temp.convert(x)
    if(len(x)!=1):
        splitins.append(temp)
basicblock.append(len(splitins))
# for i in splitins:
#     i.printobj()
unique = set(variables)
variables = list(unique)

print(basicblock)
print(marker)
build_nextusetable()
print("*********************************************************************************")
for i in nextuse:
    print(i)
print("*********************************************************************************")
for i in range(len(nextuse)):
    for j in nextuse[i-1].keys():
        if(j=='1line'):
            continue
        if(isregassigned(j)!='-1'):
            continue
        if(isregassigned(j)=='-1'):
            temp=getreg(i,j)
        print("line no: "+str(i)+"  "+j+"  ::  "+str(temp))
        # print()


convertassem()

#print(splitins)
# for l in splitins:
#     print(l)
#     if(l[1]=='='):
#         print(l[2]+" "+ l[1]+" "+l[3])
#     elif(l[1]=='+' or l[1]== '-' or l[1]=='*' or l[1]=='/' or l[1]=='%'):
#         print(l[2]+ " = "+ l[3]+ l[1] + l[4])
#
# # print(splitins)
# # print(data)
# #w=input().split(",");
# # print(w)
