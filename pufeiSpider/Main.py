from pufeiSpider import DownloadPage

url = "http://www.pufei.net/manhua/173/"
save_path = "G:/manhua"

downloadPage = DownloadPage.DownloadPage()
content = downloadPage.get_page_chapter(url, save_path)
