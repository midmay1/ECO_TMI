import os
import utils

searched_cid = 525
name, all_poison_list = utils.load_poison_info(searched_cid)
print(all_poison_list)