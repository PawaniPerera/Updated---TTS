from mysql.connector import Error
import numpy as np
from dbCreation import db_connection1

from gtts import gTTS
import os
from pydub import AudioSegment
from pydub.playback import play
import numpy as np

connection = db_connection1("localhost", "root", "Sandu@96", "databaseRP2")


mytext = ['සීගිරිය', 'සෑදූ', 'රජතුමා', 'කවුද?']


def mix_list_items_entities(mixedEntities, k):
    entities = []
    for raw in mixedEntities:
        if any(entity[3] > 0 for entity in raw):
            for entity in sorted(raw, key=lambda x: (-x[3], -x[2], int(x[1][x[1].rfind("/") + 2:-1])))[:k]:
                entities.append(entity)
        else:
            raw = sorted(raw, key=lambda x: (-x[2], int(x[1][x[1].rfind("/") + 2:-1])))
            for entity in raw[:k]:
                entities.append(entity)
    return entities


def check_relation_range_type(relation, qType):
    return True
    sparql = SPARQLWrapper(wikidataSPARQL)
    sparql.setQuery("""
               PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
               ASK {<""" + relation + """> rdfs:range <""" + qType + """> }
            """)
    sparql.setReturnFormat(JSON)
    results1 = sparql.query().convert()
    if results1['boolean']:
        return True
    else:
        sparql.setQuery("""
               PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
               ASK {<""" + relation + """> rdfs:range ?range. ?range rdfs:subClassOf ?t. ?t rdfs:subClassOf <""" + qType + """>}
            """)
        sparql.setReturnFormat(JSON)
        results2 = sparql.query().convert()
        if results2['boolean']:
            return True
        else:
            return False
    return results1['boolean']


def check_entities_in_text(text, term):
    doc = []
    if len(doc.ents) > 0:
        for ent in doc.ents:
            if ent.text == term or ent.text in term:
                return True


def basic_entity(combinations, text):
    doc = list(text)
    relations = []
    entities = [x.text for x in doc.ents]
    final_combinations = []
    for token in doc:
        for ent in entities:
            ent = ent.replace("?", "")
            ent = ent.replace(".", "")
            ent = ent.replace("!", "")
            ent = ent.replace("\\", "")
            ent = ent.replace("#", "")
            if token.text in ent:
                ent_list = ent.split(' ')
                next_token = doc[token.i + 1]
                if ent_list.index(token.text) != len(ent_list) - 1 and next_token.dep_ == "compound":
                    isEntity = True
                    break
        if not isEntity:
            relations.append(token.text)
    for comb in combinations:
        if len(relations) == 0:
            if comb.capitalize() not in final_combinations:
                final_combinations.append(comb.capitalize())
        for relation in relations:
            if relation in comb:
                if comb.lower() not in [x.lower() for x in final_combinations]:
                    final_combinations.append(comb.lower())
                    break
        if comb.lower() not in [x.lower() for x in final_combinations]:
            final_combinations.append(comb.capitalize())
    return final_combinations


def levenshtein(seq1, seq2):
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros((size_x, size_y))
    for x in range(size_x):
        matrix[x, 0] = x
    for y in range(size_y):
        matrix[0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x - 1] == seq2[y - 1]:
                matrix[x, y] = min(
                    matrix[x - 1, y] + 1,
                    matrix[x - 1, y - 1],
                    matrix[x, y - 1] + 1
                )
            else:
                matrix[x, y] = min(
                    matrix[x - 1, y] + 1,
                    matrix[x - 1, y - 1] + 1,
                    matrix[x, y - 1] + 1
                )
    print(matrix)
    return matrix[size_x - 1, size_y - 1]


def retrive_answer(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


entities = (" ".join(mytext))

# entities = ['බිතු සිතුවම්', '']


select_details = f""" SELECT description
               FROM segiriya
              WHERE name LIKE '%{entities}'
"""
details = retrive_answer(connection, select_details)
print(details)

myfile = open("myfile11.txt", "w")
for row in details:
    np.savetxt(myfile, row, fmt="%s")
myfile.close()

lan = "si"
output = "myoutput1.mp3"

with open("myfile11.txt") as file:
    tts1 = gTTS(file.read(), lang=lan, slow=False)
tts1.save(output)

sound = AudioSegment.from_file(output)
play(sound)
