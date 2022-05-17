import numpy as np
import math
import copy
import pandas as pd
import matplotlib.pyplot as plt
#import for writing Imed Report in Excel Sheet
import openpyxl as opxl
import os

"""function for saving data frame"""
def saveDataFrame(dataframes,filepath,names):
    writer = pd.ExcelWriter(filepath, engine='xlsxwriter')
    for df,sname in zip(dataframes,names):
        df.to_excel(writer,sheet_name=sname)   
    writer.save()
	

"""A class for nodes"""
class pframeNode:
    """ this class defines a node for plane frame which has following  attributes 
    x=x  coordinate of node
    y = y coordinate of node
    marker=marker to drawing
    u=global axial displacement dof
    v=global latteral displacement dof
    theta=global rotational dof
    node marks  
    This part is changed to accomodate continuous beam which has no y coordinates
    
    """
    def __init__(self,nodeno,x,marker):
        self.nodeno=nodeno
        self.x=x
        #self.y=y
        self.marker=marker
        self.u=2*(self.nodeno-1)       
        self.theta=2*(self.nodeno-1)+1
    def displayNode(self):
        print("Marker--->{} x={} Vertical dof={} Roation dof={}".format(self.marker,self.x,self.u,self.theta))
"""Auxilary functions for calcualting nodal distance"""
def calculateNoadalDistance(j,k):
    delx=k.x-j.x
    dely=k.y-j.y
    dist=math.sqrt(delx*delx+dely*dely)
    cx=(delx*1.0)/dist
    cy=(dely*1.0)/dist
    result={"dist":dist,"cx":cx,"cy":cy}
    return result
"""Member Load:Class for handling Load Applied directly on Member"""
class memberLoad:
    """
    p=value of loads
    a=application point
    ltype=1,2,3,4...........
    1=concentrated load
    2=concentrated momnet
    3=udl on whole panel
    4=axial load on panel
    a=in fraction of L
    Ra=bending moment at left Counter clockwise poisitive
    Rb=bending moment at right Counter clockwise poisitive
    Ra=vertical Reaction at Left upward positive
    Rb=vertical Reaction at Right upward positive
    Xa=Horizontal Reaction at Left positive ----> positive
    Xb=Horizontal Reaction at Right positive ----> positive
    """
    def __init__(self,p,a,ltype):
        self.p=p
        self.a=a*1.0
        self.ltype=ltype
        self.Ra=0
        self.Ma=0
        self.Rb=0
        self.Mb=0
        self.Xa=0
        self.Xb=0
        s=(4,1)
        self.EndActions=np.zeros(s)
    def calcualteFixedEndAction(self,L):
        a1=self.a*L
        b1=(1-self.a)*L
        p=self.p
        ltype=self.ltype
        if ltype==1:
            self.Ma=-(p*a1*b1*b1)/(L*L)
            self.Mb=(p*a1*a1*b1)/(L*L)
            self.Ra=-((p*b1*b1)/(L*L*L))*(3*a1+b1)
            self.Rb=-((p*a1*a1)/(L*L*L))*(a1+3*b1)
            #self.Xa=0
            #self.Xb=0
        if ltype==2:
            self.Ma=((p*b1)/(L*L))*(2*a1-b1)
            self.Mb=((p*ba1)/(L*L))*(2*b1-a1)
            self.Ra=((6*p*a1*b1)/(L*L*L))
            self.Rb=-((6*p*a1*b1)/(L*L*L))
            #self.Xa=0
            #self.Xb=0
        if ltype==3:
            self.Ma=-(p*L*L)/12.0
            self.Mb=+(p*L*L)/12.0
            self.Ra=-(p*L/2)
            self.Rb=-(p*L/2)
            #self.Xa=0
            #self.Xb=0
        if ltype==4:
            self.Ma=0
            self.Mb=0
            self.Ra=0
            self.Rb=0
            #self.Xa=(-p*b1)/L
            #self.Xb=(-p*a1)/L
            print(self.Xa)
            print(self.Xb)
        self.EndActions[0][0]=self.Ra
        self.EndActions[1][0]=self.Ma
        self.EndActions[2][0]=self.Rb
        self.EndActions[3][0]=self.Mb 
        
    def calculateSFD(self,points):
        n=points.shape[0]
        print(n)        
        s=(n,1)
        L=points[-1]
        svalues=np.zeros(s)
        application_point=L*self.a
        ltype=self.ltype        
        if ltype==1:            
            for i in range(n):
                if (points[i]>=application_point):
                    svalues[i]=self.p    
                    
        if ltype==3:
             for i in range(n):
                if (points[i]>=application_point):
                    svalues[i]=self.p*points[i]
        #print("printing shear force.......................")
        #print(svalues)
        return svalues
    
    def calculateBMD(self,points):
        n=points.shape[0]
        print(n)        
        s=(n,1)
        L=points[-1]
        mvalues=np.zeros(s)
        application_point=L*self.a
        ltype=self.ltype        
        if ltype==1:            
            for i in range(n):
                if (points[i]>=application_point):
                    mvalues[i]=self.p*(points[i]- application_point)
        if ltype==3:
             for i in range(n):
                if (points[i]>=application_point):                                   
                    mvalues[i]=self.p
                    
        if ltype==3:
             for i in range(n):
                if (points[i]>=application_point):
                    load_length=points[i]-application_point                    
                    mvalues[i]=self.p*(load_length*load_length)*0.5
        #print("printing shear force.......................")
        #print(svalues)
        return mvalues           
    def displayEndAction(self):
        #print("Ma={} Ra={} Mb={} Rb={}".format(self.Ma,self.Ra,self.Mb,self.Rb))
        print(self.EndActions)
    def DisplayLoad(self):
        print("Load Value={} Type={} Application point={}".format(self.p,self.ltype,self.a))

        
        
        
"""Class for Beam"""
class pframeMember:    
    """ this class defines a member for plane frame which has following  attributes 
    j=starting node
    k=terminating node
    E=young's modulus
    A=Cross-sectional Area of the member
    L=Length of the member
    I=Moment of Inertia
    Term1=Axial stiffness=EA/L
    Term2=vertical stiffness=12*E*I/L^3
    SMI=Memeber stiffnes matrix along local axis
    node marks   
    this part has been modified for continuous beam analysis.
    Parameter A has been dropped
    Term1 has been dropped as no axial stiffness is required.
    
    """
    def __init__(self,j,k,E,I,mindex):
        self.member_no=int(mindex)
        self.j=j
        self.k=k
        self.calcualteGlobalIndex()
        self.E=E
        #self.A=A
        self.I=I
        result=self.calculateGeometry()
        L=self.L
        #self.Term1=(E*A/L)
        self.Term2=(12.0*E*I)/(L*L*L)
        self.Term3=(6.0*E*I)/(L*L)
        self.Term4=(4.0*E*I)/(L)
        self.Term5=(2.0*E*I)/(L)
        #self.assembleRotationTransformationMatrix()
        self.assembleLocalStiffnessMatrix()
        s=(4,1)
        self.memberEndActions=np.zeros(s)
        self.memberReactions=np.zeros(s)# calcualted member end forces
        self.Loads=[]
        s=(21,3)
        self.BMDMatrix=np.zeros(s)
        
    def calculateGeometry(self):
        """This function hasbeen modified to accomodate beam"""
        #result=self.k.x-self.j.x
        self.L=self.k.x-self.j.x
        self.cx=1
        self.cy=1
    def calcualteGlobalIndex(self):
        j=self.j.nodeno
        k=self.k.nodeno
        self.j1=2*(j-1)
        self.j2=2*(j-1)+1       
        self.k1=2*(k-1)
        self.k2=2*(k-1)+1
        
    def assembleRotationTransformationMatrix(self):
        R1=np.array([[self.cx,self.cy,0],[-self.cy,self.cx,0],[0,0,1]])
        RT=np.transpose(R1)
        Row1=[self.cx,self.cy,0,0,0,0]
        Row2=[-self.cy,self.cx,0,0,0,0]
        Row3=[0,0,1,0,0,0]
        Row4=[0,0,0,self.cx,self.cy,0]
        Row5=[0,0,0,-self.cy,self.cx,0]
        Row6=[0,0,0,0,0,1]
        self.RT=np.array([Row1,Row2,Row3,Row4,Row5,Row6])
        self.RTT=np.transpose(self.RT)
        print(self.RT)
        print(self.RTT)
    def assembleLocalStiffnessMatrix(self):
        Row1=[self.Term2,self.Term3,-self.Term2,self.Term3]
        Row2=[self.Term3,self.Term4,-self.Term3,self.Term5]
        Row3=[-self.Term2,-self.Term3,self.Term2,-self.Term3]
        Row4=[self.Term3,self.Term5,-self.Term3,self.Term4]      
        self.SMI=np.array([Row1,Row2,Row3,Row4])
        """premultyplying member axis stifness matrix by rotation matrix"""
        #sm1=self.RTT@self.SMI  
        #self.SMS=sm1@self.RT
        self.SMS=self.SMI
    def test(self):
        print(self.Term1)
        print(self.Term2)
        print(self.Term3)
        print(self.Term4)
        print(self.Term5)
        print(self.cx)
        print(self.cy)
    def displayMemberStiffnessMatix(self):
        print("displaying member stiffness matrix in local axis.........")
        print(self.SMI)
        print("displaying member stiffness matrix in structural axis.........")
        print(self.SMS)
    def addMemberLoad(self,mload):
        mload.calcualteFixedEndAction(self.L)
        for i in range(4):
            self.memberEndActions[i][0]=self.memberEndActions[i][0]+mload.EndActions[i][0]
        print("Printing member end actions status..................") 
        print(self.memberEndActions)
        self.Loads.append(mload)
    def calcualteBMD(self):
        print("printing member reactons for BMD calcualtion.................")
        print(self.memberReactions)
        x=np.arange(0,1.05,0.05)
        x=x.reshape(x.shape[0],1)
        x=self.L*x
        self.BMDMatrix[:,0]=x[:,0]
        self.BMDMatrix[:,1]=self.BMDMatrix[:,1]+self.memberReactions[0]
        self.BMDMatrix[:,2]=self.BMDMatrix[:,2]+self.memberReactions[1]*-1
        """Adding BMD due to Left END Reactions"""
        self.BMDMatrix[:,2]=self.BMDMatrix[:,2]+self.memberReactions[1]*self.BMDMatrix[:,0]
        for load in self.Loads:
            svalues=load.calculateSFD(self.BMDMatrix[:,0])
            mvalues=load.calculateBMD(self.BMDMatrix[:,0])
            self.BMDMatrix[:,1]=self.BMDMatrix[:,1]+ svalues[:,0]
            self.BMDMatrix[:,2]=self.BMDMatrix[:,2]+ mvalues[:,0]
        #adding End Shearforce and Bending Moment at the end
        self.BMDMatrix[-1,1]=self.BMDMatrix[-1,1]+self.memberReactions[2]
        self.BMDMatrix[-1,2]=self.BMDMatrix[-1,2]+self.memberReactions[3]
        print("printing shear force.......................")
        print(svalues)
        print("printing bending moment values....................")
        print(mvalues)
    def displayBMDMatrix(self):
        print(self.BMDMatrix)
    def plotBMD(self):
        plt.plot(self.BMDMatrix[:,0],self.BMDMatrix[:,2])
        plt.show()
    def buildMemberName(self):
        member_name="member_"+self.j.marker+self.k.marker
        return member_name
"""
Plane Frame Structure  Although named as prframe structure it actually
Handles Continous Beam

"""
class pframeStructure:

    def __init__(self,totalNode):
        self.totalDof=totalNode*2
        s=( self.totalDof, self.totalDof)
        self.SJ=np.zeros(s)
        s2=(self.totalDof,1)
        self.AJ=np.zeros(s2) #joint load vector
        self.AE=np.zeros(s2) #Equivalent Joint Load Vector From Member Load
        self.AC=np.zeros(s2) #Combined Joint Load Vector From Member Load AJ+AC
        self.SC=np.zeros(s2) #Joint Restrined Conditon
        self.Members=[]
        self.Nodes=[]        
        self.Support_Reactions_Global=np.zeros(s2) 
        self.totalNode=totalNode
    def addNodes(self,node):
        self.Nodes.append(node)
        
    def addMember(self,member):
        rows=[member.j1,member.j2,member.k1,member.k2]
        cols=[member.j1,member.j2,member.k1,member.k2]
        self.Members.append(member)
        #self.assembleMemberLoad(member)
        for j in range(4):
            mycol=[]
            c=cols[j]
            for i in range(4):
                r=rows[i]
                self.SJ[r][c]=self.SJ[r][c]+member.SMS[i][j]
                
                #print((i,j))
    def assembleMemberLoad(self,member):
        rows=[member.j1,member.j2,member.k1,member.k2]       
        mload_struc=member.memberEndActions       
        for i in range(4):
            row=rows[i]
            self.AE[row][0]=self.AE[row][0]- mload_struc[i][0]
    def addJointLoad(self,jno,load_value,load_direction):        
        row=2*(jno-1)+load_direction-1
        self.AJ[row][0]=self.AJ[row][0]+load_value
    def defineMemberLoadMatrix(self):
        n=len(self.Members)
        s=(4,n)
        self.MLI=np.zeros(s)
        print(self.MLI)
    def addMemberLoad(self,load,member_index):
        
        member=self.Members[member_index-1]
        load.calcualteFixedEndAction(member.L)
        print("Displaying Memeber Loads End Actions................")
        load.displayEndAction()
        for i in range(4):
            self.MLI[i][member_index-1]=self.MLI[i][member_index-1]+load.EndActions[i][0]
         
        member.addMemberLoad(load)
        load.displayEndAction()
        rows=[member.j1,member.j2,member.k1,member.k2]
        mload_struc=load.EndActions
        for i in range(4):
            row=rows[i]
            self.AE[row][0]=self.AE[row][0]- mload_struc[i][0]
        """  
        for i in range(6):
            member.memberEndActions[i][0]= member.memberEndActions[i][0]+load.EndActions[i][0]
        """
       
        
    def calcualteCombinedLoadVector(self):
        self.AC=self.AJ+self.AE        
        
        """ 
        for j in range(1,7):
             mycol=[]
            for i in range(1,7):
                mycol.append(member.SMS[i][j])
            print(mycol)
         """
    def addSupport(self,jno,suppot_conditions):
        row1=2*(jno-1)
        self.SC[row1][0]= suppot_conditions[0] 
        row2=2*(jno-1)+1
        self.SC[row2][0]= suppot_conditions[1] 
        
    def calcualtePartionedStiffnessMatrix(self):
        dof=list(self.SC)
        fdof=[]
        rdof=[]
        n=len(dof)
        original_index=[]
        for i in range(n):
            original_index.append(i)
            if dof[i]==0:
                fdof.append(i)
                
            else:
                rdof.append(i)
        print(fdof)
        print(rdof)
        re_arrang_index=[]
        
        for x in fdof:
            re_arrang_index.append(x)
        for x in rdof:
            re_arrang_index.append(x)
        print("rearrange index..............................")  
        print(re_arrang_index)
        """Reaaranging Rows"""
        #storing original and reaaranging index
        self.original_index=original_index
        self.re_arrang_index=re_arrang_index
        SJ_sorted=copy.deepcopy(self.SJ)
        AC_sorted=copy.deepcopy(self.AC)
        AJ_row_sorted= SJ_sorted[re_arrang_index,:]
        AJ_col_sorted=AJ_row_sorted[:,re_arrang_index]
        self.AJ_sorted=copy.deepcopy(AJ_col_sorted)
        AC_row_sorted=AC_sorted[re_arrang_index,:]
        self.AC_sorted=copy.deepcopy(AC_row_sorted)
        n2=len(fdof)
        self.SFF=self.AJ_sorted[0:n2,0:n2]
        self.Inv_SFF=np.linalg.inv(self.SFF)
        #self.AFC=AC_row_sorted[0:n2,:]
        self.AFC=self.AC_sorted[0:n2,:]
        m=len(dof)
        self.ARC=self.AC_sorted[n2:m,:]
        self.SRF=self.AJ_sorted[n2:m,0:n2]

    def calcualteDisplacement(self):
        DF=self.Inv_SFF@self.AFC
        s=(self.totalDof,1)
        self.DJ=np.zeros(s)
        n=len(DF)
        k=0
        for i in range(self.totalDof):
            if self.SC[i][0]==0:
                self.DJ[i][0]=DF[k]
                k=k+1
        print("Total Displacement Matrix.................")
        print(self.DJ)
        self.DF=DF
        """  
        print("Displacement in sorted.................")
        print(self.DJ)
        DJ_sorted=copy.deepcopy(self.DJ)
        print("Dispalying the sorting order...........")
        print(self.re_arrang_index)
        DJ_original_index=DJ_sorted[self.re_arrang_index,:]
        print("Displacement in Origial Order.................")
        self.DJ=DJ_original_index  
        print(self.DJ)
        self.DF=DF
        """
    def trasnferSuppotReactionToGlobalNodes(self):
        pass
        
    def calcualteSupportReactions(self):
        self.AR=-self.ARC+self.SRF@self.DF
        print("printing support reactions..............")
        print(self.AR)
        dof=list(self.SC)
        n=len(dof)
        k=0
        for i in range(n):
            if (self.SC[i][0]==1):
                self.Support_Reactions_Global[i][0]=self.AR[k][0]
                k=k+1
        """Partionong Reactions to Moment and shear in Respective Nodes"""
        moment_list=[]
        reaction_list=[]
        for i in range(n):
            if i%2==0:
                reaction_list.append(self.Support_Reactions_Global[i][0])
            else:
                moment_list.append(self.Support_Reactions_Global[i][0])
        self.Nodal_Reaction=reaction_list
        self.Nodal_Moment=moment_list
       
    def claculateMemberDeflectionAndForces2(self,member):
        j=member.j.nodeno
        k=member.k.nodeno        
        mindex=member.member_no-1
        
        print("member no={} j={} k={}".format(mindex+1,j,k))
       
        
        s=(4,1)
        print("printing member end actions...............")
        print(member.memberEndActions)
        member_DJ=np.zeros(s)
       
       # print("starting node={}".format(j))
       # print("Finishing node={}".format(k))
        member_DJ[0][0]=self.DJ[3*(j-1)][0]
        member_DJ[1][0]=self.DJ[3*(j-1)+1][0]
        member_DJ[2][0]=self.DJ[3*(k-1)][0]
        member_DJ[3][0]=self.DJ[3*(k-1)+1][0]
     
        print("Deflection in global axis..........")
        print(member_DJ)
        member_DJ_local_axis=member_DJ
        print("Deflection in local.........")
        print(member_DJ_local_axis)
        member_force_from_deflection=member.SMI@member_DJ_local_axis
        print("Member force due to deflection..............")
        print(member_force_from_deflection)
        
        mli=self.MLI[:,mindex] # will return one one dimensionl array needed to be reshped into 2d vecor form
        mli=mli.reshape(mli.shape[0],1)
        print("Fixed End actions................")
        print(mli)
        total_member_force=mli+member_force_from_deflection
        
        print("total force due to deflection and end action.................")
        print(total_member_force)
        return total_member_force
    def claculateMemberDeflectionAndForces(self,member):
        j=member.j.nodeno
        k=member.k.nodeno        
        mindex=int(member.member_no-1)
        
        print("member no={} j={} k={}".format(mindex+1,j,k))
       
        
        s=(4,1)
        print("printing member end actions...............")
        print(member.memberEndActions)
        member_DJ=np.zeros(s)
       
       # print("starting node={}".format(j))
       # print("Finishing node={}".format(k))
        member_DJ[0][0]=self.DJ[2*(j-1)][0]
        member_DJ[1][0]=self.DJ[2*(j-1)+1][0]
        member_DJ[2][0]=self.DJ[2*(k-1)][0]
        member_DJ[3][0]=self.DJ[2*(k-1)+1][0]     
        print("Deflection in global axis..........")
        print(member_DJ)
        member_DJ_local_axis=member_DJ
        print("Deflection in local.........")
        print(member_DJ_local_axis)
        member_force_from_deflection=member.SMI@member_DJ_local_axis
        print("Member force due to deflection..............")
        print(member_force_from_deflection)
        
        mli=self.MLI[:,mindex] # will return one one dimensionl array needed to be reshped into 2d vecor form
        mli=mli.reshape(mli.shape[0],1)
        print("Fixed End actions................")
        print(mli)
        total_member_force=mli+member_force_from_deflection
        
        print("total force due to deflection and end action.................")
        print(total_member_force)
        return total_member_force
    def calcualteIndividualMemberForce(self,member):
        s=(4,1)
        DJ=np.zeros(s)
        j=member.j
        k=member.k
        
    def calculateMemberEndForces(self):
        n=len(self.Members)
        s=(4,n)
        self.MF=np.zeros(s) # member end force    
        for member in self.Members:
            #j=member.j.nodeno
            #k=member.k.nodeno        
            mindex=member.member_no-1
            #m =member.member_no
            #j=member.j.nodeno
            #k=member.k.nodeno
            #print("member no={} j={} k={}".format(m,j,k))
            
            member_force=self.claculateMemberDeflectionAndForces(member)
            member.memberReactions=member_force
            for j in range(4):
                mindex=member.member_no-1
                self.MF[j][mindex]=member_force[j][0]
                #print(member_force[j][0])
                #print(self.MF[j][mindex])
                
                 
          
        
    def displayJointStiffnessMatrix(self):
        print("Displaying Joint Stiffness Matrix..............")
        print(self.SJ)
        print("Displaying Equivalent Joint Load Matrix..............")
        print(self.AE)
        print("Direct Joint Load Matrix..............")
        print(self.AJ)
        print("Combined Joint Load Matrix..............")
        print(self.AC)
        print("Joint Restrained Conditions.................")
        print(self.SC)
    def displaySortedStiffnessMatrix(self):
        print("Displaying Joint Stiffness Matrix before sorting..............")
        print(self.SJ)
        print("Displaying Joint Stiffness Matrix after sorting..............")
        print(self.AJ_sorted)
        print("Printing SFF.........................")
        print(self.SFF)
        print("Printing Invers SFF.........................")
        print( self.Inv_SFF)
        print("Printing AFC matrix............................")
        print(self.AFC)
        #self.SFF=self.AJ_sorted[0:n2,0:n2]
        #self.Inv_SFF=np.linalg.inv(self.SFF)
        #self.AFC=AC_sorted[0:n2,:]
        #m=len(dof)
        #self.ARC=AC_sorted[n2:m,:]
        #self.SRF=self.AJ_sorted[n2:m,0:n2]
    def displayNodes(self):
        print("displaying nodes........................")
        for node in self.Nodes:
            node.displayNode()
    def disPlayLoadvector(self):
        print("printing joint load..................")
        print(self.AJ)
        print("printing Equivalent member Loads")
        print(self.AE)
        print("printing Total Joiint Actions............")
        print(self.AC)
    def displayMemberForce(self):
        print("printing fixed member actions....................")
        print(self.MLI)
        print("printing member end forces...........")
        print(self.MF)
        
    def processMemberInformation(self):
        for member in self.Members:
            m =member.member_no
            j=member.j.nodeno
            k=member.k.nodeno
            print("member no={} j={} k={}".format(m,j,k))
            
    def dispalyMemberLoadInfo(self):
        for member in self.Members:
            print("printing load informations for member {}".format(member.member_no))
            for load in member.Loads:
                load.DisplayLoad()
        
            
