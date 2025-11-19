import os
import logging
from datetime import datetime

class FileManager:
    def __init__(self, base_path=None):
        self.base_path = base_path or os.getcwd()
        self.ensure_directories()
    
    def ensure_directories(self):
        """Pastikan direktori yang diperlukan ada"""
        os.makedirs(self.base_path, exist_ok=True)
    
    def get_offset(self):
        """Baca nilai offset saat ini"""
        offset_file = os.path.join(self.base_path, "offset.txt")
        try:
            if os.path.exists(offset_file):
                with open(offset_file, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if content.isdigit():
                        return int(content)
            return 0
        except Exception as e:
            logging.error(f"Error reading offset: {e}")
            return 0
    
    def update_offset(self, offset_value):
        """Update nilai offset"""
        offset_file = os.path.join(self.base_path, "offset.txt")
        try:
            with open(offset_file, 'w', encoding='utf-8') as f:
                f.write(str(offset_value))
            return True
        except Exception as e:
            logging.error(f"Error updating offset: {e}")
            return False
    
    def get_logs(self, max_lines=1000):
        """Baca isi log file"""
        log_file = os.path.join(self.base_path, "download.log")
        try:
            if os.path.exists(log_file):
                with open(log_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    # Return last max_lines lines
                    return ''.join(lines[-max_lines:])
            return "Log file tidak ditemukan"
        except Exception as e:
            return f"Error membaca log: {str(e)}"
    
    def clear_logs(self):
        """Hapus isi log file"""
        log_file = os.path.join(self.base_path, "download.log")
        try:
            open(log_file, 'w').close()
            return True
        except Exception as e:
            logging.error(f"Error clearing logs: {e}")
            return False
    
    def write_log(self, message):
        """Tulis pesan ke log file"""
        log_file = os.path.join(self.base_path, "download.log")
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"{timestamp} - {message}\n")
            return True
        except Exception as e:
            logging.error(f"Error writing log: {e}")
            return False

# Global file manager instance
file_manager = FileManager()