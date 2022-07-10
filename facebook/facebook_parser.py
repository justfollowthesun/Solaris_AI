from facebook_scraper import get_posts_by_search,get_posts
from tqdm import tqdm
from nlp_functions.text_classificationn import text_tonality

def get_parsed_dict(posts,brand_name):
  posts_with_comments={}
  page_list=[]
  for post in tqdm(posts):
    if post['post_text'] is not None:
      post_text = post['post_text'].lower()
      post_flag = post_text.find(brand_name.lower())>=0
      comments_list_to_check = [comment_['comment_text'].lower() for comment_ in post['comments_full'] if (comment_['comment_text'].lower().find(brand_name.lower())>=0 and not comment_['comment_text'].lower().startswith('https://'))]
      comments_flag = len(comments_list_to_check)>0
      if post_flag or comments_flag:
        posts_with_comments[post['post_id']] = {'post_flag':post_flag,
                                              'comments_flag':comments_flag,
                                              'post_text':post['post_text'],
                                              'comments_text':comments_list_to_check,
                                              'post_ton':None,
                                              'comments_ton':None,
                                              }
        page_list.append(post['page_id'])


  # print('Number of posts found: ',len(posts_with_comments),' out of ',len(set(page_list)),' pages')
  bad_list=[]
  for post_id,post_info in posts_with_comments.items():
      try:
        if post_info['post_flag']:
          # print(text_tonality(post_info['post_text']))
          posts_with_comments[post_id]['post_ton']=text_tonality(post_info['post_text'])
        if post_info['comments_flag']:
          posts_with_comments[post_id]['comments_ton']=[text_tonality(comment_text) for comment_text in post_info['comments_text']]
      except:
        bad_list.append(post_id)
  if len(bad_list)>0:
    for key in bad_list:
      del posts_with_comments[key]
    # print('Removed ',len(bad_list),' spoiled posts')

  return posts_with_comments

def transpose_dict(posts_with_comments):
  pos_post_dict={}
  neg_post_dict={}
  pos_comments_dict={}
  neg_comments_dict={}
  for key,value in posts_with_comments.items():
    if value.get('post_ton') is not None:
      if value['post_ton']>0:
        pos_post_dict[key]=value['post_text']
      elif value['post_ton']<0:
        neg_post_dict[key]=value['post_text']
    if value.get('comments_ton') is not None:
      pos_list=[]
      neg_list=[]
      for n,com_ton in enumerate(value['comments_ton']):
        if com_ton>0:
          pos_list.append(value['comments_text'][n])
        elif com_ton<0:
          neg_list.append(value['comments_text'][n])
      if len(neg_list)>0:
        neg_comments_dict[key]={'comments_texts':neg_list,
                                  'post_text':value['post_text']}
      if len(pos_list)>0:
        pos_comments_dict[key]={'comments_texts':pos_list,
                                  'post_text':value['post_text']}

  return pos_post_dict,neg_post_dict,pos_comments_dict,neg_comments_dict


def parse_facebook(brand_name,cookies_file,mode='by_news',page_list=None):

  if mode == 'by_news':
    posts=get_posts_by_search(word=brand_name,cookies=cookies_file,options={"comments": 50},page_limit=10)
    posts_with_comments = get_parsed_dict(posts,brand_name)
  elif mode == 'by_pages':
    posts_with_comments={}
    for page in page_list:
      posts = get_posts(page,cookies=cookies_file,options={"comments": 50},page_limit=5)
      posts_with_comments.update(get_parsed_dict(posts,brand_name))
  else:
    print("Invalid mode")
    return None

  pos_post_dict,neg_post_dict,pos_comments_dict,neg_comments_dict = transpose_dict(posts_with_comments)

  return pos_post_dict,neg_post_dict,pos_comments_dict,neg_comments_dict
