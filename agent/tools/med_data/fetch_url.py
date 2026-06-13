import asyncio
import sys
import time
from typing import Optional, Dict, Any, Tuple
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright


async def fetch_and_extract_text_from_url(
        url: str,
        use_javascript: bool = False,
        wait_for_selector: Optional[str] = None,
        timeout: int = 30,
        max_text_length: Optional[int] = 10000,
        user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
) -> Tuple[str, Dict[str, Any]]:
    print(f"\n{'=' * 70}")
    print(f"🔍 开始抓取: {url}")
    print(f"📌 使用JS: {use_javascript}, 超时: {timeout}秒")
    print(f"{'=' * 70}\n")

    if not url.startswith(('http://', 'https://')):
        raise ValueError("Invalid URL format. URL must start with http:// or https://")

    metadata = {
        "url": url,
        "use_javascript": use_javascript,
        "status_code": None,
        "content_length": 0,
        "truncated": False,
        "timeout_occurred": False
    }

    extracted_text = ""

    try:
        if use_javascript:
            print("🌐 使用 Playwright (JavaScript渲染模式)")

            try:
                from playwright.async_api import async_playwright
            except ImportError as e:
                raise Exception(
                    "Playwright is not installed. Please run: pip install playwright && playwright install chromium")

            print("🚀 启动浏览器...")
            start_time = time.time()

            async with async_playwright() as p:
                browser = await p.chromium.launch(
                    headless=True,
                    args=['--disable-blink-features=AutomationControlled']
                )
                print(f"  ├─ 浏览器启动成功 (耗时: {time.time() - start_time:.2f}秒)")

                page = await browser.new_page()
                await page.set_extra_http_headers({"User-Agent": user_agent})

                print(f"  ├─ 加载页面 (超时设置: {timeout}秒)...")
                goto_start = time.time()

                try:
                    await page.goto(url, timeout=timeout * 1000, wait_until='domcontentloaded')
                    print(f"  ├─ ✅ 页面加载完成 (耗时: {time.time() - goto_start:.2f}秒)")
                    metadata["status_code"] = 200
                except Exception as goto_error:
                    print(f"  ├─ ⚠️ 页面加载超时 ({timeout}秒): {str(goto_error)[:80]}")
                    metadata["timeout_occurred"] = True
                    metadata["status_code"] = 200
                    print(f"  ├─ 📍 当前页面URL: {page.url}")

                # 等待一下让可能的动态内容开始加载
                await asyncio.sleep(3)

                # 获取并打印完整的 HTML 内容
                print(f"  ├─ 📄 获取页面HTML内容...")
                html_content = await page.content()
                print(f"  ├─ 📊 HTML内容长度: {len(html_content)} 字符")

                # 打印完整 HTML 内容
                print(f"\n{'=' * 70}")
                print(f"📄 完整 HTML 内容:")
                print(f"{'=' * 70}")
                print(html_content)
                print(f"{'=' * 70}\n")

                # 尝试获取渲染后的文本
                print(f"  ├─ 📝 尝试获取渲染后的文本...")
                try:
                    extracted_text = await page.evaluate('''
                        () => {
                            if (document.body && document.body.innerText) {
                                return document.body.innerText;
                            }
                            return '';
                        }
                    ''')
                    print(f"  ├─ ✅ 渲染文本提取完成，长度: {len(extracted_text)} 字符")
                except Exception as e:
                    print(f"  ├─ ⚠️ 渲染文本提取失败: {e}")
                    extracted_text = ""

                # 如果没有获取到，使用 BeautifulSoup 从 HTML 提取
                if not extracted_text or len(extracted_text) < 100:
                    print(f"  ├─ 🔄 使用 BeautifulSoup 从 HTML 提取文本")
                    from bs4 import BeautifulSoup
                    soup = BeautifulSoup(html_content, 'html.parser')
                    for tag in soup(['script', 'style']):
                        tag.decompose()
                    extracted_text = soup.get_text()
                    print(f"  ├─ 📊 BeautifulSoup 提取文本长度: {len(extracted_text)} 字符")

                # 显示预览
                if extracted_text:
                    lines = [l.strip() for l in extracted_text.split('\n') if l.strip()]
                    print(f"  ├─ 👀 内容预览 (前15行):")
                    for line in lines[:15]:
                        preview = line[:100] + '...' if len(line) > 100 else line
                        print(f"  │    {preview}")
                else:
                    print(f"  ├─ ⚠️ 警告: 未提取到任何文本")

                await browser.close()
                print(f"  └─ ✅ 浏览器已关闭 (总耗时: {time.time() - start_time:.2f}秒)")

        else:
            # 非JS模式
            print("🌐 使用 aiohttp + BeautifulSoup (纯HTTP模式)")
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=timeout)) as response:
                    metadata["status_code"] = response.status
                    if response.status != 200:
                        raise Exception(f"HTTP {response.status}")
                    html_content = await response.text()

            # 打印 HTML 内容
            print(f"\n{'=' * 70}")
            print(f"📄 完整 HTML 内容:")
            print(f"{'=' * 70}")
            print(html_content)
            print(f"{'=' * 70}\n")

            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            for tag in soup(['script', 'style']):
                tag.decompose()
            extracted_text = soup.get_text()

    except Exception as e:
        print(f"❌ 异常错误: {type(e).__name__}: {str(e)}")
        import traceback
        print(f"详细堆栈:\n{traceback.format_exc()}")
        if extracted_text:
            print(f"  ├─ 返回已提取的部分内容 ({len(extracted_text)} 字符)")
        else:
            raise Exception(f"URL extraction error: {str(e)}")

    # 清理文本
    print(f"\n{'=' * 70}")
    print(f"🧹 清理文本")
    print(f"{'=' * 70}")

    if extracted_text:
        original_len = len(extracted_text)
        print(f"  ├─ 原始长度: {original_len}")

        # 移除Cookie相关行
        lines = extracted_text.split('\n')
        cleaned_lines = []
        for line in lines:
            line = line.strip()
            if line:
                lower_line = line.lower()
                if len(line) < 60 and (
                        'cookie' in lower_line or 'got it' in lower_line or 'learn more' in lower_line or 'kaggle uses' in lower_line):
                    continue
                cleaned_lines.append(line)

        extracted_text = '\n'.join(cleaned_lines)

        print(f"  ├─ 清理后长度: {len(extracted_text)}")

        if max_text_length and len(extracted_text) > max_text_length:
            extracted_text = extracted_text[:max_text_length] + "\n...(内容已截断)"
            metadata["truncated"] = True
            print(f"  ├─ 截断至: {max_text_length} 字符")

        if extracted_text:
            preview = extracted_text[:500]
            print(f"  └─ 最终预览 (前500字符):\n{preview}...")
    else:
        print(f"  └─ ⚠️ 警告: 没有文本需要清理")

    metadata["extracted_length"] = len(extracted_text)

    if not extracted_text or not extracted_text.strip():
        raise Exception("No text content extracted from the webpage")

    print(f"\n✅ 成功! 最终提取 {len(extracted_text)} 字符")
    return extracted_text, metadata

async def main():
    """测试函数"""
    url = "https://www.kaggle.com/datasets/mohamedabdalkader/egyptian-medical-retinal-images"

    print("\n" + "🎯" * 35)
    print("Kaggle 数据集抓取测试")
    print("🎯" * 35)

    try:
        text, metadata = await fetch_and_extract_text_from_url(
            url=url,
            use_javascript=True,
            timeout=60,  # 增加超时时间
            max_text_length=10000
        )

        print(f"\n{'=' * 70}")
        print(f"✅ 抓取成功!")
        print(f"{'=' * 70}")
        print(f"📊 统计信息:")
        print(f"  - 提取字符数: {len(text)}")
        print(f"  - 是否截断: {metadata['truncated']}")

        print(f"\n📄 提取的内容:")
        print("-" * 70)
        print(text)
        print("-" * 70)

        with open("kaggle_output.txt", "w", encoding="utf-8") as f:
            f.write(text)
        print(f"\n💾 完整内容已保存到: kaggle_output.txt")

    except Exception as e:
        print(f"\n❌ 抓取失败: {e}")





if __name__ == "__main__":
    asyncio.run(main())