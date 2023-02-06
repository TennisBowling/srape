import asyncio
import aiohttp
from lxml import html
import ujson

async def fetch_essays(essay_urls):
        print(f'getting {len(essay_urls)} essays')
        async with aiohttp.ClientSession() as session:
            async with session.post('http://127.0.0.1:3000/', json={'requesturls': essay_urls}, timeout=None) as response:
                try:
                    responses = await response.json()
                except Exception as e:
                    print(e)
                    print(response)
                    responses = []
        print(f'got {len(responses)} essays')
        return responses
                

async def fetch_essay(session, url):
    async with session.get(url, headers={'User-Agent':''}, timeout=None) as response:
        return response

async def main():
    """
    sitemap_url = "https://ivypanda.com/essays/sitemap.xml"

    async with aiohttp.ClientSession() as session:
        async with session.get(sitemap_url, headers={'User-Agent':''}, timeout=None) as response:
            sitemap_xml = await response.text()
            tree = html.fromstring(sitemap_xml.encode('utf-8'))
            sitemap_root = tree.xpath(".//loc")
            topics_urls = [url.text for url in sitemap_root if url.text.startswith("https://ivypanda.com/essays/sitemap-pt-post")]
    print(f'there are {len(topics_urls)} topics urls')

    async with aiohttp.ClientSession() as session:

        print(f'getting {len(topics_urls)} topics')
        async with session.post('http://127.0.0.1:3000/', json={'requesturls': topics_urls}) as response:
            responses = await response.json()
        print(f'got {len(responses)} topics')
        documents = [html.fromstring(resp.encode('utf-8')) for resp in responses]

    
    essay_urls = []
    for document in documents:
        for essay_url in document.xpath(".//loc"):
            if 'topic' not in essay_url:
                essay_urls.append(essay_url.text)
    print(f'there are {len(essay_urls)} essay urls')

    with open('essay_urls.json', 'w') as file:
        ujson.dump(essay_urls, file)
        print(f'wrote {len(essay_urls)} essay urls to essay_urls.json')"""
    
    with open('essay_urls.json', 'r') as file:
        essay_urls = ujson.load(file)
        print(f'read {len(essay_urls)} essay urls from essay_urls.json')

    essays_text = await fetch_essays(essay_urls[:len(essay_urls)//40])


    articles = []

    for essay_text in essays_text:
        tree = html.fromstring(essay_text)
        prompt = tree.xpath("//h1/text()")
        completion = tree.xpath("//*[contains(@class,'article__content')]/*[self::h2 or self::h3 or self::p]/text()")
        completionstr = ' '.join(completion)

        article = {
            "prompt": prompt[0] if prompt else "",
            "completion": completionstr
        }
        articles.append(article)

    with open("Essays.json", "w") as file:
        ujson.dump(articles, file)
        print(f'wrote {len(articles)} essays to Essays.json')

async def fetch_topic(session, url):
    async with session.get(url, headers={'User-Agent':''}, timeout=None) as response:
        return response

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()