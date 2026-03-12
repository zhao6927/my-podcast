import os
import time
from feedgen.feed import FeedGenerator

# --- 配置 ---
# 你的 GitHub Pages 基础地址
BASE_URL = "https://zhao6927.github.io/my-podcast/" 
# 支持的音频后缀，转为小写匹配更稳健
AUDIO_EXTENSIONS = ('.mp3', '.m4a', '.wav', '.aac')
RSS_FILENAME = "podcast.xml"

def generate_rss():
    fg = FeedGenerator()
    fg.load_extension('podcast')
    
    # 播客整体信息
    fg.title('我的 GitHub 播客库')
    fg.description('通过 GitHub Actions 自动更新的音频订阅源')
    fg.link(href=BASE_URL, rel='alternate')
    fg.language('zh-CN')

    # 扫描当前目录下所有音频文件
    files = [f for f in os.listdir('.') if f.lower().endswith(AUDIO_EXTENSIONS)]
    # 按文件最后修改时间排序（新的在前）
    files.sort(key=lambda x: os.path.getmtime(x), reverse=True)

    for filename in files:
        fe = fg.add_entry()
        # 使用文件名作为单集标题
        fe.title(filename.rsplit('.', 1)[0]) 
        
        # 拼接文件的完整 URL 地址
        # 注意：文件名若包含空格或特殊字符，URL 需要处理，脚本会自动处理基础连接
        file_url = f"{BASE_URL}{filename}".replace(" ", "%20")
        
        # 媒体文件三要素：URL, 文件大小, MIME类型
        file_size = os.path.getsize(filename)
        fe.enclosure(file_url, str(file_size), 'audio/mpeg')
        fe.guid(file_url)
        
        # 设置发布时间为文件修改时间
        file_mtime = time.gmtime(os.path.getmtime(filename))
        fe.pubDate(time.strftime('%a, %d %b %Y %H:%M:%S +0000', file_mtime))

    # 生成并写入文件
    fg.rss_file(RSS_FILENAME)
    print(f"成功生成 {RSS_FILENAME}，包含 {len(files)} 个音频。")

if __name__ == "__main__":
    generate_rss()
