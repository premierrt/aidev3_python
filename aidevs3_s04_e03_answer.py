from aidevs3_lib_rt import *

if __name__ == "__main__":
    answer_dict = {}
    answer_dict["01"] = "kontakt@softoai.whatever"
    answer_dict["02"] = "https://banan.ag3nts.org/"
    answer_dict["03"] =  "ISO 9001 oraz ISO/IEC 27001"

    print (answer_dict)

    send_answer (answer_dict, "softo")