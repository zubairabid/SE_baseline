def get_simscore(index, text):
    # Gets as input the text returned from ocr module and the index it 
    # Corresponds to. Looks up the database for the correct answer, then
    # Runs the similarity module on them
    
    with open('tmp/correct_'+str(index), 'r') as master:
        answer = master.read()
        return similarity(answer, text)

def similarity(reference, script):
    return 0.6
