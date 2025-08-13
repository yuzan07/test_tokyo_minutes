import streamlit as st
import json
from datetime import datetime

def apply_tokyo_assembly_style():
    st.markdown("""
        <style>
        /* メインカラー: 東京都の青 */
        :root {
            --primary-color: #004098;
            --secondary-color: #e6f0fa;
            --accent-color: #d32f2f;
        }
        
        /* 全体のフォントと背景 */
        html, body, [class*="css"] {
            font-family: "Hiragino Sans", "Meiryo", "Yu Gothic", sans-serif;
            line-height: 1.6;
        }
        
        /* ヘッダー */
        header[data-testid="stHeader"] {
            background-color: var(--primary-color);
            color: white;
        }
        
        /* メインコンテンツ */
        .stApp {
            background-color: #f9f9f9;
        }
        
        /* タイトル */
        h1 {
            color: var(--primary-color);
            border-bottom: 3px solid var(--primary-color);
            padding-bottom: 8px;
            font-weight: 700;
        }
        
        h2 {
            color: var(--primary-color);
            border-left: 5px solid var(--primary-color);
            padding-left: 12px;
            margin-top: 1.5em;
        }
        
        h3 {
            color: var(--primary-color);
            font-weight: 600;
        }
        
        /* サイドバー */
        [data-testid="stSidebar"] {
            background-color: var(--secondary-color);
            border-right: 1px solid #d0d0d0;
        }
        
        [data-testid="stSidebar"] .sidebar-content {
            padding: 1rem;
        }
        
        /* 選択ボックス */
        .stSelectbox label {
            font-weight: bold;
            color: var(--primary-color);
        }
        
        /* ボタン */
        .stButton button {
            background-color: var(--primary-color);
            color: white;
            border-radius: 4px;
            border: none;
            font-weight: 500;
        }
        
        .stButton button:hover {
            background-color: #002f6c;
            color: white;
        }
        
        /* エキスパンダー */
        .stExpander {
            border: 1px solid #d0d0d0;
            border-radius: 4px;
            margin-bottom: 1rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        
        .stExpander .streamlit-expanderHeader {
            background-color: var(--secondary-color);
            color: var(--primary-color);
            font-weight: 600;
            padding: 0.75rem 1rem;
        }
        
        .stExpander .streamlit-expanderContent {
            padding: 1rem;
            background-color: white;
        }
        
        /* 議事録アイテム */
        .meeting-item {
            background-color: white;
            border-left: 4px solid var(--primary-color);
            padding: 1rem;
            margin-bottom: 1rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        
        .meeting-item-head {
            font-weight: bold;
            color: var(--primary-color);
            margin-bottom: 0.5rem;
        }
        
        .meeting-item-body {
            color: #333;
            white-space: pre-wrap;
        }
        
        /* フッター */
        .footer {
            margin-top: 3rem;
            padding: 1rem;
            text-align: center;
            color: #666;
            font-size: 0.9rem;
            border-top: 1px solid #eee;
        }
        
        /* レスポンシブ対応 */
        @media (max-width: 768px) {
            [data-testid="stSidebar"] {
                width: 80% !important;
            }
            
            h1 {
                font-size: 1.5rem;
            }
        }
        
        /* 東京都バッジ */
        .tokyo-badge {
            display: inline-block;
            background-color: var(--primary-color);
            color: white;
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
            font-size: 0.8rem;
            font-weight: bold;
            margin-right: 0.5rem;
        }
        
        /* 検索結果バッジ */
        .result-badge {
            display: inline-block;
            background-color: #4caf50;
            color: white;
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
            font-size: 0.8rem;
            font-weight: bold;
            margin-left: 0.5rem;
        }
        
        /* 検索ハイライト */
        .highlight {
            background-color: #fff59d;
            padding: 0.1em 0.2em;
            border-radius: 0.2em;
            font-weight: bold;
        }
        
        /* スマホ用サイドバー自動閉じ */
        @media (max-width: 768px) {
            .sidebar-collapse {
                display: none;
            }
        }
        </style>
        
        <script>
        // スマホで検索条件が確定したらサイドバーを閉じる
        function closeSidebarOnMobile() {
            if (window.innerWidth <= 768) {
                const sidebar = window.parent.document.querySelector('[data-testid="stSidebar"]');
                if (sidebar) {
                    sidebar.style.display = 'none';
                }
            }
        }
        
        // 検索クエリのハイライト処理
        function highlightText(text, query) {
            if (!query) return text;
            const regex = new RegExp(query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi');
            return text.replace(regex, match => `<span class="highlight">${match}</span>`);
        }
        
        // ページ読み込み時に実行
        document.addEventListener('DOMContentLoaded', function() {
            // スマホ表示時にサイドバーを閉じるトリガーを設定
            const inputs = document.querySelectorAll('input, select');
            inputs.forEach(input => {
                input.addEventListener('change', closeSidebarOnMobile);
            });
        });
        </script>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)

def highlight_search_term(text, query):
    """検索クエリをハイライト表示する"""
    if not query:
        return text
    import re
    highlighted = re.sub(
        f"({re.escape(query)})", 
        r'<span class="highlight">\1</span>', 
        text, 
        flags=re.IGNORECASE
    )
    return highlighted

def search_items(data, search_query):
    results = []
    for meeting in data:
        for category in meeting["categories"]:
            for cluster in category["clusters"]:
                for item in cluster["items"]:
                    if search_query.lower() in item["body"].lower():
                        # ハイライト処理を追加
                        highlighted_body = highlight_search_term(item["body"], search_query)
                        highlighted_head = highlight_search_term(item["head"], search_query)
                        
                        results.append({
                            "meeting_id": meeting["meeting_id"],
                            "date": meeting.get("date", "記載なし"),
                            "category": category["category"],
                            "cluster_keywords": cluster["cluster_keywords"],
                            "item": {
                                "head": highlighted_head,
                                "body": highlighted_body
                            }
                        })
    return results

# データ読み込み
data = []
for n in range(10):
    data += load_data(f"output_test/{2024-n}.json") 

# アプリケーションの設定
st.set_page_config(
    page_title="東京都議会議事録ビューア",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# スタイル適用
apply_tokyo_assembly_style()

# ヘッダー
st.markdown("""
    <div style="display: flex; align-items: center; margin-bottom: 1rem;">
        <img src="https://www.pngitem.com/pimgs/m/224-2247048_-hd-png-download.png" alt="東京都ロゴ" style="height: 90px; margin-right: 15px;">
        <div>
            <h1 style="margin: 0; padding: 0;">東京都議会議事録ビューア</h1>
            <p style="margin: 0; color: #666;">過去10年間の議事録を検索・閲覧できます</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# サイドバー
with st.sidebar:
    st.markdown("""
        <div style="padding: 0.5rem 0; border-bottom: 1px solid #d0d0d0; margin-bottom: 1rem;">
            <h3 style="color: var(--primary-color); margin: 0;">検索条件</h3>
        </div>
    """, unsafe_allow_html=True)
    
    # フリーワード検索
    search_query = st.text_input("フリーワード検索", placeholder="検索したいフレーズを入力", key="search_input")
    
    # 通常のフィルタリング
    meeting_ids = [meeting["meeting_id"] for meeting in data]
    selected_meeting = st.selectbox("会議番号を選択", meeting_ids, key="meeting_select")
    
    meeting_data = next((m for m in data if m["meeting_id"] == selected_meeting), None)
    
    if meeting_data:
        categories = [c["category"] for c in meeting_data["categories"]]
        selected_category = st.selectbox("カテゴリを選択", categories, key="category_select")
        
        category_data = next((c for c in meeting_data["categories"] if c["category"] == selected_category), None)
        
        if category_data:
            cluster_keywords = [cl["cluster_keywords"] for cl in category_data["clusters"]]
            selected_cluster_keywords = st.selectbox("キーワードを選択", cluster_keywords, key="keyword_select")

# メインコンテンツ
if search_query:
    # フリーワード検索結果を表示
    search_results = search_items(data, search_query)
    st.markdown(f"""
        <div style="background-color: var(--secondary-color); padding: 1rem; border-radius: 4px; margin-bottom: 2rem;">
            <h3 style="margin-top: 0;">検索結果</h3>
            <div style="display: grid; grid-template-columns: auto 1fr; gap: 0.5rem 1rem;">
                <div style="font-weight: bold;">検索クエリ:</div>
                <div>"{search_query}"</div>
                <div style="font-weight: bold;">ヒット件数:</div>
                <div>{len(search_results)}件 <span class="result-badge">絞り込み結果</span></div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    if search_results:
        for result in search_results:
            st.markdown(f"""
                <div class="meeting-item">
                    <div style="margin-bottom: 0.5rem;">
                        <span class="tokyo-badge">会議番号</span>
                        <span>{result['meeting_id']}</span>
                        <span class="tokyo-badge">開催日</span>
                        <span>{result['date']}</span>
                    </div>
                    <div style="margin-bottom: 0.5rem;">
                        <span class="tokyo-badge">カテゴリ</span>
                        <span>{result['category']}</span>
                        <span class="tokyo-badge">キーワード</span>
                        <span>{result['cluster_keywords']}</span>
                    </div>
                    <div class="meeting-item-head">📌 {result['item']['head']}</div>
                    <div class="meeting-item-body">{result['item']['body']}</div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("該当する議事内容が見つかりませんでした。")
        
elif meeting_data:
    # 会議基本情報
    st.markdown(f"""
        <div style="background-color: var(--secondary-color); padding: 1rem; border-radius: 4px; margin-bottom: 2rem;">
            <h3 style="margin-top: 0;">会議基本情報</h3>
            <div style="display: grid; grid-template-columns: auto 1fr; gap: 0.5rem 1rem;">
                <div style="font-weight: bold;">会議番号:</div>
                <div>{meeting_data['meeting_id']}</div>
                <div style="font-weight: bold;">開催日:</div>
                <div>{meeting_data.get('date', '記載なし')}</div>
                <div style="font-weight: bold;">カテゴリ数:</div>
                <div>{len(meeting_data['categories'])}件</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    if category_data and selected_cluster_keywords:
        selected_cluster = next(
            (cl for cl in category_data["clusters"] if cl["cluster_keywords"] == selected_cluster_keywords),
            None
        )
        
        if selected_cluster:
            st.markdown(f"""
                <div style="margin-bottom: 1.5rem;">
                    <span class="tokyo-badge">カテゴリ</span>
                    <span style="font-size: 1.2rem; font-weight: bold;">{category_data['category']}</span>
                </div>
                <div style="margin-bottom: 2rem;">
                    <span class="tokyo-badge">キーワード</span>
                    <span style="font-size: 1.2rem; font-weight: bold;">{selected_cluster_keywords}</span>
                    <span class="result-badge">絞り込み結果: {len(selected_cluster['items'])}件</span>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### 議事内容")
            for item in selected_cluster["items"]:
                st.markdown(f"""
                    <div class="meeting-item">
                        <div class="meeting-item-head">📌 {item['head']}</div>
                        <div class="meeting-item-body">{item['body']}</div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.error("選択されたクラスタが見つかりません。")
    else:
        st.info("左のサイドバーからカテゴリとキーワードを選択してください。")
else:
    st.error("データが見つかりませんでした。")

# フッター
st.markdown("""
    <div class="footer">
        <p>© 2025 東京都議会議事録ビューア | このシステムは東京都議会の議事録を閲覧するためのものです</p>
    </div>
""", unsafe_allow_html=True)

# スマホ表示時にサイドバーを自動で閉じるJavaScriptを追加
st.markdown("""
    <script>
    // スマホ表示かどうかを判定
    function isMobile() {
        return window.innerWidth <= 768;
    }
    
    // 検索条件が変更されたらサイドバーを閉じる
    function setupSidebarAutoClose() {
        const inputs = document.querySelectorAll('input, select');
        inputs.forEach(input => {
            input.addEventListener('change', function() {
                if (isMobile()) {
                    const sidebar = window.parent.document.querySelector('[data-testid="stSidebar"]');
                    if (sidebar) {
                        sidebar.style.display = 'none';
                    }
                }
            });
        });
    }
    
    // ページ読み込み時に実行
    document.addEventListener('DOMContentLoaded', function() {
        setupSidebarAutoClose();
    });
    
    // Streamlitのコンポーネントが更新された時にも実行
    const observer = new MutationObserver(function(mutations) {
        setupSidebarAutoClose();
    });
    
    observer.observe(document.body, { childList: true, subtree: true });
    </script>
""", unsafe_allow_html=True)
