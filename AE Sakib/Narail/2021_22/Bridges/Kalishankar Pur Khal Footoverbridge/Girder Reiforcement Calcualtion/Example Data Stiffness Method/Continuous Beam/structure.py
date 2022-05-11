"""Plane Frame Structure  Frame Structure.................."""
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
        for i in range(n):
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
        SJ_sorted=copy.deepcopy(self.SJ)
        AC_sorted=copy.deepcopy(self.AC)
        AJ_row_sorted= SJ_sorted[re_arrang_index,:]
        AJ_col_sorted=AJ_row_sorted[:,re_arrang_index]
        self.AJ_sorted=copy.deepcopy(AJ_col_sorted)
        n2=len(fdof)
        self.SFF=self.AJ_sorted[0:n2,0:n2]
        self.Inv_SFF=np.linalg.inv(self.SFF)
        self.AFC=AC_sorted[0:n2,:]
        m=len(dof)
        self.ARC=AC_sorted[n2:m,:]
        self.SRF=self.AJ_sorted[n2:m,0:n2]

    def calcualteDisplacement(self):
        DF=self.Inv_SFF@self.AFC
        s=(self.totalDof,1)
        self.DJ=np.zeros(s)
        n=len(DF)
        for i in range(n):
            self.DJ[i][0]=DF[i]            
        print(self.DJ)
        self.DF=DF
    def calcualteSupportReactions(self):
        self.AR=-self.ARC+self.SRF@self.DF
        print("printing support reactions..............")
        print(self.AR)
    def claculateMemberDeflectionAndForces(self,member):
        j=member.j.nodeno
        k=member.k.nodeno        
        mindex=member.member_no-1
        
        print("member no={} j={} k={}".format(mindex+1,j,k))
       
        
        s=(6,1)
        print("printing member end actions...............")
        print(member.memberEndActions)
        member_DJ=np.zeros(s)
       
       # print("starting node={}".format(j))
       # print("Finishing node={}".format(k))
        member_DJ[0][0]=self.DJ[3*j-3][0]
        member_DJ[1][0]=self.DJ[3*j-2][0]
        member_DJ[2][0]=self.DJ[3*j-1][0]
        member_DJ[3][0]=self.DJ[3*k-3][0]
        member_DJ[4][0]=self.DJ[3*k-2][0]
        member_DJ[5][0]=self.DJ[3*k-1][0]
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
        s=(6,n)
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
            for j in range(6):
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
            