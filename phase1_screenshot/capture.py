#!/usr/bin/env python3
"""
Kindle for Mac 自動スクリーンショット取得スクリプト
"""

import pyautogui
import time
import json
import os
import argparse
from datetime import datetime
from PIL import Image

class KindleCapture:
    def __init__(self, config_path='config.json'):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
    def setup_kindle(self):
        """Kindleアプリをアクティブにする"""
        # AppleScriptを使用してKindleをアクティブ化
        os.system('''
        osascript -e 'tell application "Kindle" to activate'
        ''')
        time.sleep(2)
        
    def capture_page(self, page_num, output_dir):
        """現在のページをキャプチャ"""
        area = self.config['capture_area']
        screenshot = pyautogui.screenshot(region=(
            area['x'], area['y'], area['width'], area['height']
        ))
        
        # ファイル名を生成
        filename = f"page_{page_num:03d}.{self.config['output_format']}"
        filepath = os.path.join(output_dir, filename)
        
        # 画像を保存
        screenshot.save(filepath)
        return filepath
        
    def turn_page(self):
        """次のページへ移動"""
        pyautogui.press('right')
        time.sleep(self.config['page_turn_delay'])
        
    def capture_book(self, book_name, num_pages, start_page=1):
        """本全体をキャプチャ"""
        # 出力ディレクトリを作成
        output_dir = os.path.join('output', book_name)
        os.makedirs(output_dir, exist_ok=True)
        
        # Kindleをセットアップ
        self.setup_kindle()
        
        print(f"キャプチャを開始します: {book_name}")
        print(f"ページ数: {start_page} - {start_page + num_pages - 1}")
        
        # 各ページをキャプチャ
        for i in range(num_pages):
            current_page = start_page + i
            print(f"ページ {current_page} をキャプチャ中...")
            
            filepath = self.capture_page(current_page, output_dir)
            print(f"  保存: {filepath}")
            
            # 最後のページ以外は次へ
            if i < num_pages - 1:
                self.turn_page()
                
        print(f"\\nキャプチャ完了: {output_dir}")

def main():
    parser = argparse.ArgumentParser(description='Kindle自動スクリーンショット')
    parser.add_argument('--book', required=True, help='本の名前')
    parser.add_argument('--pages', type=int, default=10, help='ページ数')
    parser.add_argument('--start', type=int, default=1, help='開始ページ')
    parser.add_argument('--end', type=int, help='終了ページ（--pagesより優先）')
    
    args = parser.parse_args()
    
    # ページ数を計算
    if args.end:
        num_pages = args.end - args.start + 1
    else:
        num_pages = args.pages
        
    # キャプチャを実行
    capture = KindleCapture()
    capture.capture_book(args.book, num_pages, args.start)

if __name__ == '__main__':
    main()