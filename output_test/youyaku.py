import json
import os
import re
from collections import defaultdict
from janome.tokenizer import Tokenizer

def preprocess_text(text):
    """テキストの前処理を強化"""
    # 全角句点で統一し、連続する句点を除去
    text = text.replace('.', '。').replace('．', '。')
    text = re.sub(r'。+', '。', text)
    # 不要な空白を除去
    text = re.sub(r'\s+', '', text)
    return text.strip('。')

def extract_keywords(text, cluster_keywords_str="", n=5):
    """キーワード抽出を改良（クラスタキーワードを考慮）"""
    t = Tokenizer()
    words = []
    
    for token in t.tokenize(text):
        pos = token.part_of_speech.split(',')[0]
        # 名詞、動詞、形容詞に限定し、記号を除外
        if pos in ['名詞', '動詞', '形容詞'] and token.surface not in ['。', '、']:
            words.append(token.surface)
    
    word_counts = defaultdict(int)
    for word in words:
        if len(word) > 1:  # 1文字の単語を除外
            word_counts[word] += 1
    
    # クラスタキーワードを考慮
    if cluster_keywords_str:
        cluster_keywords = cluster_keywords_str.split('・')
        for kw in cluster_keywords:
            if kw in word_counts:
                word_counts[kw] += 3  # クラスタキーワードに重み付け
    
    return sorted(word_counts.items(), key=lambda x: -x[1])[:n]

def summarize_content(text, cluster_keywords="", target_length=150):
    """改良版要約関数"""
    if not text or len(text) <= target_length:
        return text
    
    # 文分割（句点できれいに分割）
    sentences = [s.strip() for s in text.split('。') if s.strip()]
    if not sentences:
        return ""
    
    # キーワード抽出（クラスタキーワードも考慮）
    keywords = [kw[0] for kw in extract_keywords(text, cluster_keywords)]
    
    # 文の重要度評価
    scored_sentences = []
    for i, sentence in enumerate(sentences):
        score = 0
        
        # キーワード含有スコア
        keyword_score = sum(5 for kw in keywords if kw in sentence)
        score += keyword_score
        
        # 文の位置スコア（最初と最後の文を重視）
        position_score = 1.5 if i == 0 or i == len(sentences)-1 else 1
        score *= position_score
        
        # 文の長さスコア（適度な長さを重視）
        length_score = min(1, len(sentence)/30)  # 30文字前後を理想とする
        score *= length_score
        
        scored_sentences.append((score, sentence, i))  # 元のインデックスも保持
    
    # スコア順にソート
    scored_sentences.sort(reverse=True, key=lambda x: x[0])
    
    # 要約生成
    selected_indices = set()
    current_length = 0
    summary_sentences = []
    
    for score, sentence, orig_idx in scored_sentences:
        if current_length + len(sentence) <= target_length:
            selected_indices.add(orig_idx)
            current_length += len(sentence)
    
    # 元の順序で文を選択
    for idx, sentence in enumerate(sentences):
        if idx in selected_indices:
            summary_sentences.append(sentence)
            if len('。'.join(summary_sentences)) >= target_length:
                break
    
    # 句点で結合
    result = '。'.join(summary_sentences)
    
    # 句点で終わっていない場合は追加
    if not result.endswith('。'):
        result += '。'
    
    # 長さ調整（句点を追加した分を考慮）
    return result[:target_length]

def process_files():
    """ファイル処理のメイン関数"""
    # 出力ディレクトリ作成
    output_dir = "output_test"
    os.makedirs(output_dir, exist_ok=True)

    # 2015年から2024年まで処理
    for year in range(2015, 2025):
        input_file = f"outputs/{year}.json"
        output_file = f"{output_dir}/{year}.json"  # output_test内に保存
        
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            for meeting in data:
                if not isinstance(meeting, dict):
                    continue
                    
                if 'categories' in meeting:
                    for category in meeting['categories']:
                        if not isinstance(category, dict):
                            continue
                            
                        if 'clusters' in category:
                            for cluster in category['clusters']:
                                if not isinstance(cluster, dict):
                                    continue
                                    
                                if 'items' in cluster:
                                    for item in cluster['items']:
                                        if not isinstance(item, dict):
                                            continue
                                            
                                        if 'body' in item and 'cluster_keywords' in cluster:
                                            # 前処理
                                            processed_text = preprocess_text(item['body'])
                                            # 要約（クラスタキーワードを渡す）
                                            item['body'] = summarize_content(
                                                processed_text,
                                                cluster['cluster_keywords']
                                            )

            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2, separators=(',', ': '))

            print(f"要約完了: {year}.json")

        except FileNotFoundError:
            print(f"ファイルが見つかりません: {input_file}")
        except json.JSONDecodeError:
            print(f"JSON解析エラー: {input_file}")
        except Exception as e:
            print(f"{year}年処理中にエラー: {str(e)}")

    print("全ての年度の処理が完了しました")

if __name__ == "__main__":
    process_files()
