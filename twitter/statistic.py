import json

def count_ton(path):
    with open(path) as f:
        dict_ = json.load(f)
    neg=0
    pos=0
    nt=0
    for v in dict_.values():
      if v['ton']==1:
        pos+=1
      elif v['ton']==0:
        nt+=1
      elif v['ton']==-1:
        neg+=1
    assert pos+nt+neg==len(dict_)
    print(f'Positive entities: {pos}')
    print(f'Neutral entities: {nt}')
    print(f'Negative entities: {neg}')
    return pos,nt,neg