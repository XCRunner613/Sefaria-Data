#encoding=utf-8

import django
django.setup()
from sefaria.model import *
from data_utilities.dibur_hamatchil_matcher import *

def get_relevant_DHs(ch_name, file_name):
    #returns those DHs of the lines under ch_name in file_name until the ch after ch_name
    dont_start = True
    relevant_DHs = []
    max_length = 6 #how many words in DH
    with open(file_name) as f:
        for line_n, line in enumerate(f):
            if line_n == 0:
                continue
            if line == "@{}\n".format(ch_name):
                if dont_start:
                    dont_start = False
                    continue
                else:
                    break
            if not dont_start:
                dh = line.split(".")[0].decode('utf-8')
                if len(dh.split()) > max_length:
                    dh = " ".join(line.split()[0:max_length]).decode('utf-8')
                relevant_DHs.append(dh)
    return relevant_DHs

if __name__ == "__main__":
    files = ["nazir.txt", "kiddushin.txt", "sotah.txt", "yevamot.txt"]
    files = ["yevamot.txt"]
    for file_name in files:
        print file_name
        with open(file_name) as f:
            lines = list(f)
            found_amud_count = 0
            prev_last_word = ""
            for line_n, line in enumerate(lines):
                if line_n == 0:
                    continue
                line = line.replace("\n", "")
                if len(line) is 0:
                    continue
                words = line.split()
                curr_last_word = words[-1].replace(":", "").replace(".", "")
                curr_first_word = words[0].replace(":", "").replace(".", "")
                if curr_first_word != prev_last_word and (curr_first_word in prev_last_word or prev_last_word in curr_first_word) and prev_last_word:
                    pass
                if curr_first_word == prev_last_word:
                    found_amud_count += 1
                prev_last_word = curr_last_word
        index = library.get_index(file_name.split(".txt")[0])
        amudim = index.all_section_refs()
        actual_amud_count = len(amudim)
        print found_amud_count
        print actual_amud_count
        for ch_name, alt_struct_ch in enumerate(index.alt_structs["Chapters"]["nodes"]):
            relevant_DHs = get_relevant_DHs(ch_name+1, file_name)
            base_text = TextChunk(Ref(alt_struct_ch["wholeRef"]), lang='he')
            matches = match_ref(base_text, relevant_DHs, lambda x: x.split())
            print matches["matches"]


#Use alt struct of index to get map of each chapter and its dappim and create range variable from first to last amud
#then using marked up file containing chapter info, gather all DHs for that chapter
#and base text chunk's ref will be based on range variable