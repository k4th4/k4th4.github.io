import waybackpy
import pandas



def export_html_full(html):
    """exports the email text as a txt file,
    erases the previous version in the txt before exporting,
    for testing"""

    html_head = '<!DOCTYPE html> \n <html> \n <head> \n'
    style = '<link rel=¨stylesheet¨ type=¨text/css¨ href=¨style.css¨>\n'
    end_of_head = '</head>\n<body>\n'
    script = '\n <script src="script.js"> \n </script> \n'
    html_tail = '</body>\n</html>'
    full_text_html = html_head + style + end_of_head + html + script + html_tail
    print(full_text_html)
    with open(f'index2.html',
              mode='w') as html_file:
        html_file.write(full_text_html)

def archive_urls(url_list):
    user_agent = "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Mobile Safari/537.36"  # determined the user-agent.
    archived_urls =[]
    for url in url_list:
        # url =  # determined the URL to be saved.
        wayback = waybackpy.Url(url, user_agent)  # created the waybackpy instance.
        archive = wayback.save()  # saved the link to the internet archive
        print(archive.archive_url)  # printed the URL.
        archived_urls.append(archive.archive_url)

    return archived_urls



if __name__ == "__main__":
    html = "<h1>Hello World</h1> <p>I'm hosted with GitHub Pages.</p>"
    export_html_full(html)



