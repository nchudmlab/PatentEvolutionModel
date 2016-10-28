import json

def isSame(set1, set2):
    
    len(set1)
    len
    
    if all():
        return True
    else:
        return False


def _test_numOfBucketsAndLinks(buckets_path, links_path):
    
    with open(buckets_path, mode='r') as f:
        buckets=json.loads(f.read())
        
    with open(links_path, mode='r') as f:
        links=json.loads(f.read())
    
    groupSetOfBuckets = set()
    groupSetOfLinks = set()
        
    for date in buckets:
        for group in buckets[date]:
            groupSetOfBuckets.add((date,group))
            
            
    for key in links.keys():
        keySplit = key.split('<=>')
        _srcSplit = keySplit[0].split(' ')
        _dstSplit = keySplit[1].split(' ')
        
        groupSetOfLinks.add((_srcSplit[0],_srcSplit[1]))
        groupSetOfLinks.add((_dstSplit[0],_dstSplit[1]))
        
    
    print('Group number of Buckets: {}'.format(len(groupSetOfLinks)))
    print('Group number of Links: {}'.format(len(groupSetOfLinks)))
    
    
    
def _test_numOfTags(tags_path ):
    
    with open(tags_path, mode='r') as f:
        tags=json.loads(f.read())
        
    groupSetOfTag = set()
    
    for key in tags:
        keySplit = key.split(' ')
        groupSetOfTag.add((keySplit[0],keySplit[1]))
        
    print('Group number of Tags : {}'.format(len(groupSetOfTag)))
    
        

    
if __name__ == '__main__':
#     _test_numOfBucketsAndLinks('H04W/buckets', 'H04W/links')
#     _test_numOfTags('H04W/tags_fix')