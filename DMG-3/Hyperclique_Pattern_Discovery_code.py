
from IPython.display import Markdown, display
def printmd(string):
    display(Markdown(string))

printmd('## **Hyperclique Pattern Discovery**')

printmd('### **1. size 1 prevalent item**')

def f1_item():
    pre_it=[item for elem in data for item in elem]
    pre_it=list(set(pre_it))

    pre_items=[]
    for item in pre_it:
        pre_items.append([item])

    #convert item set into frozenset     
    pre_items=list(map(frozenset,pre_items))
    return pre_items

printmd('### **2. support based prunning**')

def support_prunning(pattern, min_sup):
    dic={}
    n=len(data)
    for d in data:
        for p in pattern:
            if p.issubset(d):
                if not p in dic: 
                    dic[p]=1
                else: 
                    dic[p] += 1
                    
    support=[]
    item=[]
    for d in dic:
        dic[d]/=n
        if dic[d] >= min_sup:
            support.append(dic[d])
            item.append(d)
            
    return item,support

printmd('### **3. H-Confidence based prunning**')

def hc_prunning(item_set, sup, min_hc, item1, sup1):
    hconf=[]
    new_item=[]
    new_sup=[]
    for it,sp in zip(item_set, sup):
        item=list(it)
        max_sup=0
        for i in item:
            temp=sup1[item1.index(i)]
            if max_sup<temp:
                max_sup=temp
                
        hc= sp/max_sup
        if hc > min_hc:
            hconf.append(hc)
            new_item.append(it)
            new_sup.append(sp)
            
    return new_item,new_sup,hconf

printmd('### **4. Generate new item set F(k) using F(k-1)**')

def aprioriGen(pattern, size):
    new_p=[]
    n=len(pattern)
    size-=1
    for i in range(n):
        for j in range(i+1,n): 
            p1=list(pattern[i])
            p2= list(pattern[j])
            
            list1=p1[:size-1]
            list2=p2[:size-1]
            list1.sort()
            list2.sort()
            if list1==list2:
                new_p.append(pattern[i] | pattern[j])
    return new_p

printmd('### **5. Hyperclique miner algorithm**')

def Hyperclique_miner(min_hc, min_sp):
    pre_items = f1_item()                                #find size 1 prevalent items
    n = len(pre_items)
    patterns = []
    support = []
    hconf = []
    item, sup = support_prunning(pre_items, min_sp)      #prunning on the basis of support
    zipped_pairs = zip(sup, item)                        #sort items on the basis of support
    item = [j for i,j in sorted(zipped_pairs)]
    sup1=sorted(sup)
    
    item1=[]
    for f_set in item:                                   #frozenset to list
        item1.append(list(f_set)[0])
    k=2
    new_list_length=len(item)
    size=0
    while(k<n and new_list_length>0 ):
        new_p = aprioriGen(item,k)                       # F(k-1) to F(k)
        item, sup = support_prunning(new_p, min_sp)      #prunning on the basis of support
        item, sup, hc = hc_prunning(item, sup, min_hc, item1, sup1) #prunning on the basis of H-confidence
        new_list_length=len(item)
        size+=new_list_length
        if(new_list_length>0):
            patterns.append(item)
            support.append(sup)
            hconf.append(hc)
            k+=1
    
    return patterns,support,hconf,size

printmd('### **6. Read dataset using file handling**')

dataset=[line.rstrip('\n').split(" ") for line in open("Dataset/kosarak.dat")]
for i in range(len(dataset)):
    dataset[i]=[int(i) for i in dataset[i]] 

len(dataset)

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline
from matplotlib import pyplot as plt
from time import time
from random import sample

printmd('### **7. Sample output of first 10000 entries**')

data=dataset[:10000]

patterns,sup,hcon,total_size= Hyperclique_miner(0.2,0.01)

patterns

patterns[0] #size 2 patterns

patterns[1] #size 3 patterns

#support of items
sup

# H-confidence
hcon

# Total number of patterns
total_size

data=dataset

printmd('### **9. Result and analysis**')

hconf=[]
support=[]
length=[]
clock=[]
s=0.01
for i in range(10):
    t1=time()
    patterns,sp,hc,size= Hyperclique_miner(h,s)
    t2=time()-t1
    clock.append(t2)
    hconf.append(h)
    support.append(s)
    length.append(size)
    h+=0.1
    s+=0.02

plt.xticks(hconf)
plt.yticks(length)
plt.xlabel('H-confidence') 
plt.ylabel('Number of patterns')
plt.title('Number of patterns Vs H-confidence')
plt.scatter(hconf,length)
plt.show()

plt.xticks(support)
plt.yticks(length)
plt.xlabel('Support') 
plt.ylabel('Number of patterns')
plt.title('Number of patterns Vs Support')
plt.scatter(support,length)
plt.show()

plt.xlabel('Measure') 
plt.ylabel('Number of patterns')
plt.title('Number of patterns Vs Measure')
plt.scatter(hconf,length,label="H-confidence")
plt.scatter(support,length,label="support")
plt.legend()
plt.show()

plt.xlabel('Measure') 
plt.ylabel('Execution Time in Seconds')
plt.title('Execution Time Vs Measure')
plt.scatter(hconf,clock,label="H-confidence")
plt.scatter(support,clock,label="support")
plt.legend()
plt.show()

plt.xlabel('Execution Time in Seconds') 
plt.ylabel('Number of Patterns')
plt.title('Execution Time Vs Number of Patterns')
plt.scatter(clock,length)
plt.show()