import json

with open('result.json', 'r') as f:
    content = json.load(f)

print(f"获取到{len(content['goods_list'])}个产品")
total_comments = 0
for good, comments in content['goods_list'].items():
    print(f"商品id:{good}有{len(comments)}条评论")
    total_comments += len(comments)

print(f"{total_comments} == {len(content['comment_list'])} ? {total_comments == len(content['comment_list'])}")
# print(content)
