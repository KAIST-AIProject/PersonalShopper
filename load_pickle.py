import pickle 

save_path_quality = "Naver_item1_quality.bin"
with open(save_path_quality, 'rb') as quality_file:
    contents = pickle.load(quality_file)
# print(contents)

print(len(contents['리뷰']))

for idx, c in enumerate(contents['리뷰']):
    print(idx)
    print(c)