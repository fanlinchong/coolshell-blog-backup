from bs4 import BeautifulSoup
import requests, json, os, subprocess

file_path = 'articles.json'

def load_articles():
	home_page_url = 'https://coolshell.cn'
	print("home page url: %s" % home_page_url)
	data = requests.get(home_page_url)
	soup = BeautifulSoup(data.text, 'html.parser')

	# 底部分页部分的最后一项
	last_page_link = soup.find("a", class_="last")
	# 最大的页数
	# max_page_num = 1;
	max_page_num = int(last_page_link.get('href').split('/')[-1])

	print("Total pages: %d" % (max_page_num))

	page_base_url = home_page_url + '/page/'
	article_infos = []
	# 循环获取每页中的文档链接
	for page_num in range(1, max_page_num + 1):
		page_url = page_base_url + str(page_num)
		print('[%d] url: %s' % (page_num, page_url))
		page_data = requests.get(page_base_url + str(page_num))
		page_soup = BeautifulSoup(page_data.text, 'html.parser')
		# 提取每页中的 h2 标签
		h2_tags = page_soup.find_all('h2')
		for h2_tag in h2_tags:
			# 筛选出是真实文章的链接
			a_tag = h2_tag.find('a', rel="bookmark")
			if a_tag:
				article_info = {'url': a_tag.get('href'), 'title': a_tag.text}
				article_infos.append(article_info)
				print('\t' + article_info['url'] + '\t\t' + article_info['title'])
	return article_infos
			

# 保存文章信息到文件
def save_article_infos(article_infos):
	with open(file_path, 'a', encoding='utf-8') as f:
		json.dump(article_infos, f, indent=4, ensure_ascii=False)
	

def download_articles(article_infos):
	article_save_path = os.path.abspath(os.path.dirname(__file__)) + '/articles/'
	print('Article archive path: %s' % article_save_path)

	for index, article_info in enumerate(article_infos):
		article_url = article_info['url']
		article_id = article_url.split('/')[-1].split('.')[0]
		new_file_name = article_id + '_' + article_info['title'].replace(' ', '').replace('/', '__').replace('(', '（').replace(')', '）') + '.html'
		new_file_path = article_save_path + new_file_name
		print('[%s][%s - %s] downloading...' % (index, article_id, article_info['title']))
		if os.path.exists(new_file_path) and os.stat(new_file_path).st_size > 0:
			print('existed.')
		else:
			download_cmd = 'docker run singlefile ' + article_url + ' > ' + new_file_path
			subprocess.run(download_cmd, shell=True)
			print('completed.')



if os.path.exists(file_path) and os.stat(file_path).st_size > 0:
	with open(file_path, encoding='utf-8') as f:
		article_infos = json.load(f)
		print('The total number of articles is: %d' % len(article_infos))
		download_articles(article_infos)
else:
	article_infos = load_articles()
	print('The total number of articles is: %d' % len(article_infos))
	save_article_infos(article_infos)
	download_articles(article_infos)

