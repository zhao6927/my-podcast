import os
import time
from feedgen.feed import FeedGenerator

# --- 自动扫描配置 ---
BASE_URL = "https://zhao6927.github.io/my-podcast/" 
AUDIO_EXTENSIONS = ('.mp3', '.m4a', '.wav', '.aac', '.mp4')
RSS_FILENAME = "podcast.xml"

def generate_rss():
    fg = FeedGenerator()
    fg.load_extension('podcast')
    fg.title('我的私藏音频库')
    fg.description('GitHub 自动化播客源')
    fg.link(href=BASE_URL, rel='alternate')
    fg.language('zh-CN')

    # 扫描策略：同时找根目录和 audio 文件夹
    files_to_process = []
    scan_paths = ['.', 'audio'] 
    
    for path in scan_paths:
        if os.path.exists(path):
            for f in os.listdir(path):
                if f.lower().endswith(AUDIO_EXTENSIONS):
                    full_path = os.path.join(path, f)
                    # 记录文件完整路径和相对于根目录的 URL 路径
                    rel_url = f if path == '.' else f"{path}/{f}"
                    files_to_process.append((full_path, rel_url, f))

    # 按文件修改时间排序
    files_to_process.sort(key=lambda x: os.path.getmtime(x[0]), reverse=True)

    for full_path, rel_url, filename in files_to_process:
        fe = fg.add_entry()
        fe.title(filename.rsplit('.', 1)[0]) 
        file_url = f"{BASE_URL}{rel_url}".replace(" ", "%20")
        fe.enclosure(file_url, str(os.path.getsize(full_path)), 'audio/mpeg')
        fe.guid(file_url)
        file_mtime = time.gmtime(os.path.getmtime(full_path))
        fe.pubDate(time.strftime('%a, %d %b %Y %H:%M:%S +0000', file_mtime))

    fg.rss_file(RSS_FILENAME)
    print(f"成功！找到了 {len(files_to_process)} 个音频文件。")

if __name__ == "__main__":
    generate_rss()
