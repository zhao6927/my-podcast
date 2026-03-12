import os
import time
from feedgen.feed import FeedGenerator

# --- 核心配置 ---
TARGET_FOLDER = "播客"  # 你的文件夹名称
BASE_URL = "https://zhao6927.github.io/my-podcast/" 
AUDIO_EXTENSIONS = ('.mp3', '.m4a', '.wav', '.aac', '.mp4')
RSS_FILENAME = "podcast.xml"

def generate_rss():
    fg = FeedGenerator()
    fg.load_extension('podcast')
    fg.title('我的私藏音频库')
    fg.description('自动扫描“播客”文件夹生成的订阅源')
    fg.link(href=BASE_URL, rel='alternate')
    fg.language('zh-CN')

    # 检查文件夹是否存在
    if not os.path.exists(TARGET_FOLDER):
        print(f"警告：找不到【{TARGET_FOLDER}】文件夹，请确认文件夹名是否准确。")
        return

    # 扫描指定文件夹下的音频
    files_to_process = []
    for f in os.listdir(TARGET_FOLDER):
        if f.lower().endswith(AUDIO_EXTENSIONS):
            full_path = os.path.join(TARGET_FOLDER, f)
            files_to_process.append((full_path, f))

    # 按修改时间排序（新的在前）
    files_to_process.sort(key=lambda x: os.path.getmtime(x[0]), reverse=True)

    for full_path, filename in files_to_process:
        fe = fg.add_entry()
        fe.title(filename.rsplit('.', 1)[0]) 
        
        # 关键点：链接必须包含文件夹名，且处理中文路径和空格
        from urllib.parse import quote
        encoded_path = quote(f"{TARGET_FOLDER}/{filename}")
        file_url = f"{BASE_URL}{encoded_path}"
        
        fe.enclosure(file_url, str(os.path.getsize(full_path)), 'audio/mpeg')
        fe.guid(file_url)
        
        file_mtime = time.gmtime(os.path.getmtime(full_path))
        fe.pubDate(time.strftime('%a, %d %b %Y %H:%M:%S +0000', file_mtime))

    fg.rss_file(RSS_FILENAME)
    print(f"完成！已从【{TARGET_FOLDER}】中抓取 {len(files_to_process)} 个文件。")

if __name__ == "__main__":
    generate_rss()
