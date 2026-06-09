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
    print(f"📌 使用JS: {use_javascript}")
    print(f"{'=' * 70}\n")

    # 验证URL格式
    if not url.startswith(('http://', 'https://')):
        raise ValueError("Invalid URL format. URL must start with http:// or https://")

    metadata = {
        "url": url,
        "use_javascript": use_javascript,
        "status_code": None,
        "content_length": 0,
        "truncated": False
    }

    extracted_text = ""

    try:
        if use_javascript:
            print("🌐 使用 Playwright (JavaScript渲染模式)")

            # 检查 Playwright 是否安装
            try:
                from playwright.async_api import async_playwright
                print("✅ Playwright 导入成功")
            except ImportError as e:
                print(f"❌ Playwright 未安装: {e}")
                raise Exception(
                    "Playwright is not installed. Please run: pip install playwright && playwright install chromium")

            print("🚀 启动浏览器...")
            start_time = time.time()

            async with async_playwright() as p:
                # 启动浏览器（无头模式）
                browser = await p.chromium.launch(
                    headless=True,
                    args=['--disable-blink-features=AutomationControlled']
                )
                print(f"  ├─ 浏览器启动成功 (耗时: {time.time() - start_time:.2f}秒)")

                # 创建新页面
                page = await browser.new_page()
                print(f"  ├─ 页面创建成功")

                # 设置用户代理
                await page.set_extra_http_headers({"User-Agent": user_agent})

                # 第一步：加载页面框架
                print(f"  ├─ 加载页面框架...")
                goto_start = time.time()
                await page.goto(url, timeout=timeout * 1000, wait_until='domcontentloaded')
                print(f"  ├─ ✅ 页面框架加载完成 (耗时: {time.time() - goto_start:.2f}秒)")
                metadata["status_code"] = 200

                # 获取页面基本信息
                title = await page.title()
                print(f"  ├─ 📄 页面标题: {title[:100]}")

                # 第二步：关键修复 - 等待动态内容加载
                print(f"  ├─ ⏳ 等待动态内容加载...")

                # 策略1: 等待特定关键词出现（根据你的页面内容定制）
                try:
                    await page.wait_for_function(
                        'document.body && document.body.innerText && document.body.innerText.includes("About Dataset")',
                        timeout=15000
                    )
                    print(f"  ├─ ✅ 动态内容已加载（找到关键词 'About Dataset'）")
                except:
                    # 策略2: 如果关键词没找到，等待页面文本足够长
                    print(f"  ├─ ⚠️ 关键词未出现，尝试等待文本增长...")
                    try:
                        await page.wait_for_function(
                            'document.body.innerText.length > 500',
                            timeout=10000
                        )
                        print(f"  ├─ ✅ 页面文本长度足够，内容可能已加载")
                    except:
                        print(f"  ├─ ⚠️ 文本长度未达标，继续尝试...")

                # 可选：再给网络请求一点点时间
                await asyncio.sleep(2)

                # 检查HTML内容长度
                html_content = await page.content()
                print(f"  ├─ 📊 HTML内容长度: {len(html_content)} 字符")
                metadata["content_length"] = len(html_content)

                # 如果用户指定了等待选择器
                if wait_for_selector:
                    print(f"  ├─ ⏳ 等待用户指定元素: {wait_for_selector}")
                    try:
                        await page.wait_for_selector(wait_for_selector, timeout=5000)
                        print(f"  ├─ ✅ 找到元素: {wait_for_selector}")
                    except:
                        print(f"  ├─ ⚠️ 未找到元素: {wait_for_selector}")

                # 第三步：提取文本内容
                print(f"  ├─ 📝 提取文本内容...")
                extract_start = time.time()

                extracted_text = await page.evaluate('''
                    () => {
                        // 移除不需要的元素
                        const removeSelectors = ['script', 'style', 'nav', 'footer', 'header', 'aside'];
                        removeSelectors.forEach(selector => {
                            document.querySelectorAll(selector).forEach(el => el.remove());
                        });

                        // 尝试提取主要内容区域
                        const mainContent = document.querySelector('main') || document.body;
                        let text = mainContent.innerText || mainContent.textContent || '';

                        // 清理多余的空白行
                        text = text.split('\\n').filter(line => line.trim().length > 0).join('\\n');

                        return text;
                    }
                ''')

                print(f"  ├─ ✅ 文本提取成功 (耗时: {time.time() - extract_start:.2f}秒)")
                print(f"  ├─ 📊 原始文本长度: {len(extracted_text)} 字符")

                # 显示文本预览
                if extracted_text:
                    preview = extracted_text[:300].replace('\n', ' ').replace('\r', ' ').strip()
                    print(f"  ├─ 👀 文本预览: {preview[:200]}...")
                else:
                    print(f"  ├─ ⚠️ 警告: 提取的文本为空!")

                    # 调试：尝试获取更详细的信息
                    body_text = await page.evaluate('document.body.innerText')
                    print(f"  ├─ 🔍 Debug - body.innerText长度: {len(body_text)}")
                    if body_text:
                        print(f"  ├─ 🔍 Debug - body预览: {body_text[:200]}")

                # 关闭浏览器
                await browser.close()
                print(f"  └─ ✅ 浏览器已关闭 (总耗时: {time.time() - start_time:.2f}秒)")

        else:
            # 不使用JS的简单HTTP模式
            print("🌐 使用 aiohttp + BeautifulSoup (纯HTTP模式)")
            import aiohttp

            async with aiohttp.ClientSession() as session:
                async with session.get(
                        url,
                        timeout=aiohttp.ClientTimeout(total=timeout),
                        headers={"User-Agent": user_agent}
                ) as response:
                    metadata["status_code"] = response.status
                    print(f"  ├─ HTTP状态码: {metadata['status_code']}")

                    if response.status != 200:
                        raise Exception(f"HTTP {response.status}: Failed to fetch URL")

                    html_content = await response.text()
                    metadata["content_length"] = len(html_content)
                    print(f"  ├─ HTML内容长度: {metadata['content_length']} 字符")

            # 解析HTML
            soup = BeautifulSoup(html_content, 'html.parser')
            title = soup.title.string if soup.title else "无标题"
            print(f"  ├─ 页面标题: {title[:100]}")

            # 移除不需要的标签
            remove_tags = ['script', 'style', 'nav', 'footer', 'header', 'aside', 'meta', 'link']
            for tag in remove_tags:
                for element in soup.find_all(tag):
                    element.decompose()

            # 提取文本
            extracted_text = soup.get_text()
            print(f"  ├─ 提取文本长度: {len(extracted_text)} 字符")

    except asyncio.TimeoutError:
        print(f"❌ 超时错误: {timeout}秒")
        raise TimeoutError(f"Request timeout after {timeout} seconds when fetching URL: {url}")
    except Exception as e:
        print(f"❌ 异常错误: {type(e).__name__}: {str(e)}")
        import traceback
        print(f"详细堆栈:\n{traceback.format_exc()}")
        raise Exception(f"URL extraction error: {str(e)}")

    # 清理文本：去除多余空白和换行
    print(f"\n{'=' * 70}")
    print(f"🧹 清理文本")
    print(f"{'=' * 70}")

    if extracted_text:
        original_len = len(extracted_text)
        print(f"  ├─ 原始长度: {original_len}")

        # 按行清理
        lines = (line.strip() for line in extracted_text.splitlines())
        # 移除空行
        non_empty_lines = [line for line in lines if line]
        extracted_text = ' '.join(non_empty_lines)

        cleaned_len = len(extracted_text)
        print(f"  ├─ 清理后长度: {cleaned_len}")

        # 限制文本长度
        if max_text_length and len(extracted_text) > max_text_length:
            original_length = len(extracted_text)
            extracted_text = extracted_text[:max_text_length] + "...(内容已截断)"
            metadata["truncated"] = True
            metadata["original_length"] = original_length
            print(f"  ├─ 截断至: {max_text_length} 字符")

        # 显示最终预览
        if extracted_text:
            preview = extracted_text[:500].replace('\n', ' ').replace('\r', ' ').strip()
            print(f"  └─ 最终预览: {preview[:300]}...")
    else:
        print(f"  └─ ⚠️ 警告: 没有文本需要清理")

    metadata["extracted_length"] = len(extracted_text)

    if not extracted_text or not extracted_text.strip():
        print(f"\n❌ 最终错误: 没有提取到有效文本")
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
        # 使用 JavaScript 渲染模式
        text, metadata = await fetch_and_extract_text_from_url(
            url=url,
            use_javascript=True,  # Kaggle 必须为 True
            timeout=60,  # 60秒足够
            max_text_length=3000  # 限制输出长度
        )

        print(f"\n{'=' * 70}")
        print(f"✅ 抓取成功!")
        print(f"{'=' * 70}")
        print(f"📊 统计信息:")
        print(f"  - 提取字符数: {len(text)}")
        print(f"  - 是否截断: {metadata['truncated']}")
        print(f"  - 响应状态: {metadata['status_code']}")

        print(f"\n📄 提取的内容预览 (前1000字符):")
        print("-" * 70)
        print(text[:1000])
        print("-" * 70)

        # 保存到文件以便查看完整内容
        with open("kaggle_output.txt", "w", encoding="utf-8") as f:
            f.write(text)
        print(f"\n💾 完整内容已保存到: kaggle_output.txt")

    except Exception as e:
        print(f"\n❌ 抓取失败: {e}")


if __name__ == "__main__":
    asyncio.run(main())