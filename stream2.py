import streamlit as st
import json
from datetime import datetime
import re

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
        
        /* コンテンツを中央寄せ */
        .main .block-container {
            max-width: 900px;
            margin: 0 auto;
            padding: 2rem 1rem;
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
            padding-bottom: 8px;
            font-weight: 700;
            text-align: center;
            border-bottom: none !important;
        }
        
        h2 {
            color: var(--primary-color);
            padding-left: 12px;
            margin-top: 1.5em;
            text-align: center;
            border-bottom: none !important;
        }
        
        h3 {
            color: var(--primary-color);
            font-weight: 600;
            text-align: center;
            border-bottom: none !important;
        }
        
        /* 検索条件の見出しから下線を削除 */
        div[data-testid="stMarkdownContainer"] h3 {
            border-bottom: none !important;
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
            font-size: 1.4rem !important; /* ここを追加 */
            padding: 1.4rem 2rem !important; /* ボタン自体も大きめに */
        }
        div[data-testid="stButton"] button[kind="secondary"] {
    background-color: #666 !important;
    color: white !important;
    font-size: 1.2rem !important;   /* 文字サイズ */
    padding: 0.8rem 2.5rem !important; /* 高さと幅 */
    border-radius: 6px !important;
    border: none !important;
    min-height: 50px !important; /* 高さを確保 */
}

div[data-testid="stButton"] button[kind="secondary"]:hover {
    background-color: #555 !important;
}
        /* ボタンの中の文字部分に適用 */
        .stButton button div[data-testid="stMarkdownContainer"] p {
            font-size: 1.4rem !important;
            margin: 0;  /* デフォルト余白を消す */
        }
        
        .stButton button:hover {
            background-color: #002f6c;
            color: white;
        }
        
/* 戻るボタン用ラッパーにスタイルを適用 */
.back-button-wrapper button {
    background-color: #666 !important;
    color: white !important;
    font-size: 1.2rem !important;   /* 文字サイズ */
    padding: 0.6rem 2rem !important; /* 高さと幅 */
    border-radius: 6px !important;
    border: none !important;
}

.back-button-wrapper button:hover {
    background-color: #555 !important;
}
        /* 議事録アイテム */
        .meeting-item {
            background-color: white;
            border-left: 4px solid var(--primary-color);
            padding: 1rem;
            margin-bottom: 1rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            border-radius: 4px;
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
            color: #000 !important;
        }
        
        /* 検索モード切り替えタブ */
        .search-mode-tabs {
            display: flex;
            justify-content: center;
            margin-bottom: 2rem;
            gap: 1rem;
        }
        
        .search-mode-tab {
            padding: 1rem 2rem;
            border: 2px solid #d0d0d0;
            border-radius: 8px;
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            cursor: pointer;
            transition: all 0.3s ease;
            min-width: 180px;
            text-align: center;
            font-weight: 600;
            font-size: 1.1rem;
            color: #666;
        }
        
        .search-mode-tab:hover {
            border-color: var(--primary-color);
            background: linear-gradient(135deg, #e6f0fa 0%, #d4e4f7 100%);
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        
        .search-mode-tab.active {
            color: white !important;
            background: linear-gradient(135deg, var(--primary-color) 0%, #002f6c 100%) !important;
            border: 2px solid var(--primary-color) !important;
            font-weight: 700;
            box-shadow: 0 4px 8px rgba(0,64,152,0.3);
            transform: translateY(-2px);
        }
        
        /* 入力フィールドを中央寄せ */
        .stTextInput > div > div {
            margin: 0 auto;
            max-width: 500px;
        }
        
        .stSelectbox > div > div {
            margin: 0 auto;
            max-width: 500px;
        }
        
        /* 中央寄せ用クラス */
        .center-content {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
        }
        
        /* 検索パネル全体を中央寄せ */
        .search-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            width: 100%;
            max-width: 700px;
            margin: 0 auto;
            padding: 2rem;
        }
        
        /* 戻るボタン用の固定位置コンテナ - 余白削除 */
        .back-button-container {
            position: sticky;
            top: 0;
            z-index: 100;
            background-color: #f9f9f9;
            padding: 10px 0 0 0;
            margin-bottom: 0.5rem;
            border-bottom: 1px solid #eee;
        }
        
        /* 選択ボックスのラベルスタイル改善 */
        .stSelectbox label, .stTextInput label {
            font-size: 1.1rem !important;
            font-weight: 600 !important;
            color: var(--primary-color) !important;
            margin-bottom: 0.5rem !important;
        }
        
/* ▼ ラベル部分（セレクトボックス + テキスト入力） */
div[data-testid="stSelectbox"] label p,
div[data-testid="stTextInput"] label p,
div[data-testid="stSelectbox"] label,
div[data-testid="stTextInput"] label {
    font-size: 1.5rem !important;
    font-weight: 700 !important;
    color: var(--primary-color) !important;
    margin-bottom: 0.8rem !important;
}

/* セレクトボックスの選択中テキスト */
div[data-baseweb="select"] [role="combobox"] > div:first-child {
    font-size: 1.4rem !important;
    font-weight: 600 !important;
    color: #333 !important;
}

/* セレクトボックス全体の横幅 */
div[data-baseweb="select"] {
    width: 100% !important;
    max-width: 800px !important;
}

/* アイコン付きラベル */
.icon-label {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    font-size: 1.6rem;
    font-weight: 700;
}

/* 検索モードアイコン */
.search-icon {
    font-size: 1.8rem;
    margin-right: 0.5rem;
}

/* ヘッダーと検索モードの間の余白を調整 */
.center-content {
    margin-bottom: 1rem !important;
}

/* 空白を削除するためのスタイル */
.stElementContainer[data-testid="stElementContainer"]:empty,
.stMarkdown[data-testid="stMarkdown"]:empty,
.st-emotion-cache-r44huj:empty,
.search-container:empty,
.search-panel:empty {
    display: none !important;
    height: 0 !important;
    padding: 0 !important;
    margin: 0 !important;
}

/* フリーワード検索の入力欄のフォントサイズを大きく */
.stTextInput input {
    font-size: 1.2rem !important;
}

/* 選択ボックスのフォントサイズを大きく */
.stSelectbox select {
    font-size: 1.2rem !important;
}

/* 検索結果のテキストサイズを大きく */
.meeting-item-head {
    font-size: 1.3rem !important;
}

.meeting-item-body {
    font-size: 1.1rem !important;
}

/* 検索ボタンコンテナ */
.search-button-container {
    display: flex;
    justify-content: center;
    margin-top: 2rem;
}

/* 検索モード切り替えボタン - 修正版 */
.search-mode-button {
    font-size: 1.4rem !important;
    font-weight: 700 !important;
    padding: 1.2rem 2rem !important;
    border-radius: 12px !important;
    border: 2px solid var(--primary-color) !important;
    background: white !important;
    color: var(--primary-color) !important;
    transition: all 0.2s ease-in-out;
    width: 100%;
}

.search-mode-button:hover {
    background: var(--secondary-color) !important;
    transform: translateY(-2px);
}

.search-mode-button.active {
    background: var(--primary-color) !important;
    color: white !important;
    box-shadow: 0 4px 10px rgba(0,64,152,0.3);
}

/* 検索モードボタンコンテナを中央寄せ */
.search-mode-buttons {
    display: flex;
    justify-content: center;
    gap: 1rem;
    margin-bottom: 2rem;
    width: 100%;
}

/* 検索パネル内のコンテンツを中央寄せ */
.search-panel-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
}

/* 検索モード選択ガイド */
.search-mode-guide {
    display: grid;
    grid-template-columns: 1fr 1fr;   /* 左右2分割 */
    gap: 4rem;                        /* 真ん中の空白を広げる */
    align-items: center;              /* 各ボックスを縦方向で中央揃え */
    justify-items: center;            /* 各ボックスを横方向で中央揃え */
    margin-top: 3rem;
}

.search-mode-guide-item {
    text-align: center;
    max-width: 240px;
}

.search-mode-guide-icon {
    font-size: 2rem;
    margin-bottom: 0.5rem;
}

.search-mode-guide-title {
    color: var(--primary-color);
    margin-bottom: 0.5rem;
}

.search-mode-guide-desc {
    font-size: 0.9rem;
    color: #666;
}
        </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)

def highlight_search_term(text, query):
    """検索クエリをハイライト表示する"""
    if not query:
        return text
    
    # 複数キーワードの場合に分割
    keywords = query.split()
    highlighted_text = text
    
    for keyword in keywords:
        if keyword.strip():  # 空のキーワードを除外
            import re
            highlighted_text = re.sub(
                f"({re.escape(keyword)})", 
                r'<span class="highlight">\1</span>', 
                highlighted_text, 
                flags=re.IGNORECASE
            )
    
    return highlighted_text

def search_items(data, search_query):
    results = []
    
    # 複数キーワードを分割
    keywords = search_query.split()
    
    for meeting in data:
        for category in meeting["categories"]:
            for cluster in category["clusters"]:
                for item in cluster["items"]:
                    # すべてのキーワードが含まれているかチェック
                    if all(keyword.lower() in item["body"].lower() for keyword in keywords if keyword.strip()):
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

# アプリケーションの設定
st.set_page_config(
    page_title="東京都議会議事録ビューア",
    page_icon="🏛️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# スタイル適用
apply_tokyo_assembly_style()

# セッション状態の初期化
if 'show_search_panel' not in st.session_state:
    st.session_state.show_search_panel = True
if 'search_mode' not in st.session_state:
    st.session_state.search_mode = None  # デフォルトで何も選択されていない状態
if 'search_query' not in st.session_state:
    st.session_state.search_query = None
if 'meeting_data' not in st.session_state:
    st.session_state.meeting_data = None
if 'category_data' not in st.session_state:
    st.session_state.category_data = None
if 'previous_inputs' not in st.session_state:
    st.session_state.previous_inputs = {
        "freeword": "",
        "meeting": "",
        "category": "",
        "keyword": ""
    }
if 'scroll_to_top' not in st.session_state:
    st.session_state.scroll_to_top = False

# 戻るボタン（常に一番上に表示）
if not st.session_state.show_search_panel:
    st.markdown(
        """
        <div class="back-button-container">
            <div class="back-button-wrapper">
        """,
        unsafe_allow_html=True
    )
    if st.button("← 検索条件に戻る", key="back_button", type="secondary"):
        st.session_state.show_search_panel = True
        st.session_state.scroll_to_top = True
        st.rerun()
    st.markdown("</div></div>", unsafe_allow_html=True)

# 検索後に自動でページトップにスクロール
if st.session_state.scroll_to_top:
    st.markdown("""
        <script>
        window.scrollTo(0, 0);
        </script>
    """, unsafe_allow_html=True)
    st.session_state.scroll_to_top = False

# ヘッダー表示（検索パネル表示時のみ）
if st.session_state.show_search_panel:
    st.markdown("""
        <div class="center-content" style="margin-bottom: 1rem;">
            <img src="https://www.pngitem.com/pimgs/m/224-2247048_-hd-png-download.png" alt="東京都ロゴ" style="height: 80px; margin-right: 15px;">
            <div>
                <h1 style="margin: 0; padding: 0;">東京都議会議事録ビューア</h1>
                <p style="margin: 0; color: #666; font-size: 1.2rem;">過去10年間の議事録を検索・閲覧できます</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

# 検索パネル表示
if st.session_state.show_search_panel:
    # 検索コンテナを中央揃え
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="search-panel-content">', unsafe_allow_html=True)
        
        # 検索モード選択の見出しを指定されたものに置き換え
        st.markdown("""
            <div style="text-align: center; margin: 0rem 0 0rem 0;">
                <h2 style="color: var(--primary-color); margin-bottom: 0rem;font-size: 1.7rem;">📑 検索モードを選択してください</h2>
            </div>
        """, unsafe_allow_html=True)
        
        # 検索モード選択ボタン - 中央寄せ
        st.markdown('<div class="search-mode-buttons">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        with col1:
            # キーワード検索ボタン
            if st.button(
                "🏷️ キーワード検索", 
                key="keyword-tab-button", 
                use_container_width=True,
                type="primary" if st.session_state.search_mode == "keyword" else "secondary"
            ):
                st.session_state.search_mode = "keyword"
                st.rerun()

        with col2:
            # フリーワード検索ボタン
            if st.button(
                "🔍 フリーワード検索", 
                key="freeword-tab-button", 
                use_container_width=True,
                type="primary" if st.session_state.search_mode == "freeword" else "secondary"
            ):
                st.session_state.search_mode = "freeword"
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 検索モードが選択されていない場合は案内メッセージを表示
        if st.session_state.search_mode is None:
            st.markdown("""
                <div class="search-mode-guide">
                    <div class="search-mode-guide-item">
                        <div class="search-mode-guide-icon">🏷️</div>
                        <h4 class="search-mode-guide-title">キーワード検索</h4>
                        <p class="search-mode-guide-desc">会議・カテゴリ・キーワードから絞り込んで検索</p>
                    </div>
                    <div class="search-mode-guide-item">
                        <div class="search-mode-guide-icon">🔍</div>
                        <h4 class="search-mode-guide-title">フリーワード検索</h4>
                        <p class="search-mode-guide-desc">自由なキーワードで全文検索</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        # 検索モードが選択されている場合のみ検索フォームを表示
        elif st.session_state.search_mode:
            # 区切り線を追加
            st.markdown('<hr style="border: 1px solid #e0e0e0; margin: 1rem 0; width: 100%;">', unsafe_allow_html=True)
            
            # 選択された検索モードに基づいて表示内容を変更
            if st.session_state.search_mode == "keyword":
                # キーワード検索の見出し
                st.markdown('<div class="icon-label"><span class="search-icon">🏷️</span>キーワード検索</div>', unsafe_allow_html=True)
                
                # データ読み込み
                data = []
                for n in range(10):
                    try:
                        data += load_data(f"output_test/{2024-n}.json")
                    except FileNotFoundError:
                        st.error(f"データファイル output_test/{2024-n}.json が見つかりません")
                        continue
                
                # 会議選択 - 前回の入力を保持
                meeting_options = [meeting["meeting_id"] for meeting in data]
                selected_meeting = st.selectbox(
                    "会議番号選択", 
                    meeting_options, 
                    key="meeting_select",
                    index=meeting_options.index(st.session_state.previous_inputs["meeting"]) 
                    if st.session_state.previous_inputs["meeting"] in meeting_options else 0
                )
                
                # 選択された会議のデータを取得
                meeting_data = next((m for m in data if m["meeting_id"] == selected_meeting), None)
                
                if meeting_data:
                    # カテゴリ選択 - 前回の入力を保持
                    categories = [c["category"] for c in meeting_data["categories"]]
                    selected_category = st.selectbox(
                        "カテゴリ選択", 
                        categories, 
                        key="category_select",
                        index=categories.index(st.session_state.previous_inputs["category"]) 
                        if st.session_state.previous_inputs["category"] in categories else 0
                    )
                    
                    category_data = next((c for c in meeting_data["categories"] if c["category"] == selected_category), None)
                    
                    if category_data:
                        # キーワード選択 - 前回の入力を保持
                        cluster_keywords = [cl["cluster_keywords"] for cl in category_data["clusters"]]
                        selected_cluster_keywords = st.selectbox(
                            "キーワード選択", 
                            cluster_keywords, 
                            key="keyword_select",
                            index=cluster_keywords.index(st.session_state.previous_inputs["keyword"]) 
                            if st.session_state.previous_inputs["keyword"] in cluster_keywords else 0
                        )
                        
                        # 検索実行ボタンを中央に配置
                        st.markdown('<div class="search-button-container">', unsafe_allow_html=True)
                        search_clicked_keyword = st.button("検索実行", type="primary", use_container_width=True, key="keyword_search_button")
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        if search_clicked_keyword and selected_cluster_keywords:
                            # 前回の入力を保存
                            st.session_state.previous_inputs.update({
                                "meeting": selected_meeting,
                                "category": selected_category,
                                "keyword": selected_cluster_keywords
                            })
                            
                            st.session_state.show_search_panel = False
                            st.session_state.search_query = {
                                "meeting": selected_meeting,
                                "category": selected_category,
                                "keyword": selected_cluster_keywords
                            }
                            st.session_state.meeting_data = meeting_data
                            st.session_state.category_data = category_data
                            st.session_state.scroll_to_top = True
                            st.rerun()
            
            elif st.session_state.search_mode == "freeword":
                # フリーワード検索
                st.markdown('<div class="icon-label"><span class="search-icon">🔍</span>フリーワード検索</div>', unsafe_allow_html=True)
                
                # 前回の入力を保持
                freeword_search = st.text_input(
                    "検索キーワード", 
                    placeholder="複数単語の場合、スペースで区切って入力してください", 
                    key="freeword_search",
                    value=st.session_state.previous_inputs["freeword"]
                )
                
                # 検索ボタンを中央に配置
                st.markdown('<div class="search-button-container">', unsafe_allow_html=True)
                search_clicked = st.button("検索実行", type="primary", use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # 検索ボタンが押されたら検索パネルを非表示
                if search_clicked and freeword_search:
                    # 前回の入力を保存
                    st.session_state.previous_inputs["freeword"] = freeword_search
                    
                    st.session_state.show_search_panel = False
                    st.session_state.search_query = freeword_search
                    st.session_state.scroll_to_top = True
                    st.rerun()
                elif search_clicked and not freeword_search:
                    st.warning("検索キーワードを入力してください")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# 検索結果表示
elif not st.session_state.show_search_panel:
    # 検索後に自動でページトップにスクロール
    if st.session_state.scroll_to_top:
        st.markdown("""
            <script>
            window.scrollTo(0, 0);
            </script>
        """, unsafe_allow_html=True)
        st.session_state.scroll_to_top = False
    
    if st.session_state.search_mode == "freeword":
        # フリーワード検索結果を表示
        search_data = []
        for n in range(10):
            try:
                search_data += load_data(f"output_test/{2024-n}.json")
            except FileNotFoundError:
                st.error(f"データファイル output_test/{2024-n}.json が見つかりません")
                continue
        
        search_results = search_items(search_data, st.session_state.search_query)
        
        st.markdown(f"""
        <div style="background-color: var(--secondary-color); padding: 1.6rem; border-radius: 12px; margin-bottom: 2rem; max-width: 700px; margin-left: auto; margin-right: auto;">
            <h3 style="margin-top: 0; text-align: center; color: var(--primary-color); font-size: 1.9rem;">フリーワード検索結果</h3>
            <div style="display: flex; align-items: center; justify-content: center; gap: 1rem; flex-wrap: wrap; font-size: 1.3rem; margin-top: 0.8rem;">
                <div style="font-weight: bold; color: var(--primary-color);">検索クエリ:</div>
                <div style="font-weight: 600;">"{st.session_state.search_query}"</div>
                <span class="result-badge" style="font-size:1.3rem;">検索結果: {len(search_results)}件</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        
        if search_results:
            for result in search_results:
                st.markdown(f"""
                    <div class="meeting-item">
                        <div style="margin-bottom: 0.8rem; text-align: center; font-size: 1rem;">
                            <span class="tokyo-badge">会議番号</span>
                            <span style="font-weight: 600;">{result['meeting_id']}</span>
                            <span class="tokyo-badge">開催日</span>
                            <span style="font-weight: 600;">{result['date']}</span>
                        </div>
                        <div style="margin-bottom: 0.8rem; text-align: center; font-size: 1rem;">
                            <span class="tokyo-badge">カテゴリ</span>
                            <span style="font-weight: 600;">{result['category']}</span>
                            <span class="tokyo-badge">キーワード</span>
                            <span style="font-weight: 600;">{result['cluster_keywords']}</span>
                        </div>
                        <div class="meeting-item-head">📌 {result['item']['head']}</div>
                        <div class="meeting-item-body">{result['item']['body']}</div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("該当する議事内容が見つかりませんでした。")
            
    elif st.session_state.search_mode == "keyword":
        # キーワード検索結果を表示
        meeting_data = st.session_state.meeting_data
        category_data = st.session_state.category_data
        search_query = st.session_state.search_query

        if meeting_data and category_data:
            # selected_cluster をここで定義
            selected_cluster = next(
                (cl for cl in category_data["clusters"] if cl["cluster_keywords"] == search_query["keyword"]),
                None
            )
            
            if selected_cluster:
                result_count = len(selected_cluster["items"])
                st.markdown(f"""<div style="background-color: var(--secondary-color); padding: 1.8rem; border-radius: 12px; margin-bottom: 2rem; max-width: 650px; margin-left: auto; margin-right: auto;"><h3 style="margin-top: 0; color: var(--primary-color); font-size: 1.9rem; text-align: center;">キーワード検索結果</h3><div style="display: flex; flex-direction: column; gap: 1.2rem; font-size: 1.3rem;"><div style="display: flex; align-items: center; gap: 1.5rem;"><span class="tokyo-badge" style="font-size: 1.1rem;">会議番号</span><span style="font-size: 1.3rem; font-weight: 700; color: var(--primary-color);">{meeting_data['meeting_id']}</span><span class="tokyo-badge" style="font-size: 1.1rem;">カテゴリ</span><span style="font-size: 1.2rem; font-weight: 700; color: var(--primary-color);">{search_query['category']}</span></div><div style="display: flex; align-items: center; gap: 0.8rem; flex-wrap: wrap;"><span class="tokyo-badge" style="font-size: 1.1rem;">キーワード</span><span style="font-size: 1.2rem; font-weight: 700; color: var(--primary-color);">{search_query['keyword']}</span><span class="result-badge" style="font-size: 1.2rem; padding: 0.25rem 0.6rem; margin-left: 0.5rem;">検索結果: {result_count}件</span></div></div></div>""", unsafe_allow_html=True)

                
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
            st.error("データの読み込みに失敗しました。検索条件に戻って再度実行してください。")

# フッター
st.markdown("""
    <div class="footer">
        <p>© 2025 東京都議会議事録ビューア | このシステムは東京都議会の議事録を閲覧するためのものです</p>
    </div>
""", unsafe_allow_html=True)
